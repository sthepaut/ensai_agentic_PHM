"""Marge thermique pédagogique : LPT_Tin est supposée être un proxy de l'EGT.

Cette hypothèse ne constitue pas une identification physique des deux capteurs.
Aucune correction selon les conditions de vol n'est appliquée.
"""
import numpy as np
import pandas as pd


def marge_EGT(observations, temperature_limite, capteur='LPT_Tin'):
    """Calculer temperature_limite - température observée.

    observations : DataFrame retourné par get_measure.
    temperature_limite : limite pédagogique fixe, dans la même unité que le capteur.
    capteur : nom exact de la colonne utilisée comme proxy EGT.

    Retour : DataFrame avec timestep (si présent), temperature_proxy_EGT,
    marge_EGT. Les points non exploitables restent présents avec des NaN.
    Une marge négative signifie un dépassement de la limite choisie ; ce n'est
    pas, à elle seule, un diagnostic de panne ou une décision de maintenance.
    """
    if temperature_limite is None or not np.isscalar(temperature_limite):
        raise ValueError('Fournir une temperature_limite numérique dans la même unité que le capteur.')
    temperature_limite = float(temperature_limite)
    if not np.isfinite(temperature_limite):
        raise ValueError('temperature_limite doit être finie.')
    if capteur not in observations.columns:
        raise ValueError(f'Capteur {capteur!r} absent. Colonnes disponibles : {list(observations.columns)}')

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
