from ffdata import analysis

BOOTSTRAP = {
    "events": [
        {"id": 1, "is_current": True, "is_next": False},
        {"id": 2, "is_current": False, "is_next": True},
    ],
    "teams": [
        {"id": 1, "short_name": "AAA"},
        {"id": 2, "short_name": "BBB"},
        {"id": 3, "short_name": "CCC"},
    ],
    "element_types": [
        {"id": 1, "singular_name_short": "GKP"},
        {"id": 3, "singular_name_short": "MID"},
    ],
    "elements": [
        {"id": 10, "web_name": "Cheap", "team": 1, "element_type": 3, "now_cost": 50,
         "total_points": 40, "points_per_game": "5.0", "form": "6.0", "minutes": 720,
         "expected_goal_involvements": "2.1", "selected_by_percent": "10.0",
         "status": "a", "news": ""},
        {"id": 11, "web_name": "Pricey", "team": 2, "element_type": 3, "now_cost": 120,
         "total_points": 60, "points_per_game": "7.5", "form": "8.0", "minutes": 720,
         "expected_goal_involvements": "5.0", "selected_by_percent": "50.0",
         "status": "a", "news": ""},
        {"id": 12, "web_name": "Keeper", "team": 3, "element_type": 1, "now_cost": 45,
         "total_points": 30, "points_per_game": "3.8", "form": "4.0", "minutes": 90,
         "expected_goal_involvements": "0.0", "selected_by_percent": "1.0",
         "status": "d", "news": "Knock"},
    ],
}

# GW2: AAA v BBB; GW3: double for AAA (v BBB and v CCC), so BBB and CCC play once each.
FIXTURES = [
    {"event": 1, "team_h": 1, "team_a": 3, "team_h_difficulty": 2, "team_a_difficulty": 4},
    {"event": 2, "team_h": 1, "team_a": 2, "team_h_difficulty": 3, "team_a_difficulty": 3},
    {"event": 3, "team_h": 2, "team_a": 1, "team_h_difficulty": 2, "team_a_difficulty": 4},
    {"event": 3, "team_h": 1, "team_a": 3, "team_h_difficulty": 2, "team_a_difficulty": 5},
]


def test_gameweeks():
    assert analysis.current_gameweek(BOOTSTRAP) == 1
    assert analysis.next_gameweek(BOOTSTRAP) == 2


def test_players_table_converts_price_and_value():
    players = analysis.players_table(BOOTSTRAP).set_index("name")
    assert players.loc["Cheap", "price"] == 5.0
    assert players.loc["Cheap", "points_per_million"] == 8.0
    assert players.loc["Pricey", "team"] == "BBB"
    assert players.loc["Keeper", "position"] == "GKP"


def test_best_value_filters_and_sorts():
    players = analysis.players_table(BOOTSTRAP)
    assert list(analysis.best_value(players)["name"]) == ["Cheap", "Keeper", "Pricey"]
    assert list(analysis.best_value(players, position="MID", max_price=6)["name"]) == ["Cheap"]
    assert list(analysis.best_value(players, min_minutes=100)["name"]) == ["Cheap", "Pricey"]


def test_fixture_ticker_handles_blank_and_double():
    ticker = analysis.fixture_ticker(BOOTSTRAP, FIXTURES, start_gw=2, horizon=2).set_index("team")
    assert ticker.loc["AAA", "GW3"] == "BBB (A), CCC (H)"
    assert ticker.loc["AAA", "fixtures"] == 3
    assert ticker.loc["AAA", "avg_difficulty"] == 3.0
    assert ticker.loc["CCC", "GW2"] == "-"
    assert ticker.loc["CCC", "avg_difficulty"] == 5.0
    assert list(ticker.index) == ["BBB", "AAA", "CCC"]


def test_my_team_orders_slots_and_marks_captain():
    players = analysis.players_table(BOOTSTRAP)
    picks = {"picks": [
        {"element": 11, "position": 12, "is_captain": False, "is_vice_captain": False},
        {"element": 10, "position": 1, "is_captain": True, "is_vice_captain": False},
        {"element": 12, "position": 2, "is_captain": False, "is_vice_captain": True},
    ]}
    team = analysis.my_team(picks, players)
    assert list(team["name"]) == ["Cheap", "Keeper", "Pricey"]
    assert list(team["captain"]) == ["C", "V", ""]
    assert list(team["starter"]) == [True, True, False]
    assert team.loc[0, "position"] == "MID"
