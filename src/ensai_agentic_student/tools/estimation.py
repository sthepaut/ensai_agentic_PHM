"""Estimate the six health parameters from raw observations."""
from functools import lru_cache
from pathlib import Path

from ..mlp_inverse import load_model


@lru_cache(maxsize=1)
def _load_mlp(model_path):
    return load_model(model_path, device='cpu')


def estimation_indicateurs_mlp(observations, model_path=None):
    """Predict the six health states, with one row per observation.

    observations : DataFrame containing CR conditions and six raw measurements.
    model_path : optional checkpoint; defaults to models/best_model.pt in the repository.
    Returns: a DataFrame of the six estimates, in their original units.
    Scalers are built into the model: do not normalize the inputs.
    """
    if model_path is None:
        model_path = Path(__file__).resolve().parents[3] / 'models' / 'best_model.pt'
    model = _load_mlp(str(Path(model_path).resolve()))

    if "usable" in observations.columns:
        valides = observations["usable"].eq(True)
        predictions = model.predict(observations.loc[valides])
    else:
        predictions = model.predict(observations)

    return predictions.reindex(observations.index)