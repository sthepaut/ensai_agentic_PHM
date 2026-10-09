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

# The agent only receives observations available at the decision timestep.
observations = get_measure(TRAJECTORY_ID)
observations = observations.loc[
    observations["timestep"] <= INSTANT_DECISION
].copy()


def fenetre(debut: int, fin: int):
    if not 0 <= debut <= fin <= INSTANT_DECISION:
        raise ValueError("Window outside the authorized history.")

    if fin - debut >= 30:
        raise ValueError("Request at most 30 timesteps per call.")

    lignes = observations.loc[
        observations["timestep"].between(debut, fin)
    ].copy()

    if lignes.empty:
        raise ValueError("No observations in this window.")

    return lignes


@tool
def lire_observations(debut: int, fin: int) -> str:
    """Read measurements, conditions, and quality for up to 30 timesteps, inclusive."""
    colonnes = [
        "timestep", "DTAMB", "ALT", "MACH", "COMMAND",
        "HPC_Tout", "HP_Nmech", "HPC_Tin", "LPT_Tin",
        "Fuel_flow", "HPC_Pout_st", "usable",
    ]
    return fenetre(debut, fin)[colonnes].to_json(orient="records")


@tool
def estimer_sante(debut: int, fin: int) -> str:
    """Estimate the six health deltas over a historical window of up to 30 timesteps."""
    donnees = fenetre(debut, fin)
    resultat = estimation_indicateurs_mlp(donnees)

    resultat = resultat.assign(
        timestep=donnees["timestep"].to_numpy()
    )

    return resultat.to_json(orient="records")


@tool
def calculer_marge(debut: int, fin: int) -> str:
    """Calculate the educational thermal margin against 1150 K for up to 30 timesteps."""
    resultat = marge_EGT(
        fenetre(debut, fin),
        temperature_limite=1150.0,
    )
    return resultat.to_json(orient="records")


fichiers = sorted((ROOT / "doc").glob("*.md"))

if not fichiers:
    raise FileNotFoundError("No documentation found in doc/.")

connaissances = "\n\n".join(
    f"DOCUMENT: {p.name}\n{p.read_text(encoding='utf-8')}"
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
        "You are an aircraft engine analysis assistant for an educational exercise. "
        f"The decision timestep is {INSTANT_DECISION}. "
        "Use the tools to obtain facts. "
        "Windows contain at most 30 timesteps, including both endpoints. "
        "The exposed tools wrap the Python functions described in doc/. "
        "Distinguish findings, hypotheses, and recommendations; cite your sources.\n\n"
        + connaissances
    ),
)

resultat = agent.invoke(
    {
        "messages": [{
            "role": "user",
            "content": (
                "Analyze the engine's evolution using the available history. "
                "Compare at least one earlier window and one recent window. "
                "Justify whether to continue monitoring or request a check. "
                "Explain any ambiguities."
            ),
        }]
    },
    config={"recursion_limit": 20},
)

for message in resultat["messages"]:
    if getattr(message, "tool_calls", None):
        print("TOOL CALLS:", message.tool_calls)

    if message.type == "tool":
        print("TOOL RESULT:", message.content)

print("CONCLUSION:", resultat["messages"][-1].content)