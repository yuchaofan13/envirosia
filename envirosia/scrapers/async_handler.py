import aiohttp
import asyncio
import json
import re
import os
from .msci import get_msci
from .refinitiv import get_refinitiv
from .sustainalytics import get_sustainalytics


def clean_name(name: str)-> str:
    """Mainly for Refinitiv"""
    name = name.strip()
    name = re.sub("\(The\)$", "", name).strip()
    name = re.sub("(?<!,) Inc\.$", ", Inc.", name).strip()
    name = re.sub("(?<!,) Inc$", ", Inc.", name).strip()
    name = re.sub(", Inc$", ", Inc.", name).strip()
    name = re.sub(", Corp\.$", " Corp.", name).strip()
    name = re.sub(" Corporation$", " Corp.", name).strip()
    name = re.sub(" Company$", " Co.", name).strip()
    name = re.sub(" Incorporated$", ", Inc.", name).strip()
    return name


async def get_all_ratings(company_names: list, company_tickers: list)-> list[dict]:
    names = [clean_name(name) for name in company_names]
    module_path = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(module_path, "esgsearchsuggestions.json")
    with open(json_path) as file:
        mappings = json.load(file)
    ric_dict = {}
    for mapping in mappings:
        for key, value in mapping.items():
            if key == "companyName":
                name = value
            elif key == "ricCode":
                ric = value
        ric_dict[name] = ric

    async with aiohttp.ClientSession() as session:
        tasks = []
        for name, ticker in zip(names, company_tickers):
            tasks.append(asyncio.create_task(get_sustainalytics(session, name, ticker)))
            tasks.append(asyncio.create_task(get_msci(session, name, ticker)))
            tasks.append(
                asyncio.create_task(get_refinitiv(session, name, ticker, ric_dict))
            )

        results = await asyncio.gather(*tasks)
    return results
