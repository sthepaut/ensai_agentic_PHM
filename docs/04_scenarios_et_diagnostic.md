# Scénarios et diagnostic

Ces scénarios décrivent les situations à envisager.
Ils ne constituent pas une attribution de diagnostic à une trajectoire.

## Vieillissement progressif sans événement particulier

Le moteur s'éloigne progressivement de son état nominal, sans
dégradation additionnelle particulière.

Indices compatibles : tendances lentes et persistantes, sans changement
net inexpliqué par les conditions de fonctionnement.

« Vieillissement normal » ne signifie pas « paramètres exactement nuls »,
ni « aucune limite ne peut être atteinte ».

## Encrassement du compresseur HP

Dans la représentation pédagogique, l'encrassement ajoute une diminution
progressive des paramètres de rendement et de débit corrigé du
compresseur HP.

Indices à rechercher : évolution conjointe persistante des estimations
HPC, éventuellement changement de tendance et modification cohérente
des mesures.

Une hausse de température ou de consommation peut soutenir une
hypothèse selon le contexte, mais son signe n'est pas une règle
universelle. Ne pas attribuer un encrassement à partir d'une seule mesure.

Vérifications possibles : comparer des périodes aux conditions proches,
examiner les deux paramètres HPC et rechercher une explication par
un capteur.

## Dérive d'un capteur

Un capteur acquiert un biais évolutif. Les valeurs peuvent rester
numériquement plausibles, avec usable=True.

Indices possibles : évolution atypique d'une mesure, incohérence entre
mesures, ou déplacement des estimations MLP difficile à expliquer
par une évolution moteur commune.

Le MLP utilise les capteurs : ses sorties ne sont donc pas une
confirmation indépendante d'une mesure suspecte.

De même, marge EGT et LPT_Tin contiennent la même information thermique.

Vérifications possibles : examiner d'autres mesures et proposer un
contrôle de cohérence ou un étalonnage du capteur suspect.

## Ambiguïtés

Un même effet observé peut avoir plusieurs causes.
Plusieurs indicateurs issus des mêmes mesures peuvent se tromper ensemble.

Aucune signature décrite ici ne garantit un diagnostic unique.
Conserver des hypothèses alternatives et préciser quelles informations
manquent.

Ne pas exploiter noms de fichiers, numéros de trajectoires ou métadonnées
de génération pour retrouver une étiquette cachée.

## Maintenance

Le lavage compresseur et ses effets ne sont pas modélisés dans la
version actuelle. Ne pas annoncer un gain de lavage, une durée optimale
de maintenance ou une RUL validée.