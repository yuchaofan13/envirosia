import openai
import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Built by Yuchao Fan"},
)
from userflow import on_input
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.subheader("Empowering accessible and transparent ESG investing with artificial intelligence")
with col2:
    st.image("./assets/logo.JPG")

hide_streamlit_style = """
            <style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
fund_input = st.text_input("I want to generate an ESG fund analysis of:")
if fund_input:
    st.divider()
    on_input(fund_input)