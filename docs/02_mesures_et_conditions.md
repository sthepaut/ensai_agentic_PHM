# Mesures et conditions de fonctionnement

## Capteurs

| Colonne | Signification | Unité |
|---|---|---|
| HPC_Tout | Température en sortie du compresseur HP | K |
| HP_Nmech | Vitesse de rotation de l'arbre HP | tr/min |
| HPC_Tin | Température en entrée du compresseur HP | K |
| LPT_Tin | Température en entrée de la turbine BP | K |
| Fuel_flow | Débit de carburant | kg/s |
| HPC_Pout_st | Pression statique en sortie du compresseur HP | Pa |

Ces valeurs sont des sorties du simulateur, éventuellement modifiées
par un défaut de mesure dans le scénario. Ne pas les confondre avec
les états de santé estimés.

## Conditions connues

| Colonne | Signification | Unité | Domaine de cette version |
|---|---|---|---|
| DTAMB | Écart à la température atmosphérique standard | K d'écart | 9 à 11 |
| ALT | Altitude | ft | 34 900 à 35 100 |
| MACH | Nombre de Mach | Sans unité | 0,76 à 0,80 |
| COMMAND | Consigne de poussée en CR, selon l'interface OpenDeckSMR | lbf | 24 900 à 25 100 |
| phase | Phase de fonctionnement | Texte | CR |

Une variation de mesure peut venir des conditions de fonctionnement.
Comparer des points dans des conditions proches ou utiliser un outil
qui prend ces conditions en entrée.

La présence des conditions dans le MLP ne garantit pas une correction
parfaite.

## Temps et qualité

- trajectory_id identifie le moteur ou la trajectoire ; il ne constitue
  pas un indice de diagnostic.
- timestep ordonne les observations. Conserver les véritables écarts
  entre instants.
- usable indique qu'un point satisfait les contrôles de qualité de
  simulation.
- Convergence décrit le résultat numérique du simulateur, pas l'état
  mécanique du moteur.
- Un NaN désigne une valeur manquante ou non exploitable, jamais une
  valeur nominale.

Les points rejetés doivent rester des trous dans les analyses temporelles.
Signaler si les données manquantes empêchent une conclusion.

Un biais capteur peut rester fini et être marqué usable.

## Proxy EGT

LPT_Tin est physiquement une température d'entrée turbine BP.
Le projet l'utilise, par hypothèse pédagogique, comme proxy EGT.
Cette convention ne rend pas ces deux températures physiquement
équivalentes.

La limite pédagogique de 1 150 K et les marges calculées avec elle
ne sont pas des limites constructeur.

Une différence de température de 1 K a la même amplitude qu'une
différence de 1 °C ; ne pas confondre températures absolues et écarts.