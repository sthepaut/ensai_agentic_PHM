# Available tools

The tools perform calculations. Diagnosis and recommendations must
be developed from their results.

## get_measure

Import: `ensai_agentic_student.tools.data`

Signature: `get_measure(trajectory_id, timestep=None, data_dir=None)`

- `trajectory_id`: integer identifying a trajectory.
- `timestep`: requested timestep; `None` returns the full trajectory.
- `data_dir`: optional directory, defaulting to `data/trajectories`
  in the repository.
- Output: a DataFrame of observations, containing one row if a specific
  timestep is requested.

The tool does not return `truth`, `event`, or `config`.
A missing file or timestep is a data access error, not an engine fault.

For a decision at time t, exclude all timesteps greater than t
before analysis. The tool can return a full trajectory and does not
apply this restriction automatically.

## estimation_indicateurs_mlp

Import: `ensai_agentic_student.tools.estimation`

Signature: `estimation_indicateurs_mlp(observations, model_path=None)`

- Input: a DataFrame containing the four operating conditions and
  the six raw measurements.
- Default model: `models/best_model.pt`.
- Output: a DataFrame of the six health indicators, aligned with
  the input index.

The model is loaded and then reused. Do not normalize the inputs
manually.

The intended version of this tool filters observations using `usable`
and reinserts rejected rows as `NaN`.

A missing required column or a non-finite value not flagged by `usable`
may cause an error. Do not invent a measurement to complete an input.

## marge_EGT

Import: `ensai_agentic_student.tools.marge_egt`

Signature: `marge_EGT(observations, temperature_limite, capteur="LPT_Tin")`

Calculation: `marge_EGT = temperature_limite - sensor temperature`.

Current educational setting: `temperature_limite=1150.0`, in K.
The argument remains mandatory: this value is not a hidden default
inside the tool.

Output: a DataFrame containing `timestep` if present,
`temperature_proxy_EGT`, and `marge_EGT`. Invalid observations produce
`NaN` values.

- Positive margin: below the chosen limit.
- Zero margin: the limit has been reached.
- Negative margin: the chosen limit has been exceeded.

Example: at 1,130 K, the margin is 20 K for a limit of 1,150 K.

This limit is provisional, shared across trajectories, and not based
on certification. Do not recalculate it for each engine or change it
to obtain a desired diagnosis.

The margin is not corrected for flight conditions. On its own, it
cannot identify a cause or determine remaining useful life.

## Tools not available in this version

The current interface does not provide tools for simulator calls,
Kalman filtering, RUL estimation, or maintenance actions.
Do not claim to have executed them.