# 🏏 T20 World Cup 2026 — Big Data Analytics & Prediction

> A complete Big Data Analytics project that predicted India as the T20 WC 2026 champion with **96.1% confidence** — validated by the real result on March 8, 2026.

---

## Project Overview

This project applies Big Data Analytics and Machine Learning to ICC T20 World Cup data (2022, 2024, 2026) to:
- Analyse batting trends, team win rates, and player performance
- Build a Random Forest classifier to predict match winners
- Generate 6 professional charts via Python
- Export a 7-sheet Excel file for a live Power BI dashboard

**Built as an MCA Semester 2 project — Big Data Analytics.**

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| Pandas | Data loading, cleaning, feature engineering |
| Scikit-learn | Random Forest ML model |
| Matplotlib + Seaborn | Chart generation (6 charts) |
| OpenPyXL | Excel export for Power BI |
| Microsoft Power BI | Interactive live dashboard |

---

## Dataset

- **59 real verified matches** — ICC T20 WC 2022 (Australia), 2024 (West Indies/USA), 2026 (India)
- Source: ESPN Cricinfo
- **12 features**: teams, scores, toss, venue, city, round, player of match

---

## ML Model Results

```
Algorithm:          Random Forest Classifier
Trees:              200
Train/Test split:   80% / 20%
Test accuracy:      75.0%
Cross-val accuracy: 68.0%

Top feature by importance:
  Team win rate     50.2%
  Runs scored       20.5%
  Opponent rating   16.5%
  Run difference    12.7%
```

### 2026 Final Prediction

```
Match:   India vs New Zealand
Venue:   Narendra Modi Stadium, Ahmedabad
Date:    March 8, 2026

Model prediction:   INDIA  (96.1% confidence)
Actual winner:      INDIA  ✅ VALIDATED
```

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/t20-analytics.git
cd t20-analytics
```

**2. Install dependencies**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

**3. Run everything at once**
```bash
python run_all.py
```

Or run step by step:
```bash
python step1_explore_data.py     # explore dataset
python step2_clean_data.py       # clean and feature engineer
python step3_visualize.py        # generate 6 charts → /charts/
python step4_ml_model.py         # train model, predict 2026 final
python step5_export_powerbi.py   # export Excel for Power BI
```

---

## Output Files

| File | Description |
|------|-------------|
| `t20_clean.csv` | Cleaned dataset with engineered features |
| `win_rates.json` | Team win rates computed from data |
| `t20_predictions.csv` | Model predictions for all matches |
| `t20_powerbi_data.xlsx` | 7-sheet Excel file for Power BI |
| `charts/` | 6 PNG chart images |

---

## Power BI Dashboard

Load `t20_powerbi_data.xlsx` in Power BI Desktop:

1. Home → Get Data → Excel Workbook → select the file
2. Load all 7 sheets
3. Build 5 visuals: bar chart (wins), line chart (avg runs), donut (rounds), horizontal bar (top players), KPI cards
4. Add a **Year slicer** — clicking 2022/2024/2026 filters all visuals live

---

## Project Structure

```
t20-analytics/
├── t20_data.csv                  ← real dataset (59 matches)
├── step1_explore_data.py
├── step2_clean_data.py
├── step3_visualize.py
├── step4_ml_model.py
├── step5_export_powerbi.py
├── run_all.py                    ← run all steps at once
├── t20_powerbi_data.xlsx         ← Power BI ready Excel
└── charts/
    ├── chart1_wins.png
    ├── chart2_yearwise.png
    ├── chart3_avg_runs.png
    ├── chart4_rounds.png
    ├── chart5_players.png
    └── chart6_india_perf.png
```

---

## License

MIT License — free to use and modify.

---

*Built with Python · Scikit-learn · Power BI | MCA Sem 2 — Big Data Analytics*
