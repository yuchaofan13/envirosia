import streamlit as st

st.header("Envirosia")
col1, col2 = st.columns(2)
with col1:
    st.write(
        """
    In recent years, unprecedented environmental crises have led to escalating economic volatility. 
    In the pursuit of directing financing towards critical solutions, 
    ESG-oriented mutual funds and ETFs have expanded at an accelerating rate, 
    leading to an increasing demand for information that helps investors to identify funds with maximized ESG impacts.
    """
    )
with col2:
    st.write(
        """Our integrated platform Envirosia AI is the world's first AI-powered fund analysis generator focusing on ESG funds. 
            Our fully automated ESG fund analysis generator uses advanced generative AI technologies 
            to produce comprehensive ESG fund analysis that covers the ESG performances of the fund's top holdings, portfolio construction criteria, 
            as well as the asset manager's ESG alignment. 
            Our product could greatly expedite the analysis process that's currently carried out manually by fund analysts and offer accessible and transparent information 
            for impact investors to make informed ESG investment decisions."""
    )
