# Decisions and justification

## Possible recommendations

- Continue monitoring: insufficient evidence to request an inspection.
- Intensify monitoring: a concerning trend requires confirmation.
- Request an engine inspection: persistent signs consistent with
  an engine anomaly.
- Request a sensor check: signs consistent with a measurement fault.
- Request additional data: observations are insufficient or unusable.

A recommendation does not execute any physical action.

## Evidence to examine

Consider data quality, operating conditions, the persistence of trends,
MLP limitations, and alternative explanations.

A threshold crossing is an observation, not the identification of a fault.
A positive margin does not rule out an anomaly.
A stable estimate does not establish that the engine is healthy.

There are currently no validated thresholds for slope, persistence,
or severity. Any proposed rule must be presented as a working assumption,
not as a manufacturer rule.

## Expected structure of a conclusion

1. Scope: engine, decision timestep, and period examined.
2. Quality: number of observations used and any missing data.
3. Findings: variables, values, units, and trends actually observed.
4. Main hypothesis: supporting evidence and evidence that weakens it.
5. Alternatives: other plausible explanations.
6. Recommendation: action and justification.
7. Additional information: what would help confirm or revise
   the conclusion.

Do not report a numerical diagnostic probability without a calibrated
method. Any qualitative assessment of confidence must be justified.

## Traceability

Identify the tools used and the relevant documentation references.
Clearly distinguish measurements, estimates, and hypotheses.
Use only information available at the decision timestep.

Do not access ground truth or hidden evaluation metadata.
Filtering within a function does not provide access control:
files reserved for evaluation are not authorized resources.

Do not treat multiple outputs derived from the same sensors
as multiple independent pieces of evidence.