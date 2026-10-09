# Scenarios and diagnosis

These scenarios describe situations to consider.
They do not assign a diagnosis to any trajectory.

## Gradual aging without a specific event

The engine gradually moves away from its nominal state, without any
specific additional degradation.

Consistent signs include slow, persistent trends, with no clear change
that cannot be explained by operating conditions.

“Normal aging” does not mean “parameters are exactly zero”
or “no limit can ever be reached.”

## HP compressor fouling

In this educational representation, fouling causes an additional gradual
decrease in the HP compressor efficiency and corrected-flow parameters.

Signs to look for include persistent joint changes in the HPC estimates,
potentially accompanied by a change in trend and consistent changes
in the measurements.

An increase in temperature or fuel consumption may support a hypothesis
depending on the context, but the direction of change is not a universal
rule. Do not diagnose fouling from a single measurement.

Possible checks include comparing periods with similar operating
conditions, examining both HPC parameters, and investigating whether
a sensor issue could explain the observations.

## Sensor drift

A sensor develops a bias that changes over time. Its readings may remain
numerically plausible, with `usable=True`.

Possible signs include an unusual trend in one measurement,
inconsistencies between measurements, or shifts in MLP estimates that
are difficult to explain through a consistent change in engine health.

The MLP uses sensor measurements: its outputs therefore do not provide
independent confirmation of a suspect measurement.

Likewise, the EGT margin and `LPT_Tin` contain the same thermal information.

Possible checks include examining other measurements and recommending
a consistency check or calibration of the suspect sensor.

## Ambiguities

The same observed effect may have several causes.
Multiple indicators derived from the same measurements may be wrong
together.

None of the signatures described here guarantees a unique diagnosis.
Retain alternative hypotheses and specify what information is missing.

Do not use file names, trajectory numbers, or generation metadata
to recover a hidden label.

## Maintenance

Compressor washing and its effects are not modeled in the current
version. Do not claim a washing benefit, an optimal maintenance interval,
or a validated RUL estimate.