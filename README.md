# ENSAI — Agentic AI for Predictive Maintenance

## 1. Project objective

Build an agentic system capable of analysing observations from an aircraft engine, using computational tools and technical documentation, and providing a justified monitoring or inspection recommendation.

The system should be able to answer the following question:

> Based on the information available up to flight t, is there evidence of a concerning trend? What are the plausible causes, and what checks should be recommended?

The first stage focuses on detection, analysis and inspection recommendations. An extension may address maintenance strategies once the corresponding tools and scenarios become available.

## 2. What is provided

- Synthetic trajectories of engine observations under cruise conditions.
- A pretrained inverse MLP with built-in normalisation.
- A tool for computing a simplified thermal margin.
- A knowledge base in `doc/`.
- An introductory notebook in `notebooks/`.

Three situations are considered: gradual ageing, compressor fouling and sensor drift. Knowing these possible scenarios does not reveal the actual scenario associated with each case to be analysed.

| Tool | Function |
|---|---|
| Data retrieval | `get_measure(trajectory_id, timestep=None)` |
| Inverse estimation | `estimation_indicateurs_mlp(observations)` |
| Thermal margin | `marge_EGT(observations, temperature_limite, capteur="LPT_Tin")` |

The simulator, a Kalman filter and a Remaining Useful Life (RUL) prediction algorithm are not yet included among the agent tools in this version. They may be added as the project develops. The OpenDeckSMR package available in the environment can support the addition of a function that calls the simulator.

## 3. What is expected of you

### Design the system

Define how the agent accesses the documentation, selects tools, uses historical observations and reaches its conclusions.

A single agent is sufficient initially. A multi-agent architecture may be considered towards the end of the project and must be justified.

### Produce justified decisions

For each analysis, provide:

- the engine, decision time and period examined;
- the observations and calculations supporting the conclusion;
- a primary hypothesis and relevant alternatives;
- a recommendation for monitoring, inspection or sensor verification;
- the limitations and additional information required.

The system must be able to answer “insufficient information”. It must not treat an algorithm's output or a piece of information as a definitive diagnosis.

### Evaluate the agent's contribution

Compare the system against a fixed pipeline using the same data and tools. For example, this could be thermal-margin monitoring with a persistence rule whose parameters are tuned on the development/validation data.

Include at least:

1. A baseline without an LLM.
2. A simple agent with access to the tools and documents.
3. Your proposed approach and the improvements you wish to test.

The project is not just about producing convincing text: you must assess whether decisions are more appropriate, better justified or obtained more efficiently.

### Possible improvements

You may add trend analysis, change-point detection, consistency checks or a new estimation method.

Measure the contribution of each addition. Training an LLM is not required.

These additional tools should be implemented as functions that the agent can call, in `.py` files under `src/ensai_agentic_student/tools/`.

## 4. Repository structure

| Location | Contents |
|---|---|
| `src/ensai_agentic_student/tools/` | Callable domain-specific tools |
| `src/ensai_agentic_student/mlp_inverse.py` | MLP class and loading function |
| `models/best_model.pt` | Model weights and scalers |
| `data/trajectories/` | Data available in your installation |
| `doc/` | Knowledge available to the agents |
| `notebooks/` | Getting started and data exploration |

The `doc/` directory is a resource for the agents. This README describes the assignment and implementation choices for students.

## 5. Installation and first call

Reference environment: Linux, Python 3.11, `uv`.

The following commands require network access to download dependencies. An offline compute node requires an environment prepared in advance.

From your local clone of the repository:

```bash
cd ensai_agentic_student
uv sync

uv run python -c \
"from ensai_agentic_student.tools.data import get_measure; print('Import OK')"

uv run jupyter lab
```

Select the Python interpreter from the repository's `.venv` as the notebook kernel.

Do not copy a `.venv` from another machine. Dependency declarations and `uv.lock` must be tracked in version control; `.venv` must not.

The supplied data files and checkpoint must be present at the locations listed above. How they are downloaded depends on the distribution provided by the supervisors; cloning the Git repository may not retrieve them automatically.

First Python example:

```python
from ensai_agentic_student.tools.data import get_measure
from ensai_agentic_student.tools.estimation import estimation_indicateurs_mlp
from ensai_agentic_student.tools.marge_egt import marge_EGT

observations = get_measure(trajectory_id=1)

# Example of a decision made at flight 100:
historique = observations.loc[observations["timestep"] <= 100]

indicateurs = estimation_indicateurs_mlp(historique)
marges = marge_EGT(historique, temperature_limite=1150.0)
```

Do not manually normalise the MLP inputs. Refer to `doc/` for units, operating ranges and interpretation limits.

## 6. How do you connect an agent to the tools?

The LLM receives a task, documents and descriptions of the functions it can call.

It proposes a structured call; the Python program executes the function and returns its result. The LLM can then call another tool or produce its conclusion.

Calculations are performed by the Python tools, not invented by the LLM. DataFrames are converted to JSON before being passed to the model.

LangChain provides this type of loop through `create_agent`. You may use another framework or implement your own loop.

Start with a single agent and direct access to the documents. A document retrieval system may be added if its benefits are demonstrated.

### Fully local minimal example with Ollama

This example uses an open-weight model released under the Apache 2.0 licence, running on your machine through Ollama.

No API key or paid LLM service is required. Computation still uses your CPU/GPU and memory.

#### Set up Ollama and the dependencies

Install [Ollama](https://ollama.com/download/linux) using the procedure appropriate for your machine.

Ollama is a separate program from the Python environment: installing `langchain-ollama` alone is not enough.

From the repository root:

```bash
uv add "langchain>=1,<2" langchain-ollama
```

Check that the Ollama server responds:

```bash
ollama list
```

If no server is running, execute the following in another terminal and leave it open:

```bash
ollama serve
```

Do not start a second server if Ollama is already running as a service.

Download the initial model and select its name:

```bash
ollama pull qwen3:8b
export AGENT_MODEL="qwen3:8b"
export LANGSMITH_TRACING=false
```

The initial downloads require Internet access. Once the dependencies and weights are available, inference can run offline.

On a cluster, prepare the downloads on an authorised machine and run Ollama on an appropriate compute resource.

In this example, Ollama and the Python script must run on the same machine or node.

Data and documentation are sent to the local Ollama server at `http://localhost:11434`, not to a hosted LLM API.

#### Connect the domain-specific tools

Read and study the code in `examples/agent_minimal.py`, then run it from the repository root:

```bash
uv run python examples/agent_minimal.py
```

This code is an integration example, not a validated diagnostic system. Its Python syntax has been checked; full execution with the local models was not tested when this README was prepared.

The tools exposed to the LLM wrap the domain-specific functions: the LLM selects intervals without having to transfer DataFrames between tools itself.

The limit of 30 time steps reduces the size of the results and can be adjusted.

In your final version, handle tool errors, iteration limits and contexts that become too long.

The `num_ctx=16384` setting is a starting point: the documents, tool descriptions, conversation, results and generated output must fit within the context window.

Reduce the results or select relevant documents if necessary. Increasing the context window increases memory usage.

A generation temperature of zero does not guarantee perfect reproducibility. Check that the model actually calls the tools rather than merely generating text that imitates a tool call.

## 7. Suggested open models for free local inference

The three models below are distributed with their weights under the Apache 2.0 licence and are available with tool-calling support in Ollama.

Open weights do not imply that all training data is publicly available.

None requires a subscription or per-call charges for the local execution described here.

| Model | Ollama identifier | Size | Licence | Suggested use |
|---|---|---|---|---|
| Qwen3 8B | `qwen3:8b` | 8 billion parameters | Apache 2.0 | Starting point for the example |
| IBM Granite 3.3 8B | `granite3.3:8b` | Approximately 8 billion parameters | Apache 2.0 | Compare another model family using the same tools and documents |
| Mistral NeMo 12B Instruct | `mistral-nemo:12b` | 12 billion parameters | Apache 2.0 | Compare a larger model if resources allow |

This selection is not a performance ranking for this project. The ability to call tools does not guarantee an appropriate diagnosis.

### Switch models without changing the tools

To use Granite:

```bash
ollama pull granite3.3:8b
export AGENT_MODEL="granite3.3:8b"
uv run python examples/agent_minimal.py
```

To use Mistral NeMo:

```bash
ollama pull mistral-nemo:12b
export AGENT_MODEL="mistral-nemo:12b"
uv run python examples/agent_minimal.py
```

Only one model is needed to get started. You do not need to download all three immediately.

### Resources and comparison

- A GPU can speed up inference; CPU execution may be slow.
- Memory requirements depend on the model, quantisation, context window and concurrency. Download size is not the same as total memory usage.
- Test a short case before launching an evaluation campaign.
- Record the model, version/digest, quantisation, Ollama/LangChain versions, context window size and generation settings to make results reproducible.
- Compare models using the same trajectories, decision times, tools and tool-call budgets, documenting any model-specific adjustments.

## 8. Evaluation protocol

- Split the datasets by entire trajectory.
- Tune prompts, thresholds and architecture using development/validation data.
- Keep an independent final test set and freeze the configuration before using it.
- For a decision at time t, never use future observations.
- Never provide the agent with the true health states, scenario labels or event times for the case being tested.
- Hidden reference information must remain accessible only to the evaluator.

The data-loading function returns only observations, but this does not protect the source pickle if the agent has unrestricted filesystem access. Restrict its resources to the authorised tools and documents.

Where the necessary annotations are available, compare:

- false alarms on reference cases;
- anomaly detection;
- detection delay;
- the appropriateness of the proposed inspection;
- the proportion of insufficiently supported conclusions.

Reference criteria must be defined with the supervisors: a scenario label alone is not enough to determine the correct action at every time step.

Also measure the number of tool calls, latency, memory usage and stability across multiple runs.

Examine several failures in detail. A plausible explanation is not proof of correctness.

## 9. Expected deliverables

- Installable, documented and reproducible code.
- A description of the architecture and the choices of models, tools and documents.
- A deterministic baseline and an experimental comparison.
- Execution traces showing the observations used, tool calls and decisions.
- An analysis of limitations, errors and possible improvements.
- A demonstration using trajectories reserved for evaluation.

## 10. Technical references

- [Project knowledge base](doc/README.md)
- [OpenDeckSMR](https://github.com/OpenDeckLab/OpenDeckSMR)
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents)
- [ChatOllama integration](https://docs.langchain.com/oss/python/integrations/chat/ollama)
- [Installing Ollama on Linux](https://ollama.com/download/linux)
- [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling)
- [Qwen3 8B: model and licence](https://huggingface.co/Qwen/Qwen3-8B)
- [Granite 3.3 8B: model and licence](https://huggingface.co/ibm-granite/granite-3.3-8b-instruct)
- [Mistral NeMo Instruct: model and licence](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407)
- [Qwen3 in Ollama](https://ollama.com/library/qwen3:8b)
- [Granite in Ollama](https://ollama.com/library/granite3.3:8b)
- [Mistral NeMo in Ollama](https://ollama.com/library/mistral-nemo:12b)