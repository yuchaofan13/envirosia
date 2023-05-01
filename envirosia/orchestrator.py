"""Orchestrates the fetching of raw data
To do later: persist the dynamodb table throughout all calls
"""
import asyncio
from scrapers.yahoo import get_equity
from scrapers.async_handler import get_all_ratings
from utils.dynamo import session_table, check_cache, write_cache
import time


def orchestrator(holdings: list) -> dict:
    """Takes list of tickers as input"""
    table = session_table("ESG")
    cached_data, uncached_tickers = check_cache(holdings, table)
    new_data = {}
    company_names = []
    company_tickers = []
    for ticker_name in uncached_tickers:
        yahoo_data = get_equity(ticker_name)
        if yahoo_data:
            new_data[ticker_name] = yahoo_data
            company_names.append(yahoo_data["name"])
            company_tickers.append(ticker_name)

    ratings_data = []
    for name, ticker in zip(company_names, company_tickers):
        ratings_data = asyncio.run(get_all_ratings([name], [ticker]))
        for datapoint in ratings_data:
            if datapoint:
                tic = datapoint.pop("ticker")
                source = datapoint.pop("source")
                if tic in new_data:
                    new_data[tic][source] = datapoint
        time.sleep(1)
        # to truly leverage async, we should just pass company_names and company_tickers fully
        # but this may hit the rate limit
        # so for now, we use limited concurrency (fetch one rating from each agency concurrently)
    write_cache(new_data.values(), table)
    cached_data.update(new_data)
    return cached_data
