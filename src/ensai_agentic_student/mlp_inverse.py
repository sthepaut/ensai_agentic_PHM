"""Inverse MLP: raw data as inputs, physical units as outputs."""
import warnings

import numpy as np
import pandas as pd
import torch
from torch import nn


class InverseMLP(nn.Module):
    def __init__(self, feature_cols, target_cols, hidden_sizes=(128, 128, 128)):
        super().__init__()
        self.feature_cols = list(feature_cols)
        self.target_cols = list(target_cols)
        self.hidden_sizes = list(hidden_sizes)
        dimensions = [len(feature_cols), *hidden_sizes, len(target_cols)]
        layers = []
        for i in range(len(dimensions) - 1):
            layers.append(nn.Linear(dimensions[i], dimensions[i+1]))
            if i < len(dimensions) - 2:
                layers.append(nn.SiLU())
        self.network = nn.Sequential(*layers)
        # Persistent buffers: saved in state_dict and moved with .to().
        for name, size, ones in [('x_mean', len(feature_cols), False),
                                  ('x_scale', len(feature_cols), True),
                                  ('y_mean', len(target_cols), False),
                                  ('y_scale', len(target_cols), True)]:
            self.register_buffer(name, torch.ones(size) if ones else torch.zeros(size))
        self.register_buffer('x_train_min', torch.zeros(len(feature_cols)))
        self.register_buffer('x_train_max', torch.zeros(len(feature_cols)))
        self.register_buffer('scalers_fitted', torch.tensor(False))

    @torch.no_grad()
    def fit_scalers(self, x_train, y_train):
        if bool(self.scalers_fitted.item()):
            raise RuntimeError('Scalers already fitted: do not refit them during inference.')
        x, y = np.asarray(x_train, dtype=np.float64), np.asarray(y_train, dtype=np.float64)
        if x.ndim != 2 or y.ndim != 2 or x.shape != (len(y), len(self.feature_cols)) or y.shape[1] != len(self.target_cols):
            raise ValueError('Incorrect training data dimensions.')
        if len(x) < 2 or not (np.isfinite(x).all() and np.isfinite(y).all()):
            raise ValueError('Insufficient training data or non-finite values.')
        for prefix, array in [('x', x), ('y', y)]:
            std = array.std(axis=0, ddof=0)
            if (std < 1e-12).any():
                raise ValueError(f'Nearly constant column in {prefix}_train; check the dataset.')
            for suffix, value in [('mean', array.mean(axis=0)), ('scale', std)]:
                buffer = getattr(self, f'{prefix}_{suffix}')
                buffer.copy_(torch.as_tensor(value, dtype=buffer.dtype, device=buffer.device))
        self.x_train_min.copy_(torch.as_tensor(x.min(axis=0), dtype=self.x_mean.dtype, device=self.x_mean.device))
        self.x_train_max.copy_(torch.as_tensor(x.max(axis=0), dtype=self.x_mean.dtype, device=self.x_mean.device))
        self.scalers_fitted.fill_(True)

    def forward(self, x_raw):
        # Training also uses this path: no double normalization.
        x_scaled = (x_raw - self.x_mean) / self.x_scale
        y_scaled = self.network(x_scaled)
        return y_scaled * self.y_scale + self.y_mean

    @torch.inference_mode()
    def predict(self, data, batch_size=4096, warn_out_of_range=False):
        if not bool(self.scalers_fitted.item()):
            raise RuntimeError('Scalers not fitted: load a trained model.')
        if batch_size < 1:
            raise ValueError('batch_size must be positive.')
        if isinstance(data, pd.DataFrame):
            missing = set(self.feature_cols) - set(data.columns)
            if missing:
                raise ValueError(f'Missing inputs: {sorted(missing)}')
            if 'phase' in data and not data['phase'].eq('CR').all():
                raise ValueError('CR model: other phases are not supported.')
            values = data.loc[:, self.feature_cols].to_numpy(dtype=np.float32)
            index = data.index
        else:
            values = np.asarray(data, dtype=np.float32)
            if values.ndim == 1:
                values = values[None, :]
            index = None
        if values.ndim != 2 or values.shape[1] != len(self.feature_cols) or not np.isfinite(values).all():
            raise ValueError('Non-finite inputs or incorrect dimensions.')
        if warn_out_of_range and len(values):
            lo, hi = self.x_train_min.cpu().numpy(), self.x_train_max.cpu().numpy()
            count = int(((values < lo) | (values > hi)).any(axis=1).sum())
            if count:
                warnings.warn(f'{count}/{len(values)} rows outside the training min/max bounds. This check does not detect all out-of-distribution data.')
        was_training = self.training
        self.eval()
        try:
            parts = [self(torch.as_tensor(values[i:i+batch_size], device=self.x_mean.device)).cpu().numpy()
                     for i in range(0, len(values), batch_size)]
        finally:
            self.train(was_training)
        result = np.concatenate(parts) if parts else np.empty((0, len(self.target_cols)), dtype=np.float32)
        return pd.DataFrame(result, columns=self.target_cols, index=index)


def load_model(path, device='cpu'):
    checkpoint = torch.load(path, map_location='cpu', weights_only=True)
    if checkpoint.get('format_version') != 1:
        raise ValueError('Unsupported checkpoint format.')
    model = InverseMLP(checkpoint['feature_cols'], checkpoint['target_cols'], checkpoint['hidden_sizes'])
    model.load_state_dict(checkpoint['state_dict'], strict=True)
    if not bool(model.scalers_fitted.item()):
        raise ValueError('Checkpoint does not contain fitted scalers.')
    model.to(device).eval()
    return model