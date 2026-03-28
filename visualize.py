import pandas as pd
import matplotlib
matplotlib.use("Agg")         
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

print("=" * 55)
print("  STEP 3 — CREATE VISUALIZATIONS (5 CHARTS)")
print("=" * 55)


df = pd.read_csv("t20_clean.csv")
print(f"\n✅ Loaded clean data: {len(df)} matches")


os.makedirs("charts", exist_ok=True)

BG    = "#0a0e1a"   # very dark navy — slide background
CARD  = "#111827"   # slightly lighter — chart area
CYAN  = "#00d4ff"   # bright blue accent
ORANGE= "#ff6b35"   # orange accent
GOLD  = "#ffd700"   # gold for India
GREEN = "#39ff14"   # neon green
RED   = "#ff4444"   # red
PURPLE= "#bd93f9"   # purple

def style_ax(ax):
    """Apply consistent dark styling to any axis"""
    ax.set_facecolor(CARD)
    ax.tick_params(colors="white", labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", color="#2a3a55", alpha=0.4, zorder=0)

# ════════════════════════════════════════════════════════
# CHART 1: Total wins per team (bar chart)
# ════════════════════════════════════════════════════════
print("\n[Chart 1] Creating: Total Wins per Team ...")

fig, ax = plt.subplots(figsize=(13, 5), facecolor=BG)
style_ax(ax)

wins = df["winner"].value_counts()
# Color India gold, other top teams cyan, rest orange
bar_colors = []
for team in wins.index:
    if team == "India":
        bar_colors.append(GOLD)
    elif team in ["England", "New Zealand", "Australia"]:
        bar_colors.append(CYAN)
    else:
        bar_colors.append(ORANGE)

bars = ax.bar(wins.index, wins.values,
              color=bar_colors, edgecolor=BG, linewidth=1.5, zorder=3)

ax.set_title("Total Wins per Team — T20 World Cup 2022, 2024 & 2026*",
             color="white", fontsize=13, fontweight="bold", pad=14)
ax.set_xlabel("Team", color="#8899aa", fontsize=11)
ax.set_ylabel("Number of Wins", color="#8899aa", fontsize=11)
ax.set_xticklabels(wins.index, rotation=35, ha="right", color="white")

# Add value labels on top of each bar
for bar, val in zip(bars, wins.values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(val), ha="center", color="white",
            fontweight="bold", fontsize=11, zorder=4)

ax.text(0.99, 0.97, "*2026 data up to semi-finals",
        transform=ax.transAxes, color="#6b7a99",
        fontsize=9, ha="right", va="top", style="italic")

plt.tight_layout()
plt.savefig("charts/chart1_wins.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("   ✅ Saved: charts/chart1_wins.png")

# ════════════════════════════════════════════════════════
# CHART 2: Year-wise wins by top 5 teams (grouped bar)
# ════════════════════════════════════════════════════════
print("[Chart 2] Creating: Year-wise Wins by Top Teams ...")

fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
style_ax(ax)

top_teams = ["India", "England", "New Zealand", "South Africa", "Australia"]
year_team = df.groupby(["year", "winner"]).size().unstack(fill_value=0)
plot_cols  = [t for t in top_teams if t in year_team.columns]
colors_yw  = [GOLD, CYAN, ORANGE, RED, PURPLE][:len(plot_cols)]

year_team[plot_cols].plot(
    kind="bar", ax=ax, color=colors_yw,
    edgecolor=BG, linewidth=1, zorder=3
)
ax.set_title("Wins by Top Teams per Tournament Year",
             color="white", fontsize=13, fontweight="bold")
ax.set_xlabel("Year", color="#8899aa")
ax.set_ylabel("Wins", color="#8899aa")
ax.tick_params(colors="white", labelrotation=0)
ax.legend(facecolor=CARD, edgecolor="#2a3a55",
          labelcolor="white", fontsize=10)

plt.tight_layout()
plt.savefig("charts/chart2_yearwise.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("   ✅ Saved: charts/chart2_yearwise.png")

# ════════════════════════════════════════════════════════
# CHART 3: Average runs scored per team (horizontal bar)
# ════════════════════════════════════════════════════════
print("[Chart 3] Creating: Average Runs per Team ...")

fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
ax.set_facecolor(CARD)
ax.tick_params(colors="white", labelsize=10)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.grid(axis="x", color="#2a3a55", alpha=0.4)

avg = (df.groupby("team1")["batting_runs"]
         .mean()
         .sort_values(ascending=True)
         .tail(12))

bar_colors3 = [GOLD if t == "India" else CYAN for t in avg.index]
bars3 = ax.barh(avg.index, avg.values,
                color=bar_colors3, edgecolor=BG)

ax.set_title("Average Runs Scored per Team (T20 WC 2022–2026)",
             color="white", fontsize=13, fontweight="bold")
ax.set_xlabel("Average Runs", color="#8899aa")

for bar, val in zip(bars3, avg.values):
    ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
            f"{val:.0f}", va="center", color="white",
            fontweight="bold", fontsize=10)

plt.tight_layout()
plt.savefig("charts/chart3_avg_runs.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("   ✅ Saved: charts/chart3_avg_runs.png")

# ════════════════════════════════════════════════════════
# CHART 4: 2026 — matches per round (bar chart)
# ════════════════════════════════════════════════════════
print("[Chart 4] Creating: 2026 Matches per Round ...")

fig, ax = plt.subplots(figsize=(8, 5), facecolor=BG)
style_ax(ax)

rounds = df[df["year"] == 2026]["round"].value_counts()
round_colors = [GOLD, CYAN, ORANGE, GREEN][:len(rounds)]

bars4 = ax.bar(rounds.index, rounds.values,
               color=round_colors, edgecolor=BG, linewidth=1.5, zorder=3)

ax.set_title("T20 WC 2026 — Matches Played per Round",
             color="white", fontsize=13, fontweight="bold")
ax.set_xlabel("Round", color="#8899aa")
ax.set_ylabel("Number of Matches", color="#8899aa")
ax.tick_params(colors="white")

for bar, val in zip(bars4, rounds.values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1, str(val),
            ha="center", color="white", fontweight="bold", fontsize=13)

plt.tight_layout()
plt.savefig("charts/chart4_rounds.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("   ✅ Saved: charts/chart4_rounds.png")

# ════════════════════════════════════════════════════════
# CHART 5: Top players of the match (bar chart)
# ════════════════════════════════════════════════════════
print("[Chart 5] Creating: Top Players of the Match ...")

fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
style_ax(ax)

top_p = df["player_of_match"].value_counts().head(8)
player_colors = [GOLD, CYAN, ORANGE, GREEN, PURPLE, CYAN, GOLD, ORANGE]

bars5 = ax.bar(top_p.index, top_p.values,
               color=player_colors, edgecolor=BG, linewidth=1.5, zorder=3)

ax.set_title("Top Players of the Match — T20 WC 2022, 2024 & 2026",
             color="white", fontsize=13, fontweight="bold")
ax.set_xlabel("Player", color="#8899aa")
ax.set_ylabel("Player of Match Awards", color="#8899aa")
ax.set_xticklabels(top_p.index, rotation=30, ha="right",
                   color="white", fontsize=9)

for bar, val in zip(bars5, top_p.values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05, str(val),
            ha="center", color="white", fontweight="bold", fontsize=12)

plt.tight_layout()
plt.savefig("charts/chart5_players.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("   ✅ Saved: charts/chart5_players.png")

# ════════════════════════════════════════════════════════
# BONUS CHART 6: India's performance across all 3 years
# ════════════════════════════════════════════════════════
print("[Chart 6] Creating: India Performance Across Years ...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor=BG)

# Left: India wins per year
india_wins = (df[df["winner"] == "India"]
              .groupby("year").size()
              .reset_index(name="wins"))
axes[0].set_facecolor(CARD)
bars6 = axes[0].bar(india_wins["year"].astype(str),
                    india_wins["wins"], color=GOLD,
                    edgecolor=BG, linewidth=2)
axes[0].set_title("India Wins per Year", color="white",
                  fontsize=12, fontweight="bold")
axes[0].set_xlabel("Year", color="#8899aa")
axes[0].set_ylabel("Wins", color="#8899aa")
axes[0].tick_params(colors="white")
for sp in axes[0].spines.values():
    sp.set_visible(False)
axes[0].grid(axis="y", color="#2a3a55", alpha=0.4)
for bar, val in zip(bars6, india_wins["wins"]):
    axes[0].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.1, str(val),
                 ha="center", color="white", fontweight="bold", fontsize=14)

# Right: India avg runs per year
india_runs = (df[df["team1"] == "India"]
              .groupby("year")["batting_runs"]
              .mean()
              .reset_index())
axes[1].set_facecolor(CARD)
axes[1].plot(india_runs["year"].astype(str),
             india_runs["batting_runs"],
             color=GOLD, marker="o", linewidth=3,
             markersize=10, markerfacecolor=ORANGE)
for x, y in zip(india_runs["year"].astype(str), india_runs["batting_runs"]):
    axes[1].text(x, y + 3, f"{y:.0f}", ha="center",
                 color="white", fontweight="bold", fontsize=12)
axes[1].set_title("India Avg Runs per Year", color="white",
                  fontsize=12, fontweight="bold")
axes[1].set_xlabel("Year", color="#8899aa")
axes[1].set_ylabel("Avg Runs", color="#8899aa")
axes[1].tick_params(colors="white")
for sp in axes[1].spines.values():
    sp.set_visible(False)
axes[1].grid(axis="y", color="#2a3a55", alpha=0.4)

plt.suptitle("India's T20 World Cup Performance (2022–2026)",
             color="white", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("charts/chart6_india_perf.png", dpi=150,
            bbox_inches="tight", facecolor=BG)
plt.close()
print("   ✅ Saved: charts/chart6_india_perf.png")

print("\n" + "=" * 55)
print("  STEP 3 DONE — 6 charts saved in /charts folder")
print("  Run step4_ml_model.py next")
print("=" * 55)
