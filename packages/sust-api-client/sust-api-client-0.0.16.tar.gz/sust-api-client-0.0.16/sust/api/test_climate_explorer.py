import csv
import io
import os
import unittest

from sust.api import ClimateExplorerClient


class SmokeTestCase(unittest.TestCase):

    def setUpClass():
        for k in ['SUST_API_KEY', 'SUST_PROJECT', 'SUST_PORTFOLIO']:
            if k not in os.environ:
                raise Exception(f'{k} must be set')

    def _client(self):
        return ClimateExplorerClient(os.getenv('SUST_API_KEY'), os.getenv('SUST_PROJECT'))

    def _portfolio(self):
        return self._client().portfolio(os.getenv('SUST_PORTFOLIO'))

    def test_portfolios(self):
        portfolios = self._client().portfolios()
        self.assertTrue(len(list(portfolios)))

    def test_assets(self):
        pf = self._portfolio()
        al = pf.assets()

        ad = al.to_dicts()
        self.assertTrue(ad)

        ab = al.export_csv().read()
        rows = list(csv.DictReader(io.StringIO(ab.decode())))
        self.assertTrue(rows)

        first = rows[0]
        self.assertTrue('lat' in first)
        self.assertTrue('lng' in first)

        self.assertEqual(len(ad), len(rows))

    def test_physical_risk_exposure_attributes(self):
        pf = self._portfolio()
        ds = pf.physical_risk_exposure()

        self.assertTrue(len(list(ds.indicators)))
        for it in ds.indicators:
            self.assertTrue(ds.indicators.get(it.hazard, it.name))

        self.assertTrue(len(list(ds.windows)))
        for it in ds.windows:
            self.assertTrue(ds.windows.get(it.name))

        self.assertTrue(len(list(ds.measures)))
        for it in ds.measures:
            self.assertTrue(ds.measures.get(it.name))

        self.assertTrue(len(list(ds.hazards)))
        for it in ds.hazards:
            self.assertTrue(ds.hazards.get(it.name))

        self.assertTrue(len(list(ds.scenarios)))
        for it in ds.scenarios:
            self.assertTrue(ds.scenarios.get(it.name))

    def test_physical_risk_exposure_timeseries(self):
        pf = self._portfolio()
        ds = pf.physical_risk_exposure()

        # represents a query that should be stable over time, returning
        # one entry per asset...
        td = ds.timeseries(
                ds.scenarios.get('ssp245'),
                ds.indicators.get('wildfire', 'fire_kbdi_susceptibility'),
                ds.measures.get('mid'),
        ).to_dicts()
        self.assertTrue(td)

        # ...which means we can confirm we end up with one entry per asset
        ad = pf.assets().to_dicts()
        self.assertEqual(len(td), len(ad))

        first = td[0]
        self.assertTrue('portfolio_index' in first)
        self.assertTrue('2022' in first)

    def test_physical_risk_exposure_summary(self):
        pf = self._portfolio()
        ds = pf.physical_risk_exposure()

        # represents a query that should be stable over time, returning
        # one entry per asset...
        sd = ds.summary(
                ds.scenarios.get('ssp245'),
                ds.windows.get(30),
                ds.hazards.get('water_stress'),
        ).to_dicts()
        self.assertTrue(sd)

        # ...which means we can confirm we end up with one entry per asset
        ad = pf.assets().to_dicts()
        self.assertEqual(len(sd), len(ad))

        first = sd[0]
        self.assertTrue('portfolio_index' in first)
        self.assertTrue('risk_class' in first)
