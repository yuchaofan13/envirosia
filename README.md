# Envirosia 🌲

Envirosia streamlines ESG fund analysis workflows by integrating the power of GPT-4 with real-time data.

Under the hood, Envirosia uses the GPT-4 API, asyncio/aiohttp, BeautifulSoup and DynamoDB.

Built by Yuchao Fan.

## Demo

https://github.com/yuchaofan13/envirosia/assets/70356595/318e7064-a90f-4632-844c-1e40fb06f297

## Running Envirosia

Create a .env file in the parent directory that contains the following:

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
