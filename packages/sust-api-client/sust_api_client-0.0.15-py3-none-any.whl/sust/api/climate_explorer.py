import copy
import enum
from typing import Any, List

from sust.api.generated.climate_explorer import ApiClient, Configuration
from sust.api.generated.climate_explorer.api import portfolios_api
from sust.api.generated.climate_explorer.model.portfolio_create_request import PortfolioCreateRequest


class LabelFilter:
    """Limit objects to provided key and value"""
    def __init__(self, key, value):
        self.key = key
        self.value = value


class WindowFilters(enum.Enum):
    """Possible summary window values provided as API request
    filters.
    """
    YEARS_5 = 5
    YEARS_15 = 15
    YEARS_30 = 30

    _filter = 'window'


class ScenarioFilters(enum.Enum):
    """Possible SSP scenario values provided as API request
    filters.
    """
    SSP126 = 'ssp126'
    SSP245 = 'ssp245'
    SSP585 = 'ssp585'

    _filter = 'scenario'


class HazardFilters(enum.Enum):
    """Possible climatological hazard values provided as API request
    filters.
    """
    CYCLONE = 'cyclone'
    WILDFIRE = 'wildfire'
    FLOOD_POTENTIAL = 'flood_potential'
    WATER_STRESS = 'water_stress'
    SEA_LEVEL_RISE = 'sea_level_rise'
    HEATWAVE = 'heatwave'
    FUNDAMENTAL = 'fundamental'

    _filter = 'hazard'


class IndicatorFilters(enum.Enum):
    """Possible indicator name values provided as API request
    filters. Note that indicator filters
    must be used with a corresponding hazard filter.
    """
    BURNED_AREA = 'burned_area_norm'
    CHANGE = 'change'
    EXTREME_PRECIPITATION = 'extreme_precip'
    FREQUENCY = 'freq'
    FIRE_KBDI_SUSCEPTIBILITY = 'fire_kbdi_susceptibility'
    INLAND_FLOOD_PROBABILITY = 'inland_flood_prob'
    OBSERVED_SCORE = 'obs_score'
    OBSERVED_FREQUENCY = 'obs_freq'
    PRECIPITATION = 'precip'
    PROBABILITY = 'prob'
    SCORE = 'score'
    SPEI = 'spei_norm'
    TEMPERATURE = 'temp'

    _filter = 'indicator'


class MeasureFilters(enum.Enum):
    """Possible measure values provided as API request
    filters.
    """
    LOWER_BOUND = 'lb'
    MIDPOINT = 'mid'
    UPPER_BOUND = 'ub'

    _filter = 'measure'


class PhysicalRiskTimeseriesList:
    def __init__(self, dict_objects):
        """
        :meta private:
        """
        self._dict_objects = dict_objects

    def to_dicts(self) -> List[dict]:
        """Convert object to python dictionaries."""
        return self._dict_objects


class PhysicalRiskSummaryList:
    def __init__(self, dict_objects):
        """
        :meta private:
        """
        self._dict_objects = dict_objects

    def to_dicts(self) -> List[dict]:
        """Convert object to python dictionaries."""
        return self._dict_objects


class AssetList:
    def __init__(self, portfolio, objects):
        """
        :meta private:
        """
        self._portfolio = portfolio
        self._objects = objects
        self._index = dict((obj['portfolio_index'], obj) for obj in objects)

    def to_dicts(self) -> List[dict]:
        """Convert object to python dictionaries."""
        return [obj.to_dict() for obj in self._objects]

    def physical_risk_timeseries(self, *filters: Any) -> PhysicalRiskTimeseriesList:
        """Fetch physical risk exposure timeseries data scoped to the
        assets contained in this AssetList. Filters may be provided to
        further limit the data returned.

        :param filters: limit data using the provided filters. Only one
            of each type of filter may be provided. Available filters
            are located in :py:class:`~ScenarioFilters`,
            :py:class:`~HazardFilters`, :py:class:`IndicatorFilters`,
            and :py:class:`MeasureFilters`
        """
        lst = self._portfolio.physical_risk_timeseries(filters)
        filtered = [do for do in lst.to_dicts() if do['portfolio_index'] in self._index]
        return PhysicalRiskTimeseriesList(filtered)

    def physical_risk_summary(self, *filters: Any) -> PhysicalRiskSummaryList:
        """Fetch physical risk exposure summary data scoped to the
        assets contained in this AssetList. Filters may be provided to
        further limit the data returned.

        :param filters: limit data using the provided filters. Only one
            of each type of filter may be provided. Available filters
            are located in :py:class:`~ScenarioFilters`,
            :py:class:`~HazardFilters`, and :py:class:`WindowFilters`
        """
        lst = self._portfolio.physical_risk_summary(filters)
        filtered = [do for do in lst.to_dicts() if do['portfolio_index'] in self._index]
        return PhysicalRiskSummaryList(filtered)


class Portfolio:
    def __init__(self, client, obj):
        """
        :meta private:
        """
        self._client = client
        self._obj = obj
        self.name = obj["portfolio_name"]

    def __getitem__(self, key):
        return self._obj[key]

    def assets(self, *filters: LabelFilter) -> AssetList:
        """Fetch all assets contained within this Portfolio. Filters
        may be provided to limit the data returned.

        :param filters: Each LabelFilter is directly applied, meaning
            all assets must have exactly the key(s) and corresponding
            value(s) provided.
        """
        it = self._client._paginated_openapi_request('portfolios_assets_list', (self._obj['portfolio_name'],), {})

        objects = [
            obj for obj in it if
              (filters == None or all(obj['labels'].get(lf.key) == lf.value for lf in filters))
        ]

        return AssetList(self, objects)

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

    def _build_filter_kwargs(self, filters):
        filter_kwargs = {}
        for f in filters:
            name = f.__class__._filter.value
            if name in filter_kwargs:
                raise ValueError(f'duplicate {f.__class__.__name__} provided')
            filter_kwargs[name] = f.value
        return filter_kwargs

    def physical_risk_timeseries(self, *filters: Any) -> PhysicalRiskTimeseriesList:
        """Fetch all physical risk exposure timeseries data within this
        Portfolio. Filters may be provided to limit the data returned.

        :param filters: limit data using the provided filters. Only one
            of each type of filter may be provided. Available filters
            are located in :py:class:`~ScenarioFilters`,
            :py:class:`~HazardFilters`, :py:class:`IndicatorFilters`,
            and :py:class:`MeasureFilters`
        """
        filter_kwargs = self._build_filter_kwargs(filters)
        it = self._client._paginated_openapi_request('portfolios_datasets_physical_items_list', (self.name,), filter_kwargs)

        objects = []
        for obj in it:
            obj_d = obj.to_dict()
            re = obj_d.pop('risk_exposure')
            obj_d.update(re)
            objects.append(obj_d)

        return PhysicalRiskTimeseriesList(objects)

    def physical_risk_summary(self, *filters: Any) -> PhysicalRiskSummaryList:
        """Fetch all physical risk exposure summary data contained
        within this Portfolio. Filters may be provided to limit the
        data returned.

        :param filters: limit data using the provided filters. Only one
            of each type of filter may be provided. Available filters
            are located in :py:class:`~ScenarioFilters`,
            :py:class:`~HazardFilters`, and :py:class:`WindowFilters`
        """
        filter_kwargs = self._build_filter_kwargs(filters)
        it = self._client._paginated_openapi_request('portfolios_datasets_physical_summary_list', (self.name,), filter_kwargs)
        objects = []
        for obj in it:
            obj_d = obj.to_dict()
            summaries = obj_d.pop('risk_summaries')
            for summary in summaries:
                summary.update(obj_d)
                objects.append(summary)

        return PhysicalRiskSummaryList(objects)


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
