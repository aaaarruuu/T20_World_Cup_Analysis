import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings("ignore")

print("=" * 55)
print("  STEP 4 — MACHINE LEARNING MODEL")
print("=" * 55)

df = pd.read_csv("t20_clean.csv")
print(f"\n✅ Loaded {len(df)} clean matches")


all_teams = sorted(set(df["team1"].tolist() + df["team2"].tolist()))
le_winner = LabelEncoder().fit(df["winner"])
df["winner_enc"] = le_winner.transform(df["winner"])

with open("win_rates.json") as f:
    win_rate = json.load(f)

df["team1_winrate"] = df["team1"].map(win_rate)
df["team2_winrate"] = df["team2"].map(win_rate)


FEATURES = [
    "team1_winrate",   # How often team1 wins historically
    "team2_winrate",   # How often team2 wins historically
    "batting_runs",    # Runs scored by team1
    "run_diff",        # How many more runs team1 scored vs team2
]

X = df[FEATURES]         # Feature matrix (inputs)
y = df["winner_enc"]     # Target vector (what to predict)

print(f"\n--- Features used ---")
for f in FEATURES:
    print(f"   {f}")

print(f"\n--- Target ---")
print(f"   winner (encoded as number: 0-{len(le_winner.classes_)-1})")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n--- Train/Test Split ---")
print(f"   Training matches : {len(X_train)} (80%)")
print(f"   Testing matches  : {len(X_test)}  (20%)")

print(f"\n--- Training Random Forest (200 trees) ---")
model = RandomForestClassifier(
    n_estimators=200,   # 200 decision trees
    max_depth=4,        # Each tree can be at most 4 levels deep
    random_state=42     # Makes results reproducible
)
model.fit(X_train, y_train)
print("   ✅ Training complete!")

y_pred   = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n--- Model Accuracy ---")
print(f"   On test data: {accuracy * 100:.2f}%")
print(f"   (This means the model correctly predicted the winner")
print(f"    in {accuracy * 100:.1f}% of test matches)")

cv_scores = cross_val_score(model, X, y, cv=5)
print(f"\n   Cross-Validated Accuracy: {cv_scores.mean() * 100:.1f}%")
print(f"   (More reliable number — averaged over 5 test sets)")

print(f"\n--- Feature Importance ---")
print(f"   (Higher = model relied on this more)")
importance = pd.Series(model.feature_importances_, index=FEATURES)
importance = importance.sort_values(ascending=False)
for feat, val in importance.items():
    bar = "█" * int(val * 50)
    print(f"   {feat:20s} {bar} {val:.3f} ({val*100:.1f}%)")

print(f"\n{'─'*55}")
print(f"  PREDICTING 2026 FINAL: India vs New Zealand")
print(f"{'─'*55}")

india_wr = win_rate.get("India", 0.8)
nz_wr    = win_rate.get("New Zealand", 0.6)
india_avg_2026 = int(
    df[(df["year"] == 2026) & (df["team1"] == "India")]["batting_runs"].mean()
)

print(f"\n   India win rate in dataset  : {india_wr:.2f}  ({india_wr*100:.0f}%)")
print(f"   New Zealand win rate       : {nz_wr:.2f}  ({nz_wr*100:.0f}%)")
print(f"   India avg runs in 2026     : {india_avg_2026}")

final_input = pd.DataFrame(
    [[india_wr, nz_wr, india_avg_2026, 45]],
    columns=FEATURES
)


pred_encoded = model.predict(final_input)[0]
pred_team    = le_winner.inverse_transform([pred_encoded])[0]
probabilities = model.predict_proba(final_input)[0]

print(f"\n   🤖 Model Prediction: {pred_team.upper()}")
print(f"\n   Confidence for each team (top 4):")
top4 = sorted(zip(le_winner.classes_, probabilities),
              key=lambda x: -x[1])[:4]
for team, prob in top4:
    bar = "█" * int(prob * 40)
    print(f"   {team:15s} {bar} {prob*100:.1f}%")

print(f"\n   NOTE: The 2026 final is India vs New Zealand")
print(f"   on March 8, 2026 at Narendra Modi Stadium, Ahmedabad.")

all_preds = model.predict(X)
df["predicted_winner_enc"] = all_preds
df["predicted_winner"] = le_winner.inverse_transform(all_preds)
df["prediction_correct"] = (df["winner_enc"] == df["predicted_winner_enc"]).astype(int)

df[["year", "round", "team1", "team2", "winner",
    "predicted_winner", "prediction_correct"]].to_csv(
    "t20_predictions.csv", index=False
)
print(f"\n   ✅ Predictions saved: t20_predictions.csv")
print(f"      (Use this in Power BI to show model accuracy visually)")

print("\n" + "=" * 55)
print("  STEP 4 DONE — Run step5_export_powerbi.py next")
print("=" * 55)
