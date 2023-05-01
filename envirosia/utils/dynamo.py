import boto3
import os
from dotenv import load_dotenv, find_dotenv


def session_table(table_name: str):
    _ = load_dotenv(find_dotenv())
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="eu-west-1",
    )
    dynamodb = session.resource("dynamodb")
    return dynamodb.Table(table_name)


def check_cache(ticker_names: list, table):
    cached_data = {}
    uncached_tickers = []
    for ticker_name in ticker_names:
        db_response = table.get_item(Key={"ticker_name": ticker_name})
        if "Item" in db_response:
            cached_data[ticker_name] = db_response["Item"]
        else:
            uncached_tickers.append(ticker_name)
    return cached_data, uncached_tickers


def write_cache(items, table):
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
