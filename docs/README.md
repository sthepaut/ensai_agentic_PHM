# Agent knowledge base

These documents support the interpretation of observations and tools
in the ENSAI predictive maintenance project.

## Documents

- [Mission and scope](01_objectif_et_perimetre.md)
- [Measurements and operating conditions](02_mesures_et_conditions.md)
- [Health indicators](03_indicateurs_de_sante.md)
- [Scenarios and diagnosis](04_scenarios_et_diagnostic.md)
- [Available tools](05_outils_disponibles.md)
- [Decisions and justification](06_decisions_et_justification.md)

## Conventions

Column names match those used in the code. Educational examples
and thresholds are not manufacturer instructions.

General knowledge about the scenarios may be used.
A trajectory's scenario labels, true states, and hidden events
are not authorized observations.

At a given decision timestep, use only observations available up to
that timestep. Identifiers are used to retrieve data, never to infer
the scenario.

Initial version: observation retrieval, MLP inversion, and thermal
margin calculation. Do not assume that Kalman filtering, RUL estimation,
or maintenance actions are available.

## Sources and scope

Sensor, operating condition, and state definitions are based on OpenDeckSMR:

- https://github.com/OpenDeckLab/OpenDeckSMR/blob/main/doc/doc.md
- https://github.com/OpenDeckLab/OpenDeckSMR/blob/main/src/odsmr/sensors.py

Tool signatures and educational assumptions are specific to this project.
If changes occur, the code and configuration actually provided
are the authoritative reference.