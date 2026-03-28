import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("=" * 55)
print("  STEP 2 — CLEAN & PREPARE DATA")
print("=" * 55)

df = pd.read_csv("t20_data.csv")
print(f"\n✅ Loaded {len(df)} matches")

before = len(df)
df = df.drop_duplicates()
print(f"\n[2A] Duplicates removed: {before - len(df)}")

df = df.fillna("Unknown")
print(f"[2B] Missing values after fill: {df.isnull().sum().sum()}")

def parse_runs(score_string):
    """
    Takes a score like "200/3" or "148/7"
    Returns just the runs: 200 or 148
    If it can't parse, returns 0
    """
    try:
        return int(str(score_string).split("/")[0])
    except:
        return 0

df["batting_runs"] = df["team1_score"].apply(parse_runs)
df["chasing_runs"] = df["team2_score"].apply(parse_runs)
print(f"\n[2C] Score parsing done")
print(f"     Example: '200/3' → {parse_runs('200/3')} runs")
print(f"     Example: '148/7' → {parse_runs('148/7')} runs")

df["run_diff"] = df["batting_runs"] - df["chasing_runs"]

df["team1_won"] = (df["winner"] == df["team1"]).astype(int)

win_counts = df["winner"].value_counts().to_dict()
total_per_team = {}
for _, row in df.iterrows():
    for t in [row["team1"], row["team2"]]:
        total_per_team[t] = total_per_team.get(t, 0) + 1

win_rate = {
    team: round(win_counts.get(team, 0) / total_per_team[team], 3)
    for team in total_per_team
}

df["team1_winrate"] = df["team1"].map(win_rate)
df["team2_winrate"] = df["team2"].map(win_rate)
print(f"\n[2D] New features created:")
print(f"     - batting_runs  : runs scored by team1")
print(f"     - chasing_runs  : runs scored by team2")
print(f"     - run_diff      : batting_runs minus chasing_runs")
print(f"     - team1_won     : 1 if team1 won, 0 if team2 won")
print(f"     - team1_winrate : historical win % of team1")
print(f"     - team2_winrate : historical win % of team2")


all_teams = sorted(set(df["team1"].tolist() + df["team2"].tolist()))
le_team   = LabelEncoder().fit(all_teams)    # for team names
le_city   = LabelEncoder().fit(df["city"])   # for city names
le_winner = LabelEncoder().fit(df["winner"]) # for winner (this is our TARGET)

df["team1_enc"]  = le_team.transform(df["team1"])
df["team2_enc"]  = le_team.transform(df["team2"])
df["city_enc"]   = le_city.transform(df["city"])
df["winner_enc"] = le_winner.transform(df["winner"])

print(f"\n[2E] Label Encoding done:")
print(f"     Teams encoded: {dict(zip(le_team.classes_, le_team.transform(le_team.classes_)))}")

df.to_csv("t20_clean.csv", index=False)
print(f"\n[2F] ✅ Clean data saved as: t20_clean.csv")
print(f"     Columns now: {list(df.columns)}")

import json
with open("win_rates.json", "w") as f:
    json.dump(win_rate, f, indent=2)
print(f"     Win rates saved as: win_rates.json")

print("\n--- Top 5 Teams by Win Rate ---")
top_wr = sorted(win_rate.items(), key=lambda x: -x[1])[:5]
for team, rate in top_wr:
    bar = "█" * int(rate * 20)
    print(f"   {team:15s} {bar} {rate:.1%}")

print("\n" + "=" * 55)
print("  STEP 2 DONE — Run step3_visualize.py next")
print("=" * 55)
