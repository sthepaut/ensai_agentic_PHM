# Mission et périmètre

## Mission

Analyser l'historique disponible d'un moteur pour repérer une évolution
anormale, formuler des hypothèses et recommander une surveillance ou
une inspection justifiée.

Le système fournit une aide à la décision pédagogique. Il ne certifie
ni l'aptitude au vol ni la sécurité d'un moteur réel.

## Questions à traiter

- Les observations sont-elles exploitables ?
- L'évolution est-elle compatible avec un vieillissement progressif ?
- Existe-t-il des indices d'une anomalie moteur ou d'une dérive de capteur ?
- Quelles vérifications permettraient de départager les hypothèses ?
- Quelle action est proportionnée aux éléments disponibles ?

## Données et domaine

Une trajectoire représente un moteur observé au fil de vols successifs.
Un timestep est une observation en cruise, pas une seconde ni une
heure de fonctionnement.

Les données proviennent de calculs stationnaires successifs d'OpenDeckSMR.
La succession des états est définie par un scénario synthétique ;
elle n'est pas une simulation dynamique complète du moteur.

La première version couvre uniquement CR, avec Fan et Booster nominaux
et six paramètres de santé variables pour le compresseur HP et les
turbines HP/BP.

## Limites

Les lois de vieillissement ne sont pas calibrées sur une durée de vie
industrielle. Une alerte ne détermine pas automatiquement sa cause.

Les outils actuels n'estiment pas de RUL et ne simulent ni lavage ni
réparation. Ne pas produire une durée de vie chiffrée en se fondant
sur la longueur d'un fichier.

L'analyse doit pouvoir conclure à une information insuffisante,
plutôt que forcer l'attribution d'un scénario.