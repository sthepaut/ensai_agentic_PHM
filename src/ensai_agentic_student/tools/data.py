"""Lecture des observations dans les pickles de trajectoires du projet."""
from pathlib import Path

import pandas as pd


def get_measure(trajectory_id, timestep=None, data_dir=None):
    """Retourner les observations d'une trajectoire, ou d'un seul instant.

    trajectory_id : entier, par exemple 1 pour trajectory_000001.pkl.
    timestep : instant demandé ; None renvoie toute la trajectoire.
    data_dir : dossier optionnel ; par défaut data/trajectories du dépôt.
    Retour : DataFrame, avec une seule ligne si timestep est précisé.
    Les champs truth, event et config du pickle ne sont pas renvoyés.
    """
    if data_dir is None:
        data_dir = Path(__file__).resolve().parents[3] / 'data' / 'trajectories'
    path = Path(data_dir) / f'trajectory_{trajectory_id:06d}.pkl'
    # Charger uniquement les pickles de confiance fournis pour le projet.
    data = pd.read_pickle(path)
    observations = data['observations'].copy()
    if timestep is not None:
        observations = observations.loc[observations['timestep'] == timestep].copy()
        if observations.empty:
            raise ValueError(f'Instant {timestep} absent de la trajectoire {trajectory_id}.')
    return observations
