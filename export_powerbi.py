import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

print("=" * 55)
print("  STEP 5 — EXPORT DATA FOR POWER BI")
print("=" * 55)

df    = pd.read_csv("t20_data.csv")
preds = pd.read_csv("t20_predictions.csv")

def parse_runs(s):
    try:
        return int(str(s).split("/")[0])
    except:
        return 0

df["batting_runs"] = df["team1_score"].apply(parse_runs)
df["chasing_runs"]  = df["team2_score"].apply(parse_runs)
df["run_diff"]      = df["batting_runs"] - df["chasing_runs"]

with open("win_rates.json") as f:
    win_rate = json.load(f)

print(f"\n✅ Data loaded: {len(df)} matches")

def get_win_count(team, dataframe):
    """Returns how many times a team won in the dataset"""
    return int(dataframe["winner"].value_counts().get(team, 0))

all_matches = df[[
    "match_id", "year", "round",
    "team1", "team2", "winner",
    "venue", "city",
    "team1_score", "team2_score", "margin",
    "batting_runs", "chasing_runs", "run_diff",
    "player_of_match"
]].copy()
print(f"[Table 1] all_matches       — {len(all_matches)} rows")

win_counts = (
    df["winner"]
    .value_counts()
    .reset_index()
)
win_counts.columns = ["team", "wins"]
win_counts["win_rate_pct"] = win_counts["team"].map(
    lambda t: round(win_rate.get(t, 0) * 100, 1)
)
win_counts = win_counts.sort_values("wins", ascending=False)
print(f"[Table 2] win_counts        — {len(win_counts)} rows")

avg_runs = (
    df.groupby(["year", "team1"])["batting_runs"]
    .mean()
    .reset_index()
)
avg_runs.columns = ["year", "team", "avg_runs"]
avg_runs["avg_runs"] = avg_runs["avg_runs"].round(1)
print(f"[Table 3] avg_runs          — {len(avg_runs)} rows")

top_players = (
    df["player_of_match"]
    .value_counts()
    .reset_index()
)
top_players.columns = ["player", "awards"]

player_team_map = {}
for _, row in df.iterrows():
    p = row["player_of_match"]
    if p not in player_team_map:
        player_team_map[p] = row["winner"]
top_players["team"] = top_players["player"].map(player_team_map)
print(f"[Table 4] top_players       — {len(top_players)} rows")

year_summary = df.groupby("year").agg(
    total_matches   = ("match_id",      "count"),
    avg_runs_scored = ("batting_runs",  "mean"),
    highest_score   = ("batting_runs",  "max"),
    lowest_score    = ("batting_runs",  "min"),
).reset_index()
year_summary["avg_runs_scored"] = year_summary["avg_runs_scored"].round(1)
print(f"[Table 5] year_summary      — {len(year_summary)} rows")

model_results = preds.copy()
print(f"[Table 6] model_predictions — {len(model_results)} rows")

wr_table = pd.DataFrame([
    {
        "team":         team,
        "win_rate_pct": round(rate * 100, 1),
        "total_wins":   get_win_count(team, df)
    }
    for team, rate in win_rate.items()
])
wr_table = wr_table.sort_values("win_rate_pct", ascending=False).reset_index(drop=True)
print(f"[Table 7] win_rates_table   — {len(wr_table)} rows")

output_file = "t20_powerbi_data.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    all_matches.to_excel(writer,   sheet_name="all_matches",        index=False)
    win_counts.to_excel(writer,    sheet_name="win_counts",         index=False)
    avg_runs.to_excel(writer,      sheet_name="avg_runs",           index=False)
    top_players.to_excel(writer,   sheet_name="top_players",        index=False)
    year_summary.to_excel(writer,  sheet_name="year_summary",       index=False)
    model_results.to_excel(writer, sheet_name="model_predictions",  index=False)
    wr_table.to_excel(writer,      sheet_name="win_rates",          index=False)

print(f"\n✅ SAVED: {output_file}")
print(f"\n   7 sheets ready for Power BI:")
print(f"   Sheet 1 → all_matches         (main data, use for slicers)")
print(f"   Sheet 2 → win_counts          (bar chart: wins per team)")
print(f"   Sheet 3 → avg_runs            (line chart: runs over years)")
print(f"   Sheet 4 → top_players         (bar chart: best performers)")
print(f"   Sheet 5 → year_summary        (KPI cards: key stats)")
print(f"   Sheet 6 → model_predictions   (model accuracy visual)")
print(f"   Sheet 7 → win_rates           (win rate per team)")

print("\n" + "=" * 55)
print("  DONE! Now open Power BI Desktop.")
print("  Home → Get Data → Excel → t20_powerbi_data.xlsx")
print("  Load all 7 sheets and build your dashboard.")
print("=" * 55)
