"""Turn raw API data into tables: players, value and fixture difficulty."""

import pandas as pd


def current_gameweek(bootstrap):
    """The gameweek in progress, or the last finished one; 0 before the season starts."""
    current = [e["id"] for e in bootstrap["events"] if e["is_current"]]
    return current[0] if current else 0


def next_gameweek(bootstrap):
    """The next gameweek with a deadline still ahead; None after the last one."""
    upcoming = [e["id"] for e in bootstrap["events"] if e["is_next"]]
    return upcoming[0] if upcoming else None


def players_table(bootstrap):
    """One row per player, with readable team, position and price in £m."""
    teams = {t["id"]: t["short_name"] for t in bootstrap["teams"]}
    positions = {p["id"]: p["singular_name_short"] for p in bootstrap["element_types"]}

    df = pd.DataFrame(bootstrap["elements"])
    table = pd.DataFrame({
        "id": df["id"],
        "name": df["web_name"],
        "team": df["team"].map(teams),
        "position": df["element_type"].map(positions),
        "price": df["now_cost"] / 10,
        "total_points": df["total_points"],
        "points_per_game": df["points_per_game"].astype(float),
        "form": df["form"].astype(float),
        "minutes": df["minutes"],
        "xgi": df["expected_goal_involvements"].astype(float),
        "selected_by_pct": df["selected_by_percent"].astype(float),
        "status": df["status"],
        "news": df["news"],
    })
    table["points_per_million"] = (table["total_points"] / table["price"]).round(2)
    return table


def best_value(players, position=None, max_price=None, min_minutes=0, top=20):
    """Players with the most points per £m, after the given filters."""
    rows = players[players["minutes"] >= min_minutes]
    if position:
        rows = rows[rows["position"] == position]
    if max_price is not None:
        rows = rows[rows["price"] <= max_price]
    return rows.sort_values("points_per_million", ascending=False).head(top)


def fixture_ticker(bootstrap, fixtures, start_gw, horizon=5):
    """Opponents and difficulty (1 easy, 5 hard) per team for the next `horizon` gameweeks.

    A blank gameweek shows "-", a double gameweek lists both opponents.
    `avg_difficulty` averages over the fixtures actually played, so it
    rewards easy runs but not doubles; `fixtures` counts them.
    """
    teams = {t["id"]: t["short_name"] for t in bootstrap["teams"]}
    gameweeks = list(range(start_gw, start_gw + horizon))
    labels = {team: {gw: [] for gw in gameweeks} for team in teams.values()}
    difficulties = {team: [] for team in teams.values()}

    for f in fixtures:
        if f["event"] not in gameweeks:
            continue
        home, away = teams[f["team_h"]], teams[f["team_a"]]
        labels[home][f["event"]].append(f"{away} (H)")
        labels[away][f["event"]].append(f"{home} (A)")
        difficulties[home].append(f["team_h_difficulty"])
        difficulties[away].append(f["team_a_difficulty"])

    rows = []
    for team in teams.values():
        row = {"team": team}
        for gw in gameweeks:
            row[f"GW{gw}"] = ", ".join(labels[team][gw]) or "-"
        played = difficulties[team]
        row["fixtures"] = len(played)
        row["avg_difficulty"] = round(sum(played) / len(played), 2) if played else None
        rows.append(row)
    return pd.DataFrame(rows).sort_values("avg_difficulty").reset_index(drop=True)


def my_team(picks, players):
    """A manager's 15 picks joined to the players table, starters first."""
    # In picks, "position" is the slot (1-11 starters, 12-15 bench), not GKP/DEF/...
    df = pd.DataFrame(picks["picks"]).rename(columns={"element": "id", "position": "slot"})
    team = df.merge(players, on="id", how="left").sort_values("slot")
    team["starter"] = team["slot"] <= 11
    team["captain"] = team["is_captain"].map({True: "C", False: ""})
    team.loc[team["is_vice_captain"], "captain"] = "V"
    return team[
        ["name", "team", "position", "price", "total_points", "form", "status", "captain", "starter"]
    ].reset_index(drop=True)
