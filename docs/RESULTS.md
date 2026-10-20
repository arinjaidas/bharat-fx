# Results walkthrough

All values below are synthetic or illustrative workflow results.

| Assumed scenario | Quarter-8 p05 | Quarter-8 median | Quarter-8 p95 |
| --- | --- | --- | --- |
| baseline | 877738 | 887464 | 897150 |
| funding_stress | 717738 | 727464 | 737150 |
| funding_stress_with_inflow_offset | 765738 | 775464 | 785150 |

Each scenario uses 4,000 paths over eight quarters. The maximum accounting residual in the generated history is 3.64e-12, consistent with floating-point rounding. Scenario shifts are assumptions and the bands are model quantiles.

![Results preview](../demo_output/reserve_scenarios.svg)

The numerical files in [demo_output](../demo_output/) are the authoritative bundled artifacts. Re-run the entry command to reproduce the workflow. Figure metadata can differ across renders even when the underlying numerical example is unchanged.
