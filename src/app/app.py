import streamlit as st


st.set_page_config(
    page_title="Football Analytics",
    page_icon="⚽",
    layout="wide"
)

pg = st.navigation(
    {
        "Home" : [st.Page('homepage.py', title = "HomePage", icon = ":material/home:")],
        "Market Analysis" : [
            st.Page("odds/bookmaker_calibration.py", title = "Bookmaker Calibration"),
            st.Page("odds/match_explorer.py", title = "Match Explorer"),
            st.Page("odds/bookmaker_rankings.py", title = "Bookmaker Rankings")
        ]
    }
)


pg.run()