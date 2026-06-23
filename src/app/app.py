import streamlit as st

pg = st.navigation(
    {
        "Home" : [st.Page('homepage.py', title = "HomePage", icon = ":material/home:")],
        "Market Analysis" : [
            st.Page("odds/match_explorer.py", title = "Match Explorer"),
            st.Page("odds/bookmaker_rankings.py", title = "Bookmaker Rankings")
        ]
    }
)


pg.run()