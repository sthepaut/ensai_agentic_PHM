"""MLP d'inversion : données brutes en entrée, unités physiques en sortie."""
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
        # Buffers persistants : sauvegardés dans state_dict, déplacés avec .to().
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
            raise RuntimeError('Scalers déjà ajustés : ne pas les réajuster en inférence.')
        x, y = np.asarray(x_train, dtype=np.float64), np.asarray(y_train, dtype=np.float64)
        if x.ndim != 2 or y.ndim != 2 or x.shape != (len(y), len(self.feature_cols)) or y.shape[1] != len(self.target_cols):
            raise ValueError('Dimensions des données de train incorrectes.')
        if len(x) < 2 or not (np.isfinite(x).all() and np.isfinite(y).all()):
            raise ValueError('Train insuffisant ou non fini.')
        for prefix, array in [('x', x), ('y', y)]:
            std = array.std(axis=0, ddof=0)
            if (std < 1e-12).any():
                raise ValueError(f'Colonne presque constante dans {prefix}_train ; vérifier le dataset.')
            for suffix, value in [('mean', array.mean(axis=0)), ('scale', std)]:
                buffer = getattr(self, f'{prefix}_{suffix}')
                buffer.copy_(torch.as_tensor(value, dtype=buffer.dtype, device=buffer.device))
        self.x_train_min.copy_(torch.as_tensor(x.min(axis=0), dtype=self.x_mean.dtype, device=self.x_mean.device))
        self.x_train_max.copy_(torch.as_tensor(x.max(axis=0), dtype=self.x_mean.dtype, device=self.x_mean.device))
        self.scalers_fitted.fill_(True)

    def forward(self, x_raw):
        # L'entraînement appelle aussi ce chemin : pas de double normalisation.
        x_scaled = (x_raw - self.x_mean) / self.x_scale
        y_scaled = self.network(x_scaled)
        return y_scaled * self.y_scale + self.y_mean

    @torch.inference_mode()
    def predict(self, data, batch_size=4096, warn_out_of_range=False):
        if not bool(self.scalers_fitted.item()):
            raise RuntimeError('Scalers non ajustés : charger un modèle entraîné.')
        if batch_size < 1:
            raise ValueError('batch_size doit être positif.')
        if isinstance(data, pd.DataFrame):
            missing = set(self.feature_cols) - set(data.columns)
            if missing:
                raise ValueError(f'Entrées manquantes : {sorted(missing)}')
            if 'phase' in data and not data['phase'].eq('CR').all():
                raise ValueError('Modèle CR : autres phases non supportées.')
            values = data.loc[:, self.feature_cols].to_numpy(dtype=np.float32)
            index = data.index
        else:
            values = np.asarray(data, dtype=np.float32)
            if values.ndim == 1:
                values = values[None, :]
            index = None
        if values.ndim != 2 or values.shape[1] != len(self.feature_cols) or not np.isfinite(values).all():
            raise ValueError('Entrées non finies ou dimensions incorrectes.')
        if warn_out_of_range and len(values):
            lo, hi = self.x_train_min.cpu().numpy(), self.x_train_max.cpu().numpy()
            count = int(((values < lo) | (values > hi)).any(axis=1).sum())
            if count:
                warnings.warn(f'{count}/{len(values)} lignes hors des min/max du train. Ce contrôle ne détecte pas toutes les données hors distribution.')
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
        raise ValueError('Format de checkpoint non supporté.')
    model = InverseMLP(checkpoint['feature_cols'], checkpoint['target_cols'], checkpoint['hidden_sizes'])
    model.load_state_dict(checkpoint['state_dict'], strict=True)
    if not bool(model.scalers_fitted.item()):
        raise ValueError('Checkpoint sans scalers ajustés.')
    model.to(device).eval()
    return model
