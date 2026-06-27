import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.markdown("""
<style>
.stButton > button {
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #ff3b3b !important;
    color: white !important;
    border: 1px solid #ff3b3b !important;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

APP_PASSWORD = os.getenv("APP_PASSWORD")

# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if not st.session_state.authenticated:

#     st.title("Against all Odds...")
#     st.write("This application is currently in private beta.")

#     password = st.text_input("Password:", type="password")

#     if st.button("Get started"):
#         if password == APP_PASSWORD:
#             st.session_state.authenticated = True
#             st.rerun()
#         else:
#             st.error("Incorrect password")

#     st.stop()


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
        ],
        "Calibration by Outcome" : [
            st.Page("calibration/home.py", title = "Home Wins")
        ]
    }
)


pg.run()