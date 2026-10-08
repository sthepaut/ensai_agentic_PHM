import os
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

from ensai_agentic_student.tools.data import get_measure
from ensai_agentic_student.tools.estimation import estimation_indicateurs_mlp
from ensai_agentic_student.tools.marge_egt import marge_EGT

ROOT = Path(__file__).resolve().parents[1]
TRAJECTORY_ID = 1
INSTANT_DECISION = 100

# L'agent ne reçoit que des observations passées.
observations = get_measure(TRAJECTORY_ID)
observations = observations.loc[
    observations["timestep"] <= INSTANT_DECISION
].copy()


def fenetre(debut: int, fin: int):
    if not 0 <= debut <= fin <= INSTANT_DECISION:
        raise ValueError("Fenêtre hors de l'historique autorisé.")

    if fin - debut >= 30:
        raise ValueError("Demander au maximum 30 instants par appel.")

    lignes = observations.loc[
        observations["timestep"].between(debut, fin)
    ].copy()

    if lignes.empty:
        raise ValueError("Aucune observation dans cette fenêtre.")

    return lignes


@tool
def lire_observations(debut: int, fin: int) -> str:
    """Lire mesures, conditions et qualité entre deux instants inclus, 30 maximum."""
    colonnes = [
        "timestep", "DTAMB", "ALT", "MACH", "COMMAND",
        "HPC_Tout", "HP_Nmech", "HPC_Tin", "LPT_Tin",
        "Fuel_flow", "HPC_Pout_st", "usable",
    ]
    return fenetre(debut, fin)[colonnes].to_json(orient="records")


@tool
def estimer_sante(debut: int, fin: int) -> str:
    """Estimer les six deltas de santé sur une fenêtre passée de 30 instants maximum."""
    donnees = fenetre(debut, fin)
    resultat = estimation_indicateurs_mlp(donnees)

    resultat = resultat.assign(
        timestep=donnees["timestep"].to_numpy()
    )

    return resultat.to_json(orient="records")


@tool
def calculer_marge(debut: int, fin: int) -> str:
    """Calculer la marge thermique pédagogique à 1150 K, sur 30 instants maximum."""
    resultat = marge_EGT(
        fenetre(debut, fin),
        temperature_limite=1150.0,
    )
    return resultat.to_json(orient="records")


fichiers = sorted((ROOT / "doc").glob("*.md"))

if not fichiers:
    raise FileNotFoundError("Aucune documentation dans doc/.")

connaissances = "\n\n".join(
    f"DOCUMENT : {p.name}\n{p.read_text(encoding='utf-8')}"
    for p in fichiers
)

modele = ChatOllama(
    model=os.environ.get("AGENT_MODEL", "qwen3:8b"),
    base_url="http://localhost:11434",
    temperature=0,
    num_ctx=16384,
    validate_model_on_init=True,
)

agent = create_agent(
    model=modele,
    tools=[
        lire_observations,
        estimer_sante,
        calculer_marge,
    ],
    system_prompt=(
        "Tu es un assistant d'analyse moteur pour un exercice pédagogique. "
        f"La date de décision est le timestep {INSTANT_DECISION}. "
        "Utilise les outils pour obtenir les faits. "
        "Les fenêtres contiennent au maximum 30 instants, bornes incluses. "
        "Les outils exposés encapsulent les briques Python décrites dans doc/. "
        "Distingue constats, hypothèses et recommandations ; cite tes sources.\n\n"
        + connaissances
    ),
)

resultat = agent.invoke(
    {
        "messages": [{
            "role": "user",
            "content": (
                "Analyse l'évolution disponible du moteur. "
                "Compare au moins une fenêtre ancienne et une fenêtre récente. "
                "Justifie s'il faut poursuivre la surveillance ou demander "
                "une vérification. Explicite les ambiguïtés."
            ),
        }]
    },
    config={"recursion_limit": 20},
)

for message in resultat["messages"]:
    if getattr(message, "tool_calls", None):
        print("APPELS :", message.tool_calls)

    if message.type == "tool":
        print("RÉSULTAT OUTIL :", message.content)

print("CONCLUSION :", resultat["messages"][-1].content)