# Base de connaissances des agents

Ces documents servent à interpréter les observations et les outils
du projet ENSAI de maintenance prédictive.

## Documents

- [Mission et périmètre](01_objectif_et_perimetre.md)
- [Mesures et conditions](02_mesures_et_conditions.md)
- [Indicateurs de santé](03_indicateurs_de_sante.md)
- [Scénarios et diagnostic](04_scenarios_et_diagnostic.md)
- [Outils disponibles](05_outils_disponibles.md)
- [Décisions et justification](06_decisions_et_justification.md)

## Conventions

Les noms de colonnes sont ceux du code. Les exemples et seuils
pédagogiques ne sont pas des prescriptions constructeur.

Les connaissances générales sur les scénarios peuvent être utilisées.
Les étiquettes de scénario, états réels et événements cachés d'une
trajectoire ne sont pas des observations autorisées.

À une date de décision donnée, utiliser seulement les observations
disponibles jusqu'à cette date. Les identifiants servent à retrouver
les données, jamais à déduire le scénario.

Version initiale : lecture des observations, inversion MLP et marge
thermique. Ne pas supposer disponibles un Kalman, une RUL ou une
action de maintenance.

## Sources et portée

Les définitions des capteurs, conditions et états reposent sur OpenDeckSMR :

- https://github.com/OpenDeckLab/OpenDeckSMR/blob/main/doc/doc.md
- https://github.com/OpenDeckLab/OpenDeckSMR/blob/main/src/odsmr/sensors.py

Les signatures d'outils et les hypothèses pédagogiques sont propres
à ce projet. Le code et la configuration effectivement fournis font
référence en cas de changement.