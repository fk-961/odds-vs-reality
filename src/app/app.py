import streamlit as st

pg = st.navigation(
    {
        "Home" : [st.Page('homepage.py', title = "HomePage", icon = ":material/home:")],
        "Odds" : [
            st.Page("odds/match_odds.py", title = "Match Odds"),
            st.Page("odds/bookmaker_odds.py", title = "Bookmaker Odds")
        ]
    }
)


pg.run()