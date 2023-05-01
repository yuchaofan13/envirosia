import pandas as pd
import plotly.express as px
import streamlit as st
from yahooquery import Ticker

def flatten_nested_json_df(df: pd.DataFrame)-> pd.DataFrame:
    """from stackoverflow"""

    df = df.reset_index()

    # search for columns to explode/flatten
    s = (df.applymap(type) == list).all()
    list_columns = s[s].index.tolist()

    s = (df.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()

    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            # explode dictionaries horizontally, adding new columns
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f"{col}.")
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns)  # inplace

        for col in list_columns:
            print(f"exploding: {col}")
            # explode lists vertically, adding new columns
            df = df.drop(columns=[col]).join(df[col].explode().to_frame())
            # Prevent combinatorial explosion when multiple
            # cols have lists or lists of lists
            df = df.reset_index(drop=True)
            new_columns.append(col)

        # check if there are still dict o list fields to flatten
        s = (df[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (df[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()
    return df


def pd_msci(row: dict | None)-> dict | None:
    output = {"implied_temp": None, "latest_rating": None}
    if not isinstance(row, dict):
        return output
    if "implied_temp" in row:
        output["implied_temp"] = row["implied_temp"]
    if "latest_rating" in row:
        output["latest_rating"] = row["latest_rating"]
    return output


def gen_fund_graphics(fund_object: Ticker, fund_name: str, holdings_data: dict):
    """Must be a fund, or else you won't have fund_top_holdings"""
    col1, col2 = st.columns(2)

    df = (
        pd.DataFrame.from_dict(holdings_data)
        .T.drop(columns=["ticker_name", "exec_ages", "iss_governance_scores"])
        .reset_index(drop=True)
        .rename(columns={"name": "Name"})
        .set_index("Name")
        .dropna(how="all")
    )
    df["MSCI"] = df["MSCI"].apply(pd_msci)
    df = flatten_nested_json_df(df)

    with col1:
        st.write("Top Holdings")
        st.dataframe(df)
    with col2:
        historical = fund_object.history().reset_index()
        fig = px.line(
            historical,
            x="date",
            y="close",
            labels={"date": "Date", "close": "Close"},
            title=fund_name,
        )
        st.plotly_chart(fig, use_container_width=True)
