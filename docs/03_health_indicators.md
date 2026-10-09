# Health indicators

## Meaning

The indicators are deviations from nominal settings that modify
component maps in OpenDeckSMR:

- `mapEff` relates to map efficiency.
- `mapWc` relates to map corrected flow.
- Zero corresponds to the nominal setting.
- A negative or positive value indicates the direction of the map deviation.

These parameters are neither failure probabilities, remaining useful
life (RUL), nor direct sensor measurements.

Do not automatically interpret a delta of -0.02 as a loss of two
percentage points in physical efficiency: its effect depends on the
map convention and the operating point.

## Six MLP outputs

| Column | Component and parameter | Training range |
|---|---|---|
| deg_CmpH_s_mapEff_in | HP compressor efficiency | [-0.05, 0] |
| deg_CmpH_s_mapWc_in | HP compressor corrected flow | [-0.05, 0.03] |
| deg_TrbH_s_mapEff_in | HP turbine efficiency | [-0.05, 0] |
| deg_TrbH_s_mapWc_in | HP turbine corrected flow | [-0.05, 0.05] |
| deg_TrbL_s_mapEff_in | LP turbine efficiency | [-0.05, 0] |
| deg_TrbL_s_mapWc_in | LP turbine corrected flow | [-0.05, 0.05] |

The four fan and booster parameters are fixed at zero in this version.
They are not estimated.

The bounds above describe the training domain:
they are not failure thresholds.

A positive map corrected-flow deviation does not automatically indicate
an improvement in health.

## Interpreting the estimates

The MLP processes each observation independently, without using its
history. It normalizes the inputs and restores the outputs to their
original scale.

Accuracy varies across parameters. The initial evaluation shows
substantially better performance on the two HPC parameters and HPT
corrected flow than on HPT/LPT efficiencies and LPT corrected flow.

The outputs are not artificially bounded and may fall outside the
training range. Such a result should be reported as a potential
limitation of the estimate, not automatically interpreted as a severe
fault.

Examine whether changes persist and whether they are consistent with
the measurements and operating conditions.

A sensor bias may be incorrectly interpreted as a change in health.
This MLP does not provide calibrated uncertainty estimates.