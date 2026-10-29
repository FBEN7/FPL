"""Personal dashboard: run with `streamlit run app.py`."""

import streamlit as st

from ffdata import analysis, api

st.set_page_config(page_title="Fantasy dashboard", layout="wide")


@st.cache_data(ttl=3600)
def load():
    return api.bootstrap(), api.fixtures()


bootstrap, fixtures = load()
players = analysis.players_table(bootstrap)
current_gw = analysis.current_gameweek(bootstrap)
next_gw = analysis.next_gameweek(bootstrap)

st.title("Fantasy dashboard")
st.caption(f"Current gameweek: {current_gw} · next deadline: GW{next_gw}")

value_tab, fixtures_tab, team_tab = st.tabs(["Best value", "Fixtures", "My team"])

with value_tab:
    col1, col2, col3 = st.columns(3)
    position = col1.selectbox("Position", ["All", "GKP", "DEF", "MID", "FWD"])
    max_price = col2.slider("Max price (£m)", 3.5, 15.0, 15.0, 0.5)
    min_minutes = col3.slider("Min minutes played", 0, 90 * max(current_gw, 1), 90 * max(current_gw // 2, 1), 90)
    st.dataframe(
        analysis.best_value(
            players,
            position=None if position == "All" else position,
            max_price=max_price,
            min_minutes=min_minutes,
        ),
        hide_index=True,
    )

with fixtures_tab:
    if next_gw is None:
        st.info("The season is over.")
    else:
        horizon = st.slider("Gameweeks ahead", 1, 8, 5)
        st.dataframe(analysis.fixture_ticker(bootstrap, fixtures, next_gw, horizon), hide_index=True)
        st.caption("Difficulty: 1 easy, 5 hard. '-' = blank gameweek.")

with team_tab:
    entry_id = st.text_input("Your team ID (the number in your Points page URL)")
    if entry_id.strip().isdigit() and current_gw:
        picks = api.team_picks(int(entry_id), current_gw)
        st.dataframe(analysis.my_team(picks, players), hide_index=True)
