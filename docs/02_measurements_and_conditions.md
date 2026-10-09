# Measurements and operating conditions

## Sensors

| Column | Meaning | Unit |
|---|---|---|
| HPC_Tout | HP compressor outlet temperature | K |
| HP_Nmech | HP shaft rotational speed | rpm |
| HPC_Tin | HP compressor inlet temperature | K |
| LPT_Tin | LP turbine inlet temperature | K |
| Fuel_flow | Fuel flow rate | kg/s |
| HPC_Pout_st | HP compressor outlet static pressure | Pa |

These values are simulator outputs, potentially modified by a sensor
fault in the scenario. Do not confuse them with estimated health states.

## Known conditions

| Column | Meaning | Unit | Range in this version |
|---|---|---|---|
| DTAMB | Deviation from standard atmospheric temperature | K difference | 9 to 11 |
| ALT | Altitude | ft | 34,900 to 35,100 |
| MACH | Mach number | Dimensionless | 0.76 to 0.80 |
| COMMAND | Thrust command in CR, as defined by the OpenDeckSMR interface | lbf | 24,900 to 25,100 |
| phase | Operating phase | Text | CR |

A change in a measurement may result from a change in operating conditions.
Compare observations under similar conditions or use a tool that takes
these conditions as inputs.

Including operating conditions in the MLP does not guarantee perfect
compensation for their effects.

## Time and quality

- `trajectory_id` identifies the engine or trajectory; it must not be used
  as a diagnostic clue.
- `timestep` orders the observations. Preserve the actual gaps between
  timesteps.
- `usable` indicates that an observation passes the simulation quality
  checks.
- `Convergence` describes the simulator's numerical outcome, not the
  engine's mechanical condition.
- A `NaN` represents a missing or unusable value, never a nominal value.

Rejected observations must remain gaps in time-series analyses.
State when missing data prevent a conclusion.

A biased sensor reading can remain finite and be marked as `usable`.

## EGT proxy

Physically, `LPT_Tin` is the LP turbine inlet temperature.
The project uses it as an EGT proxy for educational purposes.
This convention does not make the two temperatures physically equivalent.

The educational limit of 1,150 K and the margins calculated from it
are not manufacturer limits.

A temperature difference of 1 K has the same magnitude as a difference
of 1 °C; do not confuse absolute temperatures with temperature differences.