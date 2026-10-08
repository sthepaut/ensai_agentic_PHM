"""Estimation des six paramètres de santé à partir des observations brutes."""
from functools import lru_cache
from pathlib import Path

from ..mlp_inverse import load_model


@lru_cache(maxsize=1)
def _load_mlp(model_path):
    return load_model(model_path, device='cpu')


def estimation_indicateurs_mlp(observations, model_path=None):
    """Prédire les six états santé, une ligne par observation.

    observations : DataFrame contenant conditions CR et six mesures brutes.
    model_path : checkpoint optionnel ; défaut models/best_model.pt du dépôt.
    Retour : DataFrame des six estimations, dans leurs unités d'origine.
    Les scalers sont intégrés au modèle : ne pas normaliser les entrées.
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
