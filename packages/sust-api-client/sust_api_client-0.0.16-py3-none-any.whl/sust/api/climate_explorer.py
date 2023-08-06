import copy
import enum
from typing import Any, List, IO

from sust.api import util
from sust.api.generated.climate_explorer import ApiClient, Configuration
from sust.api.generated.climate_explorer.api import portfolios_api
from sust.api.generated.climate_explorer.model.portfolio_create_request import PortfolioCreateRequest


class PhysicalRiskExposureTimeseries:
    def __init__(self, dict_objects):
        """
        :meta private:
        """
        self._dict_objects = dict_objects

    def to_dicts(self) -> List[dict]:
        """Convert object to python dictionaries."""
        return self._dict_objects


class PhysicalRiskExposureSummary:
    def __init__(self, dict_objects):
        """
        :meta private:
        """
        self._dict_objects = dict_objects

    def to_dicts(self) -> List[dict]:
        """Convert object to python dictionaries."""
        return self._dict_objects


class AssetList:
    def __init__(self, client, portfolio, objects):
        """
        :meta private:
        """
        self._client = client
        self._portfolio = portfolio
        self._objects = objects
        self._index = dict((obj['portfolio_index'], obj) for obj in objects)

    def to_dicts(self) -> List[dict]:
        """Convert object to python dictionaries."""
        return self._objects

    def export_csv(self) -> IO:
        """Export assets as a CSV file. The returned file-like
        object contains the same content originally uploaded to the
        Portfolio. The file-like object contains binary data.
        """
        return self._client._openapi_request('portfolios_assets_export_list', (self._portfolio['portfolio_name'],), {})


class Hazard:
    """Metadata object representing an actual hazard offered by
    a discrete dataset. This can also be used to filter requests
    for data. This class should always be instantiated by an instance
    of :py:class:`~PhysicalRiskExposureDataset`.
    """
    def __init__(self, name):
        self.name = name
        self._filters = [
            util.queryFilter('hazard', name)
        ]


class HazardList(util.itemList):
    pass


class Indicator:
    """Metadata object representing an actual hazard offered by
    a discrete dataset. This can also be used to filter requests
    for data. This class should always be instantiated by an instance
    of :py:class:`~PhysicalRiskExposureDataset`.
    """
    def __init__(self, obj):
        """
        :meta private:
        """
        self._obj = obj
        self.hazard = obj['hazard']
        self.name = obj['indicator']

        self._filters = [
            util.queryFilter('indicator', self.name),
        ] + Hazard(self.hazard)._filters

    def to_dict(self):
        return self._obj.to_dict()


class IndicatorList(util.itemList):
    def get(self, hazard, indicator):
        for it in self._items:
            if it.name == indicator and it.hazard == hazard: return it
        raise ValueError('not found')

    def to_dicts(self):
        return [it.to_dict() for it in self._items]


class Scenario:
    """Metadata object representing an actual hazard offered by
    a discrete dataset. This can also be used to filter requests
    for data. This class should always be instantiated by an instance
    of :py:class:`~PhysicalRiskExposureDataset`.
    """
    def __init__(self, name):
        """
        :meta private:
        """
        self.name = name
        self._filters = [
            util.queryFilter('scenario', name),
        ]


class ScenarioList(util.itemList):
    pass


class Window:
    """Metadata object representing an actual hazard offered by
    a discrete dataset. This can also be used to filter requests
    for data. This class should always be instantiated by an instance
    of :py:class:`~PhysicalRiskExposureDataset`.
    """
    def __init__(self, name):
        """
        :meta private:
        """
        self.name = name
        self._filters = [
            util.queryFilter('window', name),
        ]


class WindowList(util.itemList):
    pass


class Measure:
    """Metadata object representing an actual hazard offered by
    a discrete dataset. This can also be used to filter requests
    for data. This class should always be instantiated by an instance
    of :py:class:`~PhysicalRiskExposureDataset`.
    """
    def __init__(self, name):
        """
        :meta private:
        """
        self.name = name
        self._filters = [
            util.queryFilter('measure', name),
        ]


class MeasureList(util.itemList):
    pass


class PhysicalRiskExposureDataset:
    def __init__(self, client, obj, portfolio):
        """
        :meta private:
        """
        self._client = client
        self._obj = obj
        self.portfolio = portfolio

    @property
    def indicators(self) -> IndicatorList:
        """Get a list of indicators supported by this dataset."""
        return IndicatorList([Indicator(i) for i in self._obj['indicators']])

    @property
    def hazards(self) -> HazardList:
        """Get a list of hazards supported by this dataset."""
        haz = set(i['hazard'] for i in self._obj['indicators'])
        return HazardList([Hazard(h) for h in haz])

    @property
    def scenarios(self) -> ScenarioList:
        """Get a list of scenarios supported by this dataset."""
        return ScenarioList([Scenario(v) for v in ['ssp126', 'ssp245', 'ssp585']])

    @property
    def windows(self) -> WindowList:
        """Get a list of summary windows supported by this dataset."""
        return WindowList([Window(v) for v in [5, 15, 30]])

    @property
    def measures(self) -> MeasureList:
        """Get a list of measures supported by this dataset."""
        return MeasureList([Measure(v) for v in ['lb', 'mid', 'ub']])

    def timeseries(self, *filters: Any) -> PhysicalRiskExposureTimeseries:
        """Retrieve physical risk exposure timeseries data from the
        dataset. Filters may be provided to limit the data returned.

        :param filters: Limit data using the provided filters.
            Typically, one should use the other methods on this class
            to construct filters. For example, the scenarios attribute
            will yield a set of objects describing which scenarios are
            supported by the dataset. Each object may independently
            be passed as a filter here to limit the results to the
            chosen scenario.
        """
        filter_kwargs = util._build_filter_kwargs(filters)
        it = self._client._paginated_openapi_request('portfolios_datasets_physical_items_list', (self.portfolio['portfolio_name'],), filter_kwargs)

        objects = []
        for obj in it:
            obj_d = obj.to_dict()
            re = obj_d.pop('risk_exposure')
            obj_d.update(re)
            objects.append(obj_d)

        return PhysicalRiskExposureTimeseries(objects)

    def summary(self, *filters: Any) -> PhysicalRiskExposureSummary:
        """Retrieve physical risk exposure summary data contained
        within this dataset. Filters may be provided to limit the
        data returned.

        :param filters: Limit data using the provided filters.
            Typically, one should use the other methods on this class
            to construct filters. For example, the scenarios attribute
            will yield a set of objects describing which scenarios are
            supported by the dataset. Each object may independently
            be passed as a filter here to limit the results to the
            chosen scenario.
        """
        filter_kwargs = util._build_filter_kwargs(filters)
        it = self._client._paginated_openapi_request('portfolios_datasets_physical_summary_list', (self.portfolio['portfolio_name'],), filter_kwargs)
        objects = []
        for obj in it:
            obj_d = obj.to_dict()
            summaries = obj_d.pop('risk_summaries')
            for summary in summaries:
                summary.update(obj_d)
                objects.append(summary)

        return PhysicalRiskExposureSummary(objects)

    def export_zip(self) -> IO:
        """Export this physical risk exposure dataset as a zip file.
        The returned object is a binary file-like object."""
        return self._client._openapi_request('portfolios_datasets_physical_export_list', (self.portfolio['portfolio_name'],), {})


class Portfolio:
    def __init__(self, client, obj):
        """
        :meta private:
        """
        self._client = client
        self._obj = obj

    def __getitem__(self, key):
        return self._obj[key]

    def assets(self) -> AssetList:
        """Fetch all assets contained within this Portfolio."""
        objects = self._client._paginated_openapi_request('portfolios_assets_list', (self._obj['portfolio_name'],), {})
        return AssetList(self._client, self, list(objects))

    def import_assets_csv(self, fileobj):
        """Import assets to the portfolio from an open file-like object
        containing CSV-formatted data. This action will replace the
        existing assets contained within the Portfolio and trigger
        generation of risk exposure data. Visit the `Sust Global
        Developer Center <https://developers.sustglobal.com/explorer.html>`_
        for help building a valid input file.

        :param fileobj: file-like object open for binary reading
            (e.g. acces mode 'rb')
        """
        self._client._openapi_request('portfolios_assets_import_create', (self._obj['portfolio_name'], fileobj), {})


    def physical_risk_exposure(self) -> PhysicalRiskExposureDataset:
        """Fetch published dataset metadata pertaining to the Portfolio."""
        obj = self._client._openapi_request('portfolios_datasets_physical_list', (self._obj['portfolio_name'],), {})
        return PhysicalRiskExposureDataset(self._client, obj, self)


class PageIterator:
    """Used to expose paginated API routes as a python iterator.

    :meta private:
    """
    def __init__(self, req_func, req_args, req_kwargs):
        self.req_func = req_func
        self.req_args = req_args
        self.req_kwargs = req_kwargs

        self.req_kwargs['page'] = 1

        self.cache = []
        self.exhausted = False

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.cache) == 0 and not self.exhausted:
            resp = self.req_func(*self.req_args, **self.req_kwargs)
            self.cache = resp

            if len(resp) < self.req_kwargs['rows']:
                self.exhausted = True
            else:
                self.req_kwargs['page'] = self.req_kwargs['page'] + 1

        if len(self.cache) > 0:
            return self.cache.pop(0)

        raise StopIteration


class ClimateExplorerClient:
    """This class wraps all Climate Explorer API functionality into
    one simple to use interface.
    """
    def __init__(self, api_key: str, project: str):
        """
        :param api_key: Climate Explorer API key
        :param project: Climate Explorer project name or ID
        """
        self._api_key = api_key
        self._page_size = 100
        self._default_req_kwargs = {
            'project': project,
        }

        self._init_openapi(endpoint=None)

    def _init_openapi(self, endpoint):
        self._openapi_config = Configuration(host=endpoint)
        self._openapi_config.api_key['api_key'] = self._api_key

        openapi_client = ApiClient(self._openapi_config)
        self._openapi_instance = portfolios_api.PortfoliosApi(openapi_client)

    def _openapi_request(self, request_name, request_args, request_kwargs):
        rk = copy.deepcopy(self._default_req_kwargs)
        rk.update(request_kwargs)
        return getattr(self._openapi_instance, request_name)(*request_args, **rk)

    def _paginated_openapi_request(self, request_name, request_args, request_kwargs):
        rk = copy.deepcopy(self._default_req_kwargs)
        rk['rows'] = self._page_size
        rk.update(request_kwargs)
        return PageIterator(getattr(self._openapi_instance, request_name), request_args, rk)

    def portfolios(self) -> List[Portfolio]:
        """Retrieve all Portfolio objects."""
        #NOTE(bcwaldon): this should be paginated, but is not yet implemented in the API
        it = self._openapi_request('portfolios_list', (), {})
        return (Portfolio(self, obj) for obj in it)

    def create_portfolio(self, portfolio_name: str) -> Portfolio:
        """Create a new Portfolio.

        :param portfolio_name: name provided to new Portfolio. Limited
            to alphanumeric characters, underscores and hyphens.
        """
        req = PortfolioCreateRequest(portfolio_name)
        obj = self._openapi_request('portfolios_create', (req,), {})
        return Portfolio(self, obj)

    def portfolio(self, portfolio_name) -> Portfolio:
        """Retrieve a single Portfolio.

        :param portfolio_name: name of Portfolio to retrieve
        """
        obj = self._openapi_request('portfolios_read', (portfolio_name,), {})
        return Portfolio(self, obj)


def _build_filter_kwargs(filters):
    norm = []
    for f in filters:
        if hasattr(f, '_filters'):
            norm.extend(f._filters)
        else:
            norm.append(f)

    filter_kwargs = {}
    for f in norm:
        name = f.__class__._filter.value
        if name in filter_kwargs:
            raise ValueError(f'duplicate {f.__class__.__name__} provided')
        filter_kwargs[name] = f.value
    return filter_kwargs
