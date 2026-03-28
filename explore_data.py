import pandas as pd

print("=" * 55)
print("  STEP 1 — LOAD & EXPLORE DATA")
print("=" * 55)

df = pd.read_csv("t20_data.csv")

print("\n✅ File loaded successfully!")
print(f"   Total rows    : {df.shape[0]}  (each row = one match)")
print(f"   Total columns : {df.shape[1]}  (each column = one feature)")

print("\n--- First 5 Rows of Data ---")
print(df.head())

print("\n--- Column Names ---")
for col in df.columns:
    print(f"   {col}")

print("\n--- Data Types (int=number, object=text) ---")
print(df.dtypes)

print("\n--- Missing Values per Column ---")
missing = df.isnull().sum()
print(missing)
if missing.sum() == 0:
    print("   ✅ No missing values found!")
else:
    print(f"   ⚠  Total missing: {missing.sum()}")

print("\n--- Unique Years (Tournaments) ---")
print(sorted(df["year"].unique()))

print("\n--- All Teams ---")
all_teams = sorted(set(df["team1"].tolist() + df["team2"].tolist()))
print(all_teams)

print("\n--- Match Rounds ---")
print(df["round"].unique())

print("\n--- Winners (unique) ---")
print(sorted(df["winner"].unique()))

print("\n" + "=" * 55)
print("  STEP 1 DONE — Data looks good! Run step2 next.")
print("=" * 55)
