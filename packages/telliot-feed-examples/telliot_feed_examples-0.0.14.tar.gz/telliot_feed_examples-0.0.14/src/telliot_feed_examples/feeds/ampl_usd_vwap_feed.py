"""Example datafeed used by AMPLUSDVWAPReporter."""
from telliot_core.datafeed import DataFeed
from telliot_core.queries.legacy_query import LegacyRequest

from telliot_feed_examples.sources.ampl_usd_vwap import AMPLUSDVWAPSource


ampl_usd_vwap_feed = DataFeed(
    query=LegacyRequest(legacy_id=10), source=AMPLUSDVWAPSource()
)
