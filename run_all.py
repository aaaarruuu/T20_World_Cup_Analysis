import subprocess
import sys
import time

steps = [
    ("step1_explore_data.py",  "Load & Explore Data"),
    ("step2_clean_data.py",    "Clean & Prepare Data"),
    ("step3_visualize.py",     "Create 6 Charts"),
    ("step4_ml_model.py",      "Build ML Model"),
    ("step5_export_powerbi.py","Export for Power BI"),
]

print("=" * 60)
print("  T20 WC 2026 BIG DATA PROJECT — RUN ALL STEPS")
print("=" * 60)

all_passed = True

for filename, description in steps:
    print(f"\n{'─'*60}")
    print(f"  Running: {description}  ({filename})")
    print(f"{'─'*60}")
    time.sleep(0.3)

    result = subprocess.run(
        [sys.executable, filename],
        capture_output=False,
        text=True
    )

    if result.returncode == 0:
        print(f"\n  ✅ {description} — PASSED")
    else:
        print(f"\n  ❌ {description} — FAILED")
        all_passed = False
        print(f"  Fix the error above and run again.")
        break

print("\n" + "=" * 60)
if all_passed:
    print("  🎉 ALL STEPS COMPLETE!")
    print()
    print("  Files created:")
    print("    t20_clean.csv             ← cleaned dataset")
    print("    win_rates.json            ← team win rates")
    print("    t20_predictions.csv       ← ML model predictions")
    print("    t20_powerbi_data.xlsx     ← 7 sheets for Power BI")
    print("    charts/chart1_wins.png    ← wins per team")
    print("    charts/chart2_yearwise.png← year-wise wins")
    print("    charts/chart3_avg_runs.png← avg runs")
    print("    charts/chart4_rounds.png  ← 2026 rounds")
    print("    charts/chart5_players.png ← top players")
    print("    charts/chart6_india_perf.png ← India stats")
    print()
    print("  NEXT STEP: Open Power BI Desktop")
    print("  Load: t20_powerbi_data.xlsx")
else:
    print("  ⚠  Some steps failed — fix errors and try again")
print("=" * 60)
