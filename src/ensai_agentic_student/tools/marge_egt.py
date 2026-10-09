"""Educational thermal margin: LPT_Tin is assumed to be an EGT proxy.

This assumption does not imply physical equivalence between the two sensors.
No correction for flight conditions is applied.
"""
import numpy as np
import pandas as pd


def marge_EGT(observations, temperature_limite, capteur='LPT_Tin'):
    """Calculate temperature_limite - observed temperature.

    observations : DataFrame returned by get_measure.
    temperature_limite : fixed educational limit, in the same unit as the sensor.
    capteur : exact name of the column used as the EGT proxy.

    Returns: a DataFrame with timestep (if present), temperature_proxy_EGT,
    and marge_EGT. Unusable observations remain present with NaN values.
    A negative margin means the chosen limit has been exceeded; on its own,
    this is neither a fault diagnosis nor a maintenance decision.
    """
    if temperature_limite is None or not np.isscalar(temperature_limite):
        raise ValueError(
            'Provide a numerical temperature_limite in the same unit as the sensor.'
        )
    temperature_limite = float(temperature_limite)
    if not np.isfinite(temperature_limite):
        raise ValueError('temperature_limite must be finite.')
    if capteur not in observations.columns:
        raise ValueError(
            f'Sensor {capteur!r} not found. Available columns: {list(observations.columns)}'
        )

    temperature = observations[capteur].astype(float)
    valides = np.isfinite(temperature)
    if 'usable' in observations.columns:
        valides = valides & observations['usable'].eq(True).fillna(False)
    temperature = temperature.where(valides)

    resultat = pd.DataFrame(index=observations.index)
    if 'timestep' in observations.columns:
        resultat['timestep'] = observations['timestep']
    resultat['temperature_proxy_EGT'] = temperature
    resultat['marge_EGT'] = temperature_limite - temperature
    return resultat