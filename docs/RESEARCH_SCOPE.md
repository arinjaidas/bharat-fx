# Original research scope and public implementation

The documented original BHARAT-FX project contains a broader 00-19 research pipeline. This page explains its structure without distributing the original source archive, research datasets or unpublished result tables.

| Stages | Documented purpose |
| --- | --- |
| 00-02 | System audit, project bootstrap and a 142-series registry |
| 03-04 | Data ingestion and frequency alignment |
| 05-08 | RBI intake, parsing, historical audit and historical parsing |
| 09-10 | Master data lake, feature construction and validation |
| 11-13 | Model comparisons, regime/HMM analysis and econometric core |
| 14 | Bayesian and state-space methods |
| 15 | Structural RBI and balance-of-payments accounting engine |
| 16-17 | Monte Carlo scenarios and counterfactual policy analysis |
| 18-19 | Ensemble stress diagnostic and final research assembly |

The broader work includes ECM/ARDL/VAR comparisons, capital-flow composition, reserve/intervention accounting and the interpretation of external pressure. Selected original accounting, transition-matrix and syntax checks were performed locally. The advanced original pipeline was not rerun end to end for this release.

## Executable public scope

The new public_demo.py covers quarterly funding accounting, separate valuation changes, an as-of vintage helper, a relative diagnostic and conditional reserve scenarios. Its ten checks apply to that new example. They do not certify all stages in the original pipeline.

## Shock Lab extension

The history records a successful S0 bootstrap and an S1 scaffold. Later stages and end-to-end completion are not verified. Shock Lab is therefore documented as an extension in progress, rather than promoted as a completed independent product.

## Research credit

Original research context: Group 5, MA Economics, GIPE. Portfolio owner: Arinjai Das. Any future original research release must preserve collaborator and data-source attribution.
