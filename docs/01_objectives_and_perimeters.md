# Mission and scope

## Mission

Analyze the available engine history to identify abnormal changes,
formulate hypotheses, and recommend monitoring or inspection supported
by the available evidence.

The system provides decision support for educational purposes. It does
not certify the airworthiness or safety of a real engine.

## Questions to address

- Are the observations usable?
- Is the observed evolution consistent with gradual aging?
- Is there evidence of an engine anomaly or sensor drift?
- Which checks could help distinguish between the hypotheses?
- What action is proportionate to the available evidence?

## Data and domain

A trajectory represents an engine observed over successive flights.
A timestep corresponds to one observation during cruise, not one second
or one operating hour.

The data come from successive steady-state OpenDeckSMR calculations.
The sequence of states is defined by a synthetic scenario;
it is not a full dynamic simulation of the engine.

The first version covers only CR, with the fan and booster at nominal
health settings and six variable health parameters for the HP compressor
and the HP/LP turbines.

## Limitations

The aging laws are not calibrated against an industrial service life.
An alert does not automatically establish its cause.

The current tools do not estimate remaining useful life (RUL) or simulate
washing or repairs. Do not produce a numerical remaining-life estimate
based on the length of a data file.

The analysis must allow a conclusion of insufficient information,
rather than forcing the assignment of a scenario.