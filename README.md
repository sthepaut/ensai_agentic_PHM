# ENSAI — Agentic AI for Predictive Maintenance

## 1. Objectif du projet

Construire un système agentique capable d'analyser les observations
d'un moteur d'avion, de mobiliser des outils de calcul et une
documentation technique, puis de proposer une décision argumentée
de surveillance ou d'inspection.

Le système doit pouvoir répondre à cette question :

> Avec les informations disponibles jusqu'au vol t, observe-t-on
> une évolution préoccupante ? Quelles causes sont plausibles et
> quelle vérification recommander ?

La première étape porte sur la détection, l'analyse et la demande
d'inspection. Une extension pourra traiter la stratégie de maintenance
lorsque les outils et scénarios correspondants seront disponibles.

## 2. Ce qui est fourni

- Des trajectoires synthétiques d'observations moteur en cruise.
- Un MLP d'inversion préentraîné, avec normalisation intégrée.
- Une brique de calcul de marge thermique simplifiée.
- Une base de connaissances dans `doc/`.
- Un notebook de prise en main dans `notebooks/`.

Trois situations sont considérées : vieillissement progressif,
encrassement compresseur et dérive de capteur. Leur connaissance
ne donne pas accès au scénario réel de chaque cas à analyser.

| Brique | Fonction |
|---|---|
| Lecture | `get_measure(trajectory_id, timestep=None)` |
| Inversion | `estimation_indicateurs_mlp(observations)` |
| Marge thermique | `marge_EGT(observations, temperature_limite, capteur="LPT_Tin")` |

Le simulateur, un filtre de Kalman et un algorithme de prédiction de RUL ne font pas encore partie des
briques agentiques de cette version. Ils seront éventuellement rajouté selon l'évolution du projet. La présence du package OpenDeckSMR
dans l'environnement pourra permetttre l'ajout d'une fonction d'appel au simulateur.

## 3. Ce qui est attendu de vous

### Concevoir le système

Définir comment l'agent accède à la documentation, choisit les outils,
exploite l'historique et construit sa conclusion.

Un premier agent unique est suffisant ; une architecture multi-agent pourra être envisagée en fin de projet et devra être justifiée

### Produire des décisions argumentées

Pour chaque analyse, fournir :

- le moteur, l'instant de décision et la période examinée ;
- les observations et calculs sur lesquels repose la conclusion ;
- une hypothèse principale et les alternatives pertinentes ;
- une recommandation de surveillance, d'inspection ou de vérification
  de capteur ;
- les limites et informations complémentaires nécessaires.

Le système doit pouvoir répondre « informations insuffisantes ».
Il ne doit pas convertir une sortie d'algorithme ou une information en diagnostic certain.

### Évaluer l'apport de l'agent

Comparer le système à une chaîne fixe utilisant les mêmes données
et outils : par exemple une surveillance de marge thermique avec une
règle de persistance, dont les paramètres sont réglés sur les données
de développement/validation.

Distinguer au moins :

1. Une baseline sans LLM.
2. Un agent simple disposant des outils et documents.
3. Votre proposition et les améliorations que vous souhaitez tester.

Le projet ne consiste pas uniquement à produire un texte convaincant :
il faut mesurer si les décisions sont plus pertinentes, mieux
justifiées ou obtenues plus efficacement.

### Améliorations possibles

Vous pouvez ajouter une analyse de tendance, une détection de rupture,
une vérification de cohérence ou une nouvelle méthode d'estimation.

Mesurer l'apport de chaque ajout. Un entraînement de LLM n'est pas requis.

Ces briques seront ajouter sous forme de fonction à appeler pour l'agent et ajouté dans des fichiers .py dans src/ensai_agentic_student/tools

## 4. Organisation du dépôt

| Emplacement | Contenu |
|---|---|
| `src/ensai_agentic_student/tools/` | Briques métier à appeler |
| `src/ensai_agentic_student/mlp_inverse.py` | Classe et chargement du MLP |
| `models/best_model.pt` | Poids et scalers du modèle |
| `data/trajectories/` | Données disponibles dans votre installation |
| `doc/` | Connaissances utilisables par les agents |
| `notebooks/` | Prise en main et exploration |

`doc/` est une ressource pour les agents. Le présent README décrit
le travail et les choix d'implémentation destinés aux étudiants.

## 5. Installation et premier appel

Environnement de référence : Linux, Python 3.11, `uv`.

Les commandes suivantes supposent un accès réseau pour télécharger
les dépendances. Un nœud de calcul hors ligne nécessite un environnement
préparé en amont.

Depuis votre clone du dépôt :

```bash
cd ensai_agentic_student
uv sync

uv run python -c \
"from ensai_agentic_student.tools.data import get_measure; print('Import OK')"

uv run jupyter lab
```

Sélectionner le Python du `.venv` du dépôt comme kernel du notebook.

Ne pas copier un `.venv` provenant d'une autre machine. Les dépendances
et `uv.lock` doivent être versionnés ; `.venv` ne doit pas l'être.

Les fichiers de données et le checkpoint fournis doivent être présents
aux emplacements indiqués ci-dessus. Leur mode de téléchargement dépend
de la distribution remise par les encadrants ; ils ne sont pas
nécessairement récupérés par un simple clone Git.

Premier exemple Python :

```python
from ensai_agentic_student.tools.data import get_measure
from ensai_agentic_student.tools.estimation import estimation_indicateurs_mlp
from ensai_agentic_student.tools.marge_egt import marge_EGT

observations = get_measure(trajectory_id=1)

# Exemple d'une décision prise au vol 100 :
historique = observations.loc[observations["timestep"] <= 100]

indicateurs = estimation_indicateurs_mlp(historique)
marges = marge_EGT(historique, temperature_limite=1150.0)
```

Ne pas normaliser manuellement les données du MLP.
Consulter `doc/` pour les unités, domaines et limites d'interprétation.

## 6. Comment connecter un agent aux briques ?

Le LLM reçoit une mission, des documents et la description des fonctions
qu'il peut appeler.

Il propose un appel structuré ; le programme Python exécute la fonction
et lui renvoie son résultat. Le LLM peut alors appeler un autre outil
ou produire sa conclusion.

Les calculs sont réalisés par les briques Python, pas inventés par
le LLM. Les DataFrames sont convertis en JSON pour être transmis au modèle.

LangChain fournit une boucle de ce type avec `create_agent`.
Vous pouvez utiliser un autre framework ou écrire votre propre boucle.

Commencer par un seul agent et un accès direct aux documents.
Un système de recherche documentaire pourra être ajouté si son intérêt
est démontré.

### Exemple minimal entièrement local avec Ollama

Cet exemple utilise un modèle à poids ouverts sous licence Apache 2.0,
exécuté sur votre machine avec Ollama.

Aucune clé API et aucun service LLM payant ne sont nécessaires.
Le calcul mobilise néanmoins votre CPU/GPU et votre mémoire.

#### Préparer Ollama et les dépendances

Installer [Ollama](https://ollama.com/download/linux) selon la procédure
adaptée à votre machine.

Ollama est un programme distinct de l'environnement Python :
installer `langchain-ollama` seul ne suffit pas.

Depuis la racine du dépôt :

```bash
uv add "langchain>=1,<2" langchain-ollama
```


Vérifier que le serveur Ollama répond :

```bash
ollama list
```

Si aucun serveur n'est démarré, exécuter dans un autre terminal
et le laisser ouvert :

```bash
ollama serve
```

Ne pas lancer un second serveur si Ollama fonctionne déjà comme service.

Télécharger le modèle de départ puis sélectionner son nom :

```bash
ollama pull qwen3:8b
export AGENT_MODEL="qwen3:8b"
export LANGSMITH_TRACING=false
```

Les téléchargements initiaux nécessitent Internet. Une fois les
dépendances et les poids disponibles, l'inférence peut fonctionner
hors ligne.

Sur cluster, préparer les téléchargements sur une machine autorisée
et exécuter Ollama sur une ressource de calcul adaptée.

Dans cet exemple, Ollama et le script Python doivent tourner sur
la même machine ou le même nœud.

Les données et la documentation sont envoyées au serveur Ollama local
`http://localhost:11434`, pas à une API LLM hébergée.

#### Brancher les briques métier

Lire et étudier le code dans `examples/agent_minimal.py`, puis lancer depuis la racine :

```bash
uv run python examples/agent_minimal.py
```

Ce code est un exemple de raccordement, pas un système de diagnostic
validé. La syntaxe Python a été vérifiée ; l'exécution complète avec
les modèles locaux n'a pas été testée lors de la préparation du README.

Les outils exposés au LLM encapsulent les briques métier : il choisit
des intervalles, sans transférer lui-même des DataFrames d'un outil
à l'autre.

La limite de 30 instants réduit le volume des résultats et peut
être adaptée.

Dans votre version finale, traiter les erreurs d'outil, les limites
d'itérations et les contextes trop longs.

Le réglage `num_ctx=16384` est un point de départ : les documents,
descriptions d'outils, échanges, résultats et génération doivent tenir
dans le contexte.

Réduire les résultats ou sélectionner les documents si nécessaire.
Augmenter le contexte augmente la mémoire utilisée.

Une température de génération nulle ne garantit pas une reproductibilité
parfaite. Vérifier que le modèle appelle réellement les outils et ne
rédige pas simplement une imitation d'appel dans son texte.

## 7. Suggestions de modèles ouverts et gratuits à exécuter localement

Les trois modèles ci-dessous sont distribués avec leurs poids sous
licence Apache 2.0 et proposés avec prise en charge des outils dans Ollama.

L'ouverture des poids n'implique pas que toutes les données
d'entraînement soient publiques.

Aucun ne nécessite d'abonnement ni de facturation par appel pour
l'exécution locale décrite ici.

| Modèle | Identifiant Ollama | Taille | Licence | Usage proposé |
|---|---|---|---|---|
| Qwen3 8B | `qwen3:8b` | 8 milliards de paramètres | Apache 2.0 | Point de départ de l'exemple |
| IBM Granite 3.3 8B | `granite3.3:8b` | Environ 8 milliards | Apache 2.0 | Comparer une autre famille sur les mêmes outils et documents |
| Mistral NeMo 12B Instruct | `mistral-nemo:12b` | 12 milliards | Apache 2.0 | Comparer un modèle plus volumineux si les ressources le permettent |

Ce choix ne constitue pas un classement de performances sur le projet.
La capacité à appeler des outils ne garantit pas la pertinence du diagnostic.

### Changer de modèle sans changer les outils

Pour utiliser Granite :

```bash
ollama pull granite3.3:8b
export AGENT_MODEL="granite3.3:8b"
uv run python examples/agent_minimal.py
```

Pour utiliser Mistral NeMo :

```bash
ollama pull mistral-nemo:12b
export AGENT_MODEL="mistral-nemo:12b"
uv run python examples/agent_minimal.py
```

Un seul modèle est nécessaire pour démarrer. Vous n'avez pas besoin
de télécharger les trois immédiatement.

### Ressources et comparaison

- Un GPU peut accélérer l'inférence ; une exécution CPU peut être lente.
- Le besoin mémoire dépend du modèle, de la quantification, du contexte
  et de la concurrence. La taille du téléchargement ne correspond pas
  à la mémoire totale.
- Tester d'abord un cas court avant de lancer une campagne d'évaluation.
- Consigner modèle, version/digest, quantification, versions
  Ollama/LangChain, taille de contexte et paramètres de génération
  pour reproduire les résultats.
- Comparer sur les mêmes trajectoires, instants de décision, outils
  et budgets d'appels, en documentant les adaptations propres
  à chaque modèle.

## 8. Protocole d'évaluation

- Séparer les ensembles par trajectoire entière.
- Régler prompts, seuils et architecture sur développement/validation.
- Conserver un test final indépendant et figer la configuration
  avant son utilisation.
- Pour une décision au temps t, ne jamais exploiter les observations
  futures.
- Ne jamais donner à l'agent les vrais états, scénarios ou dates
  d'événement du cas testé.
- Les références cachées restent accessibles uniquement à l'évaluateur.

La fonction de lecture ne renvoie que les observations, mais cela
ne protège pas le pickle source si l'agent dispose d'un accès libre
au disque. Limiter ses ressources aux outils et aux documents autorisés.

Comparer, lorsque les annotations nécessaires sont disponibles :

- les fausses alertes sur les cas de référence ;
- la détection des anomalies ;
- le délai de détection ;
- la pertinence de l'inspection proposée ;
- la proportion de conclusions insuffisamment étayées.

Les critères de référence doivent être définis avec les encadrants :
une étiquette de scénario ne suffit pas à déterminer l'action correcte
à chaque instant.

Mesurer aussi le nombre d'appels d'outils, la latence, la consommation
mémoire et la stabilité sur plusieurs exécutions.

Étudier quelques échecs en détail. Une explication plausible n'est pas
une preuve d'exactitude.

## 9. Livrables attendus

- Un code installable, documenté et reproductible.
- Une description de l'architecture et des choix de modèles,
  outils et documents.
- Une baseline déterministe et une comparaison expérimentale.
- Des traces d'exécution montrant les observations utilisées,
  appels d'outils et décisions.
- Une analyse des limites, erreurs et améliorations possibles.
- Une démonstration sur des trajectoires réservées à l'évaluation.

## 10. Références techniques

- [Base de connaissances du projet](docs/README.md)
- [OpenDeckSMR](https://github.com/OpenDeckLab/OpenDeckSMR)
- [Agents LangChain](https://docs.langchain.com/oss/python/langchain/agents)
- [Intégration ChatOllama](https://docs.langchain.com/oss/python/integrations/chat/ollama)
- [Installation Ollama sur Linux](https://ollama.com/download/linux)
- [Appels d'outils Ollama](https://docs.ollama.com/capabilities/tool-calling)
- [Qwen3 8B : modèle et licence](https://huggingface.co/Qwen/Qwen3-8B)
- [Granite 3.3 8B : modèle et licence](https://huggingface.co/ibm-granite/granite-3.3-8b-instruct)
- [Mistral NeMo Instruct : modèle et licence](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407)
- [Qwen3 dans Ollama](https://ollama.com/library/qwen3:8b)
- [Granite dans Ollama](https://ollama.com/library/granite3.3:8b)
- [Mistral NeMo dans Ollama](https://ollama.com/library/mistral-nemo:12b)
