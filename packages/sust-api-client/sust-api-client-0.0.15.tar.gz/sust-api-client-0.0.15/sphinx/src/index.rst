Sust Global Python API Client
=============================

This document details how to use the ``sust-api-client`` python package to interact with Sust Global's Climate Explorer API.

Much of this client is generated using OpenAPI:

* Current OpenAPI spec: https://explorer.sustglobal.io/swagger.json
* OpenAPI spec documenation: https://explorer.sustglobal.io/redoc/

Quickstart
----------

Initialize a client, providing your Climate Explorer API key and project name:

.. code-block:: python

    client = ClimateExplorerClient(API_KEY, PROJECT)


Access physical risk exposure summary data with filters:

.. code-block:: python

    client.physical_risk_summary(
        WindowFilters.YEAR_30,
        HazardFilters.WILDFIRE,
        ScenarioFilters.SSP585
    )


Python API Reference
--------------------

.. autoclass:: sust.api.climate_explorer.ClimateExplorerClient
   :members:

.. autoclass:: sust.api.climate_explorer.Portfolio
   :members:

.. autoclass:: sust.api.climate_explorer.AssetList
   :members:

.. autoclass:: sust.api.climate_explorer.PhysicalRiskTimeseriesList
   :members:

.. autoclass:: sust.api.climate_explorer.PhysicalRiskSummaryList
   :members:

.. autoclass:: sust.api.climate_explorer.LabelFilter
   :members:
   :undoc-members:

.. autoclass:: sust.api.climate_explorer.ScenarioFilters
   :members:
   :undoc-members:

.. autoclass:: sust.api.climate_explorer.HazardFilters
   :members:
   :undoc-members:

.. autoclass:: sust.api.climate_explorer.IndicatorFilters
   :members:
   :undoc-members:

.. autoclass:: sust.api.climate_explorer.WindowFilters
   :members:
   :undoc-members:

.. autoclass:: sust.api.climate_explorer.MeasureFilters
   :members:
   :undoc-members:
