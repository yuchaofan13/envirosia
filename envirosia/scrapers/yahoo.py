from yahooquery import Ticker
from duckduckgo_search import ddg
import re


def get_fund_object(user_input: str) -> Ticker | None:
    """
    Lets user input a fund name or keywords.
    If a matching Yahoo Finance page is found,
    we extract the ticker and instantiate a yahooquery ticker object.
    We then check if this has holdings- if not, then it's not a fund.
    Returns a yahooquery ticker object or None.
    """
    links = [i["href"] for i in ddg(f"{user_input} yahoo finance", max_results=8)]
    ticker_regex = re.compile("yahoo.com/quote/(?P<ticker>[^/]+)/")
    for link in links:
        extract_ticker = re.search(ticker_regex, link)
        if extract_ticker:
            fund = Ticker(extract_ticker["ticker"])
            if not fund.fund_top_holdings.empty:
                return fund


def get_equity(ticker_name: str) -> dict | None:
    """Does not work well for holdings that are Chinese tickers
    Maybe they're just not there on Yahoo Finance
    """
    equity = Ticker(ticker_name)
    if isinstance(equity.quotes, str):
        return  # no data found for this ticker
    if "shortName" not in equity.quotes[ticker_name]:
        return
    name = equity.quotes[ticker_name]["shortName"]
    exec_ages = None
    if "age" in equity.company_officers.columns:
        ages = [int(i) for i in equity.company_officers["age"].fillna(0)]
        ages = ["Unknown" if i == 0 else str(i) for i in ages]
        exec_ages = {i: j for i, j in zip(equity.company_officers["name"], ages)}
    iss_governance_scores = None
    if isinstance(equity.asset_profile[ticker_name], dict):
        iss_governance_scores = {
            key: str(val)
            for key, val in equity.asset_profile[ticker_name].items()
            if key[-4:] == "Risk"
        }
    return {
        "ticker_name": ticker_name,
        "name": name,
        "exec_ages": exec_ages,
        "iss_governance_scores": iss_governance_scores,
    }
