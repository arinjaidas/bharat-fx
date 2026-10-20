import unittest
import numpy as np
import pandas as pd
from public_demo import accounts, synthetic_data, stress_diagnostic, simulate_reserves, vintage_snapshot


class AccountingAndScenarioTests(unittest.TestCase):
    def test_reserve_flow_identity(self):
        out = accounts(synthetic_data())
        np.testing.assert_allclose(out.reserve_transactions, out.current_account + out.fdi + out.portfolio + out.other)

    def test_valuation_is_separate_from_transactions(self):
        data = synthetic_data(); changed = data.copy(); changed['valuation'] += 1234
        one, two = accounts(data), accounts(changed)
        np.testing.assert_allclose(one.reserve_transactions, two.reserve_transactions)
        np.testing.assert_allclose(two.reserves_close - one.reserves_close, 1234)

    def test_contiguous_history_required(self):
        with self.assertRaises(ValueError): accounts(synthetic_data().drop(index='2001Q1'))

    def test_invalid_gdp(self):
        data = synthetic_data(); data.loc[data.index[0], 'gdp'] = 0
        with self.assertRaises(ValueError): accounts(data)

    def test_vintage_cutoff_and_revision(self):
        r = pd.DataFrame({'series': ['CA'] * 3, 'quarter': ['2020Q1'] * 3,
                          'released_at': ['2020-06-01', '2020-07-01', '2021-01-01'], 'value': [1, 2, 99]})
        self.assertEqual(vintage_snapshot(r, '2020-06-30').value.tolist(), [1])
        self.assertEqual(vintage_snapshot(r, '2020-07-01').value.tolist(), [2])

    def test_duplicate_vintage_rejected(self):
        r = pd.DataFrame({'series': ['CA'] * 2, 'quarter': ['2020Q1'] * 2,
                          'released_at': ['2020-06-01'] * 2, 'value': [1, 2]})
        with self.assertRaises(ValueError): vintage_snapshot(r, '2020-07-01')

    def test_future_values_do_not_change_calibration(self):
        data = synthetic_data(); altered = data.copy(); altered.iloc[60:, 0] -= 100000
        one, p1 = stress_diagnostic(data, 40); two, p2 = stress_diagnostic(altered, 40)
        pd.testing.assert_frame_equal(p1, p2)
        pd.testing.assert_frame_equal(one.iloc[:40], two.iloc[:40])

    def test_common_draw_scenario_accounting(self):
        one = simulate_reserves(100, np.zeros(5), np.eye(5), horizon=4, paths=10)
        two = simulate_reserves(100, np.zeros(5), np.eye(5), horizon=4, paths=10, shock=[-2, 0, -3, 0, 0])
        np.testing.assert_allclose(two - one, np.tile(-5 * np.arange(1, 5), (10, 1)), atol=1e-12)

    def test_invalid_covariance(self):
        cov = np.eye(5); cov[0, 0] = -1
        with self.assertRaises(ValueError): simulate_reserves(100, np.zeros(5), cov)

    def test_seed_reproducibility(self):
        a = simulate_reserves(100, np.zeros(5), np.eye(5), paths=10)
        b = simulate_reserves(100, np.zeros(5), np.eye(5), paths=10)
        np.testing.assert_array_equal(a, b)


if __name__ == '__main__': unittest.main()
