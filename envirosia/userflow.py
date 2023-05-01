from orchestrator import orchestrator
from scrapers.yahoo import get_fund_object
from prompts import EquityESGPrompt, FundESGPrompt
from async_completion import gather_chat_completions
import streamlit as st
import os
import asyncio
import openai
from visuals import gen_fund_graphics
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

def on_input(fund_input: str):
    fund = get_fund_object(fund_input)
    if not fund:
        st.write("Could not find fund holdings.")
        # either couldn't find fund or can't find holdings
        return
    fund_ticker = fund.symbols[0]
    if "longName" in fund.quotes[fund_ticker]:
        fund_name = fund.quotes[fund_ticker]["longName"]
    else:
        fund_name = fund.quotes[fund_ticker]["shortName"]
    fund_description = fund.asset_profile[fund_ticker]["longBusinessSummary"]

    with st.spinner("Fetching holdings data..."):
        holdings_data = orchestrator(fund.fund_top_holdings["symbol"])
    
    st.subheader(f"Report for {fund_name}")
    gen_fund_graphics(fund, fund_name, holdings_data)
    
    fund_info = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an ESG and financial analysis expert with an excellent eye for detail. You are skeptical of greenwashing but overall unbiased."},
                    {"role": "user", "content": FundESGPrompt(fund_name, fund_description).prompt}
                ],temperature = 0.5,
                stream = True)
    curr = ""
    placeholder = st.empty()
    for chunk in fund_info: # this is a generator
        if "content" in chunk["choices"][0]["delta"]:
            curr+=chunk["choices"][0]["delta"]["content"]
            with placeholder:
                st.write(curr)
    
    st.subheader("Top Holdings Analysis")

    # all holdings analysed in one query
    company_names = []
    prompt_data = []
    for ticker, data in holdings_data.items():
        company_names.append(data["name"])
        prompt_data.append(data)
    prompt = EquityESGPrompt(company_names, prompt_data).prompt()

    response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an ESG and financial analysis expert with an excellent eye for detail. You are skeptical of greenwashing but overall unbiased."},
                    {"role": "user", "content": prompt}],
                temperature = 0.5, stream = True)
    curr = ""
    placeholder = st.empty()
    for chunk in response: # this is a generator
        if "content" in chunk["choices"][0]["delta"]:
            curr+=chunk["choices"][0]["delta"]["content"]
            with placeholder:
                st.write(curr)
    print(curr)

    # async code to analyse all holdings in separate queries (expensive)

    # message_batches = []
    # for ticker, data in holdings_data.items():
    #     message_batches.append(
    #         [{"role": "system", "content": "You are an ESG and financial analysis expert with an excellent eye for detail. You are skeptical of greenwashing but overall unbiased."},
    #          {"role": "user", "content": EquityESGPrompt(data["name"], ticker, data).prompt}]
    #     )
    # with st.spinner("Generating analysis of top holdings..."):
    #     completions = asyncio.run(gather_chat_completions(message_batches))
    #     completions = [i["choices"][0]["message"]["content"] for i in completions]
    # for completion in completions:
    #     ticker, text = completion.split(" ", 1)
    #     st.subheader(ticker)
    #     st.text(text)