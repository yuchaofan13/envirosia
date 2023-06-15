import json
import re
from bs4 import BeautifulSoup


async def get_msci(session, name: str, ticker: str) -> dict | None:
    """Allows fuzzy matching"""
    search_name = "+".join(name.split())  # purely to format the keywords query
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    async with session.get(
        "https://www.msci.com/our-solutions/esg-investing/"
        "esg-ratings-climate-search-tool?"
        "p_p_id=esgratingsprofile&p_p_lifecycle=2&p_p_state=normal"
        "&p_p_mode=view&p_p_resource_id=searchEsgRatingsProfiles"
        "&p_p_cacheability=cacheLevelPage"
        f"&_esgratingsprofile_keywords={search_name}",
        headers=headers,
    ) as resp:
        response = await resp.text()
    if len(response) == 0:
        return
    if len(json.loads(response))==0:
        return
    url = json.loads(response)[0]["url"]
    title = json.loads(response)[0]["encodedTitle"]

    headers[
        "Referer"
    ] = f"https://www.msci.com/our-solutions/esg-investing/esg-ratings-climate-search-tool/issuer/{title}/{url}"
    async with session.get(
        f"https://www.msci.com/our-solutions/esg-investing/esg-ratings-climate-search-tool?p_p_id=esgratingsprofile&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=showEsgRatingsProfile&p_p_cacheability=cacheLevelPage&_esgratingsprofile_issuerId={url}",
        headers=headers,
    ) as resp:
        response = await resp.text()

    data = response.strip().replace(chr(10), "").replace(chr(9), "")
    soup = BeautifulSoup(data, "html.parser")
    result_ticker = soup.find("div", {"class": "header-company-ticker"})
    result_ticker = result_ticker.text[1:-1] if result_ticker else None
    implied_temp = soup.find("span", {"class": "implied-temp-rise-value"})
    implied_temp = implied_temp.text if implied_temp else None
    vs_peers = soup.find("span", {"class": "average-letters"})
    vs_peers = vs_peers.text if vs_peers else None
    ratings_regex = re.compile(
        "chartData\.esgRatingHistory\.dates\.push\('(?P<date>[^\)']+)'\);var rating = '(?P<rating>[^\)']+)"
    )
    ratings_history = re.findall(ratings_regex, data)
    latest_rating = None
    if len(ratings_history) > 0:
        latest_rating = ratings_history[-1][-1]
        ratings_history = {date: rating for date, rating in ratings_history}
    sdg_aligned_goals = [
        i.text for i in soup.find_all("div", {"class": "sdg-aligned-row"})
    ]
    sdg_strongly_aligned_goals = [
        i.text for i in soup.find_all("div", {"class": "sdg-strongly-aligned-row"})
    ]

    return {
        "source": "MSCI",
        "ticker": result_ticker,
        "ratings_history": ratings_history,
        "latest_rating": latest_rating,
        "implied_temp": implied_temp,
        "vs_peers": vs_peers,
        "sdg_aligned_goals": sdg_aligned_goals,
        "sdg_strongly_aligned_goals": sdg_strongly_aligned_goals,
    }
