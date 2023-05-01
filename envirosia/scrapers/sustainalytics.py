from bs4 import BeautifulSoup
from decimal import Decimal

# DynamoDB doesn't allow floats


async def get_sustainalytics(session, name, ticker):
    async with session.post(
        "https://www.sustainalytics.com/sustapi/companyratings/GetCompanyDropdown",
        json={
            "filter": name,
            "resourcePackage": "Sustainalytics",
            "page": 1,
            "pageSize": 10,
        },
    ) as resp:
        response = await resp.text()
        subdir = BeautifulSoup(response, "html.parser").find(
            "a", {"class": "search-link js-fix-path"}
        )
        if not subdir:
            return
        else:
            subdir = subdir["data-href"]
    async with session.get(
        f"https://www.sustainalytics.com/esg-rating{subdir}"
    ) as resp:
        response = await resp.text()
        soup = BeautifulSoup(response, "html.parser")

    rank = soup.find("strong", {"class": "industry-group-position"}).text
    industry = soup.find("span", {"class": "industry-group-positions-total"}).text

    return {
        "source": "Sustainalytics",
        "ticker": soup.find("strong", {"class": "identifier"}).text.split(":")[-1],
        "risk_level": soup.find("div", {"class": "col-6 risk-rating-assessment"}).text,
        "risk_score": str(soup.find("div", {"class": "col-6 risk-rating-score"}).text),
        "rank": rank + "/" + industry,
    }
