# Envirosia 🌲

Envirosia streamlines ESG fund analysis workflows by integrating the power of GPT-4 with real-time data. This proof of concept was built by Yuchao Fan.

## Motivation

ESG is becoming an increasingly important consideration for the investment decisions of both institutions and individuals. To meet this demand, ratings agencies now provide a variety of ESG scores for both individual equities and funds. However, ESG ratings can be highly inconsistent between agencies, and overall fund ratings can be opaque. One must first look at the underlying fund holdings and consider data from a diverse panel of sources before coming to a conclusion.

We talked to numerous ESG analysts, who identified two key pain points in this process: 1. aggregating the relevant data and 2. the initial processing and analysis of the data to extract key insights. The former point is partially mitigated if you have a Bloomberg Terminal, but the latter point remains an issue (and the terminal comes at a hefty cost).

Envirosia provides an end-to-end solution that addresses both of these pain points and is designed to be far more accessible; we want to democratise ESG investing. This proof of concept is built using the Streamlit framework, and the only input required from the user is the name of the fund they want to analyse. Yahoo Finance and DuckDuckGo-Search are first used to extract the fund holdings and basic metadata. There are then two core features:

1. Using asynchronous webscraping (asyncio/aiohttp) and the BeautifulSoup XML parser, we are able to rapidly collect the latest ESG data from the three big ESG ratings agencies: MSCI, Refinitiv and Sustainalytics. None of them have free APIs intended for outside use; however, by tracking XHR requests, I was able to reverse engineer the underlying API endpoints that serve their websites. DynamoDB is used for caching purposes.
3. With some careful prompt engineering, all of this data is passed to the GPT-4 API. GPT-4 provides some initial analysis of the ESG numerical data, such as how a given stock performs relative to its peers, and also summarises text data. The GPT-4 response is streamed back to the user, and data is visualised using Pandas and Plotly.

## Demo
https://github.com/yuchaofan13/envirosia/assets/70356595/34166c6c-c5d4-4611-8d99-2a60519bb335

## Running Envirosia

Create a .env file in the parent directory that contains the following:
```
OPENAI_API_KEY = 1234567890

AWS_ACCESS_KEY_ID = ABCDEFGH

AWS_SECRET_ACCESS_KEY = ABCDEFGH
 ```

Install requirements:
```
pip install requirements.txt
```
To run the Streamlit app:
```
streamlit run Home.py
```
## Future Development Plans
* Add more data sources, such as Wind (for China)
* Integrate web plugins to allow GPT-4 to search for the latest news stories regarding a given stock
* Improve the async scraping to use a Semaphore (currently, we are not making full use of the async functionality to avoid getting our IP blocked)
* Migrate to a proper backend-frontend framework
