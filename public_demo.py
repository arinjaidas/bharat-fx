"""New synthetic public example of external-sector accounting and stress scenarios.

This module is not the original BHARAT-FX 00-19 research pipeline. Its
conventions and simplified scenarios are documented in docs/METHODS.md.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FLOWS = ['current_account', 'fdi', 'portfolio', 'other']
REQUIRED = FLOWS + ['valuation', 'reserves_open', 'gdp', 'usd_inr']


def validate(frame):
    data = frame.copy()
    data.index = pd.PeriodIndex(data.index, freq='Q')
    if data.index.has_duplicates or not data.index.is_monotonic_increasing:
        raise ValueError('Quarters must be unique and increasing.')
    if len(data) < 8 or not set(REQUIRED).issubset(data.columns):
        raise ValueError('At least eight quarters and all required fields are needed.')
    if not data.index.equals(pd.period_range(data.index[0], periods=len(data), freq='Q')):
        raise ValueError('Quarterly history must be consecutive.')
    data = data[REQUIRED].apply(pd.to_numeric, errors='raise')
    if not np.isfinite(data.to_numpy()).all():
        raise ValueError('Inputs must be finite and complete.')
    if (data[['reserves_open', 'gdp', 'usd_inr']] <= 0).any().any():
        raise ValueError('Opening reserves, GDP and USD/INR must be positive.')
    return data


def accounts(frame):
    """Positive capital flows are net inflows; reserves accumulation is positive."""
    out = validate(frame)
    out['net_financial_inflows'] = out[['fdi', 'portfolio', 'other']].sum(axis=1)
    out['reserve_transactions'] = out[FLOWS].sum(axis=1)
    out['reserves_close'] = out.reserves_open + out.reserve_transactions + out.valuation
    out['accounting_residual'] = out.reserve_transactions - out.current_account - out.net_financial_inflows
    out['ca_percent_gdp'] = 100 * out.current_account / out.gdp
    return out


def vintage_snapshot(records, as_of):
    """Select latest available release for each series/quarter, without future releases."""
    fields = ['series', 'quarter', 'released_at', 'value']
    if not set(fields).issubset(records):
        raise ValueError('Vintage input requires series, quarter, released_at and value.')
    data = records[fields].copy()
    data['quarter'] = pd.PeriodIndex(data.quarter, freq='Q')
    data['released_at'] = pd.to_datetime(data.released_at, utc=True, errors='raise')
    data['value'] = pd.to_numeric(data.value, errors='raise')
    if data[fields].isna().any().any() or not np.isfinite(data.value).all():
        raise ValueError('Vintage fields must be complete and finite.')
    if data.duplicated(['series', 'quarter', 'released_at']).any():
        raise ValueError('Duplicate vintage keys are ambiguous.')
    cutoff = pd.Timestamp(as_of)
    cutoff = cutoff.tz_localize('UTC') if cutoff.tzinfo is None else cutoff.tz_convert('UTC')
    return (data.loc[data.released_at <= cutoff].sort_values('released_at')
            .drop_duplicates(['series', 'quarter'], keep='last')
            .sort_values(['series', 'quarter']).reset_index(drop=True))


def stress_diagnostic(frame, calibration_rows=40):
    data = accounts(frame)
    if not isinstance(calibration_rows, int) or not 8 <= calibration_rows <= len(data):
        raise ValueError('Calibration requires between eight and all available rows.')
    features = pd.DataFrame({
        'ca_deficit_gdp': -100 * data.current_account / data.gdp,
        'portfolio_outflow_gdp': -100 * data.portfolio / data.gdp,
        'reserve_transaction_draw_percent': -100 * data.reserve_transactions / data.reserves_open,
        'inr_depreciation_percent': 100 * np.log(data.usd_inr).diff().fillna(0),
    }, index=data.index)
    calibration = features.iloc[:calibration_rows]
    center = calibration.mean()
    scale = calibration.std(ddof=1).mask(lambda x: x < 1e-12, 1.0)
    z = (features - center) / scale
    z['stress_diagnostic'] = z.mean(axis=1)
    params = pd.DataFrame({'mean': center, 'standard_deviation': scale})
    return features.join(z.add_prefix('z_')), params


def simulate_reserves(initial, means, covariance, horizon=8, paths=4000, seed=20261019, shock=None):
    means = np.asarray(means, dtype=float)
    cov = np.asarray(covariance, dtype=float)
    if means.shape != (5,) or cov.shape != (5, 5):
        raise ValueError('Use four flow components plus valuation, with a 5x5 covariance.')
    if not np.isfinite(initial) or initial <= 0 or not np.isfinite(means).all() or not np.isfinite(cov).all():
        raise ValueError('Finite inputs and positive initial reserves required.')
    if not np.allclose(cov, cov.T) or np.linalg.eigvalsh(cov).min() < -1e-8:
        raise ValueError('Covariance must be symmetric positive semidefinite.')
    if not isinstance(horizon, int) or not isinstance(paths, int) or horizon < 1 or paths < 2:
        raise ValueError('Positive horizon and at least two paths required.')
    shock = np.zeros(5) if shock is None else np.asarray(shock, dtype=float)
    if shock.shape != (5,) or not np.isfinite(shock).all():
        raise ValueError('Shock must contain five finite component shifts.')
    draws = np.random.default_rng(seed).multivariate_normal(np.zeros(5), cov, size=(paths, horizon), check_valid='raise')
    increments = (draws + means + shock).sum(axis=2)
    return initial + np.cumsum(increments, axis=1)


def synthetic_data(seed=20261019, n=104):
    if n < 8:
        raise ValueError('At least eight quarters required.')
    rng = np.random.default_rng(seed)
    index = pd.period_range('2000Q1', periods=n, freq='Q')
    common = rng.normal(size=n)
    frame = pd.DataFrame({
        'current_account': -5000 + 1800 * common + rng.normal(0, 1200, n),
        'fdi': 6500 + rng.normal(0, 900, n),
        'portfolio': 2000 - 2200 * common + rng.normal(0, 1800, n),
        'other': 1000 + rng.normal(0, 1200, n),
        'valuation': rng.normal(0, 1300, n),
        'gdp': np.linspace(300000, 750000, n),
        'usd_inr': 45 * np.exp(np.cumsum(.004 + .012 * common)),
    }, index=index)
    changes = frame[FLOWS + ['valuation']].sum(axis=1).to_numpy()
    frame['reserves_open'] = 350000 + np.r_[0, np.cumsum(changes[:-1])]
    return validate(frame)


def run(frame, output, synthetic=False):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    data = accounts(frame)
    diagnostic, params = stress_diagnostic(frame, min(40, len(frame)))
    data.to_csv(output / 'accounting.csv', index_label='quarter')
    diagnostic.to_csv(output / 'stress_diagnostic.csv', index_label='quarter')
    params.to_csv(output / 'calibration.csv', index_label='feature')
    recent = data[FLOWS + ['valuation']].iloc[-20:]
    means, cov = recent.mean().to_numpy(), recent.cov().to_numpy()
    scenarios = {'baseline': np.zeros(5), 'funding_stress': np.array([-8000, 0, -12000, 0, 0]),
                 'funding_stress_with_inflow_offset': np.array([-8000, 0, -6000, 0, 0])}
    summaries = []
    fig, ax = plt.subplots(figsize=(9, 5))
    for name, shock in scenarios.items():
        samples = simulate_reserves(data.reserves_close.iloc[-1], means, cov, shock=shock)
        low, median, high = np.quantile(samples, [.05, .5, .95], axis=0)
        ax.plot(np.arange(1, 9), median, label=name.replace('_', ' '))
        ax.fill_between(np.arange(1, 9), low, high, alpha=.12)
        for h in range(8):
            summaries.append({'scenario': name, 'horizon_quarters': h + 1, 'reserve_p05': low[h],
                              'reserve_median': median[h], 'reserve_p95': high[h]})
    pd.DataFrame(summaries).to_csv(output / 'scenarios.csv', index=False)
    ax.set(title='SYNTHETIC CONDITIONAL SCENARIOS', xlabel='Quarter ahead', ylabel='Reserves, illustrative USD million')
    ax.legend(fontsize=8); ax.grid(alpha=.2); fig.tight_layout()
    fig.savefig(output / 'reserve_scenarios.svg'); plt.close(fig)
    metadata = {'synthetic': synthetic, 'rows': len(data), 'seed': 20261019, 'paths_per_scenario': 4000,
                'horizon_quarters': 8, 'scenario_quantiles': [.05, .5, .95],
                'calibration_rows': min(40, len(frame)), 'units': 'USD million, except exchange rate and ratios',
                'accounting_max_abs_residual': float(data.accounting_residual.abs().max()),
                'scope': 'New synthetic public example, separate from the original BHARAT-FX research archive.',
                'interpretation': 'Relative stress diagnostic and assumed-shock reserve paths; not crisis probabilities, FX forecasts or a calibrated policy-effect estimate.'}
    (output / 'run_metadata.json').write_text(json.dumps(metadata, indent=2))
    return metadata


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--demo', action='store_true'); g.add_argument('--data', type=Path)
    p.add_argument('--output', default='demo_output'); args = p.parse_args()
    frame = synthetic_data() if args.demo else pd.read_csv(args.data, index_col='quarter')
    print(json.dumps(run(frame, args.output, args.demo), indent=2))
