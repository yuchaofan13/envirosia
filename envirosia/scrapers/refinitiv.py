import re
import json


async def get_refinitiv(session, name: str, ticker: str, ric_dict: dict) -> dict | None:
    name = re.sub("\.$", "", name)
    name = name.replace(",", "")
    if name in ric_dict:
        ric = ric_dict[name]
        async with session.get(
            f"https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode={ric}"
        ) as resp:
            response = await resp.text()
        output = json.loads(response)
        output["ticker"] = ric.rsplit(".", 1)[0]
        output["source"] = "Refinitiv"
        if "industryComparison" in output and isinstance(
            output["industryComparison"], dict
        ):
            comparison = output.pop("industryComparison")
            output["rank"] = comparison["rank"] + "/" + comparison["totalIndustries"]
        if "esgScore" in output and isinstance(output["esgScore"], dict):
            scores = output.pop("esgScore")
            output["esgScore"] = str(scores["TR.TRESG"]["score"])
            # overall score
        return output
