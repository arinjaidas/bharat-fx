# Methods

## Funding convention

The public example uses positive current-account surpluses, positive net non-reserve financial inflows and positive reserve accumulation. With the capital account and errors/omissions set to zero in the simplified example, `reserve_transactions = current_account + fdi + portfolio + other`. These funding signs should not be confused with a complete BPM presentation of the financial account.

`reserves_close = reserves_open + reserve_transactions + valuation`. Valuation affects the reserve stock but is not reclassified as a current-account or financial-flow transaction. The synthetic generator links each subsequent opening stock to the previous closing stock.

## Relative diagnostic and vintages

The diagnostic averages standardised current-account deficit/GDP, portfolio outflow/GDP, reserve transaction draw/opening reserves and INR depreciation. Larger values indicate greater pressure under these chosen orientations. Means and scales are fitted to the initial 40 rows. Those calibration-period scores are in-sample descriptions. Later scores use the fixed calibration parameters, but current-vintage input data would still make the exercise retrospective.

The standalone vintage helper chooses the latest release at or before an as-of timestamp for each series and quarter. Duplicate vintage keys are rejected. This helper is not represented as a complete vintage-safe version of the original research pipeline.

## Conditional scenarios

Four funding components and valuation are simulated jointly from a covariance estimated on the latest 20 example observations. A fixed seed supplies common random draws to all scenarios. Funding stress shifts the current-account mean by -8,000 and portfolio inflows by -12,000 illustrative USD million per quarter. The assumed-offset case changes the portfolio shift to -6,000. These are assumed mean shifts, not estimated policy effects. The 5th to 95th percentile bands describe the simulated model distribution, not validated coverage for India.
