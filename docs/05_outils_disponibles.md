# Outils disponibles

Les outils réalisent des calculs. Le diagnostic et la recommandation
sont à construire à partir de leurs résultats.

## get_measure

Import : ensai_agentic_student.tools.data

Signature : get_measure(trajectory_id, timestep=None, data_dir=None)

- trajectory_id : entier identifiant une trajectoire.
- timestep : instant demandé ; None renvoie la trajectoire complète.
- data_dir : dossier optionnel, par défaut data/trajectories du dépôt.
- Sortie : DataFrame des observations, avec une ligne si un instant
  est demandé.

L'outil ne renvoie pas truth, event ou config.
Une absence de fichier ou d'instant est une erreur d'accès aux données,
pas une panne moteur.

Pour une décision au temps t, exclure tout timestep supérieur à t
avant l'analyse. L'outil peut fournir une trajectoire complète et
n'effectue pas cette restriction automatiquement.

## estimation_indicateurs_mlp

Import : ensai_agentic_student.tools.estimation

Signature : estimation_indicateurs_mlp(observations, model_path=None)

- Entrée : DataFrame contenant les quatre conditions et les six
  mesures brutes.
- Modèle par défaut : models/best_model.pt.
- Sortie : DataFrame des six indicateurs de santé, aligné sur
  l'index d'entrée.

Le modèle est chargé puis réutilisé. Ne pas normaliser les entrées
manuellement.

La version prévue de la brique filtre usable et réinsère les lignes
rejetées sous forme de NaN.

Une colonne obligatoire absente ou une valeur non finie non signalée
par usable peut provoquer une erreur. Ne pas inventer une mesure
pour compléter une entrée.

## marge_EGT

Import : ensai_agentic_student.tools.marge_egt

Signature : marge_EGT(observations, temperature_limite, capteur="LPT_Tin")

Calcul : marge_EGT = temperature_limite - température du capteur.

Configuration pédagogique actuelle : temperature_limite=1150.0, en K.
L'argument reste obligatoire : la valeur n'est pas un défaut caché
dans l'outil.

Sortie : DataFrame avec timestep si présent, temperature_proxy_EGT
et marge_EGT. Les points invalides produisent des NaN.

- Marge positive : sous la limite choisie.
- Marge nulle : limite atteinte.
- Marge négative : dépassement de la limite choisie.

Exemple : à 1 130 K, la marge vaut 20 K pour une limite de 1 150 K.

Cette limite est provisoire, commune aux trajectoires, et non issue
d'une certification. Ne pas la recalculer pour chaque moteur ni la
modifier pour obtenir un diagnostic souhaité.

La marge n'est pas corrigée des conditions de vol. Elle ne permet pas,
seule, d'attribuer une cause ou de déterminer une durée de vie.

## Outils non disponibles dans cette version

Aucune brique d'appel simulateur, de Kalman, de RUL ou d'action de
maintenance n'est fournie dans l'interface actuelle.
Ne pas prétendre les avoir exécutées.