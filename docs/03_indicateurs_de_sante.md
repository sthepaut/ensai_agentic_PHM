# Indicateurs de santé

## Signification

Les indicateurs sont des écarts au nominal qui modifient les cartes
des composants dans OpenDeckSMR :

- mapEff concerne le rendement de la carte.
- mapWc concerne le débit corrigé de la carte.
- Zéro correspond au réglage nominal.
- Une valeur négative ou positive indique le sens de l'écart de carte.

Ces paramètres ne sont ni des probabilités de panne, ni une RUL,
ni des mesures directes des capteurs.

Ne pas convertir automatiquement un delta de -0,02 en une perte de
deux points de rendement physique : l'effet dépend de la convention
de carte et du point de fonctionnement.

## Six sorties du MLP

| Colonne | Composant et paramètre | Domaine d'entraînement |
|---|---|---|
| deg_CmpH_s_mapEff_in | Rendement compresseur HP | [-0,05 ; 0] |
| deg_CmpH_s_mapWc_in | Débit corrigé compresseur HP | [-0,05 ; 0,03] |
| deg_TrbH_s_mapEff_in | Rendement turbine HP | [-0,05 ; 0] |
| deg_TrbH_s_mapWc_in | Débit corrigé turbine HP | [-0,05 ; 0,05] |
| deg_TrbL_s_mapEff_in | Rendement turbine BP | [-0,05 ; 0] |
| deg_TrbL_s_mapWc_in | Débit corrigé turbine BP | [-0,05 ; 0,05] |

Les quatre paramètres Fan et Booster sont fixés à zéro dans cette
version. Ils ne sont pas estimés.

Les bornes ci-dessus décrivent le domaine d'apprentissage :
ce ne sont pas des seuils de panne.

Un débit de carte positif ne signifie pas automatiquement une
amélioration de santé.

## Interpréter les estimations

Le MLP traite chaque observation indépendamment, sans utiliser son
historique. Il normalise les entrées et remet les sorties à leur
échelle d'origine.

La précision varie selon les paramètres. L'évaluation initiale est
nettement meilleure sur les deux paramètres HPC et le débit HPT
que sur les rendements HPT/LPT et le débit LPT.

Les sorties ne sont pas bornées artificiellement et peuvent dépasser
le domaine d'entraînement. Un dépassement doit être signalé comme
une limite possible de l'estimation, pas automatiquement comme une
panne sévère.

Examiner la persistance des évolutions et leur cohérence avec les
mesures et les conditions.

Un biais capteur peut être interprété à tort comme une variation
de santé. Aucune incertitude calibrée n'est fournie par ce MLP.