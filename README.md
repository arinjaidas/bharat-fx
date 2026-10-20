![BHARAT-FX](assets/header.svg)

# BHARAT-FX

External-sector accounting, vintage selection, relative stress diagnostics and conditional reserve scenarios with a synthetic public demo.

**Research question:** How do current-account positions, financing composition and reserve buffers interact under external-sector stress?

**Public edition:** New runnable synthetic methods demonstration and detailed research-scope documentation. Original archive remains separate.

**10 functional checks passed locally**, plus a complete demonstration run.

See [the original research scope](docs/RESEARCH_SCOPE.md) for the distinction between the broader collaborative project and this public implementation.

Read the [original research publication status](docs/ORIGINAL_RESEARCH_STATUS.md) for the larger held source and data bundle.

## What you can inspect

- Validate consecutive quarterly inputs and reconcile current-account financing with reserve transactions.
- Separate valuation changes from reserve transactions.
- Select the latest release available at an explicit as-of date using a standalone vintage helper.
- Construct a relative stress diagnostic using scaling fitted to an initial calibration window.
- Simulate conditional reserve paths with shared random draws across baseline, funding-stress and assumed-inflow-offset scenarios.

## Results preview

All values below are synthetic or illustrative workflow results.

![BHARAT-FX results preview](demo_output/reserve_scenarios.svg)

| Assumed scenario | Quarter-8 p05 | Quarter-8 median | Quarter-8 p95 |
| --- | --- | --- | --- |
| baseline | 877738 | 887464 | 897150 |
| funding_stress | 717738 | 727464 | 737150 |
| funding_stress_with_inflow_offset | 765738 | 775464 | 785150 |

Each scenario uses 4,000 paths over eight quarters. The maximum accounting residual in the generated history is 3.64e-12, consistent with floating-point rounding. Scenario shifts are assumptions and the bands are model quantiles.

## Run the example

Use Python 3.12. From this project's directory:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -v
python public_demo.py --demo --output demo_output
```

For an isolated environment, run `python -m venv .venv` first. Activate it with `source .venv/bin/activate` on Linux/macOS or `.venv\Scripts\activate` on Windows. The standard example runs offline after dependencies are installed.

The [notebook walkthrough](notebooks/01_results_walkthrough.ipynb) explains the saved outputs. Exact command-line options appear in [CLI.txt](docs/CLI.txt).

## Documentation

| Guide | What it covers |
| --- | --- |
| [Methods](docs/METHODS.md) | Formulas, assumptions and interpretation |
| [Data dictionary](docs/DATA_DICTIONARY.md) | Variables, units and validation rules |
| [Results](docs/RESULTS.md) | Actual bundled output and how to read it |
| [Reproducibility](REPRODUCIBILITY.md) | Commands, checks and the recorded environment |
| [Provenance and attribution](docs/PROVENANCE.md) | Historical context, reconstruction and contribution |
| [Roadmap](docs/ROADMAP.md) | Specific extensions, with unfinished work labelled |
| [References](docs/REFERENCES.md) | Method documentation and source links |

## Limits of interpretation

- Synthetic data and assumed flow shifts do not estimate India's actual policy response.
- The stress diagnostic is a relative index, not a crisis probability or exchange-rate forecast.
- The vintage helper is demonstrated separately; the main example is not a complete real-time vintage database.
- The original advanced pipeline was not rerun end to end. Shock Lab remains a separately documented extension.

## Contribution and research context

GIPE Group 5 research framework covering data ingestion, econometrics, regimes, Bayesian/state-space methods and scenario analysis.

Portfolio owner: Arinjai Das. Original research context: Group 5, MA Economics, GIPE. The public example was newly implemented with ChatGPT assistance and does not redistribute or certify the original 00-19 research pipeline.

**Skills demonstrated:** Python, macroeconomic accounting, balance of payments, data vintages, scenario simulation, external-sector research.

[Portfolio](https://github.com/arinjaidas/My-Projects) · [GitHub profile](https://github.com/arinjaidas)
