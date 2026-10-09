"""Read observations from the project's trajectory pickle files."""
from pathlib import Path

import pandas as pd


def get_measure(trajectory_id, timestep=None, data_dir=None):
    """Return observations for a trajectory or a single timestep.

    trajectory_id : integer, e.g. 1 for trajectory_000001.pkl.
    timestep : requested timestep; None returns the full trajectory.
    data_dir : optional directory; defaults to data/trajectories in the repository.
    Returns: a DataFrame with a single row if timestep is specified.
    The pickle's truth, event, and config fields are not returned.
    """
    if data_dir is None:
        data_dir = Path(__file__).resolve().parents[3] / 'data' / 'trajectories'
    path = Path(data_dir) / f'trajectory_{trajectory_id:06d}.pkl'
    # Only load trusted pickle files provided for the project.
    data = pd.read_pickle(path)
    observations = data['observations'].copy()
    if timestep is not None:
        observations = observations.loc[observations['timestep'] == timestep].copy()
        if observations.empty:
            raise ValueError(
                f'Timestep {timestep} not found in trajectory {trajectory_id}.'
            )
    return observations