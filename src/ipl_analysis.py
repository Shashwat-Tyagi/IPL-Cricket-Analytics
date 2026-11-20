"""
ipl_analysis.py  -  Complete IPL Cricket Data Analysis
=======================================================
Run from project root:
    python src/ipl_analysis.py

Outputs all plots to outputs/plots/ directory.
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings("ignore")
matplotlib.use("Agg")          # non-interactive backend - works in scripts & notebooks

# -------------------- Paths --------------------
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "data")
PLOTS_DIR   = os.path.join(BASE_DIR, "outputs", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# -------------------- Design System --------------------
PALETTE = ["#4ECDC4", "#FF6B6B", "#FFD93D", "#A29BFE", "#6BCB77",
           "#F9844A", "#45B7D1", "#C9ADA7"]

BG_COLOR   = "#0F0F1A"
TEXT_COLOR = "#E8E8F0"
GRID_COLOR = "#2A2A3E"
ACCENT     = "#4ECDC4"

sns.set_theme(style="dark", rc={
    "figure.facecolor":  BG_COLOR,
    "axes.facecolor":    "#16213E",
    "axes.edgecolor":    GRID_COLOR,
    "axes.labelcolor":   TEXT_COLOR,
    "axes.titlecolor":   TEXT_COLOR,
    "xtick.color":       TEXT_COLOR,
    "ytick.color":       TEXT_COLOR,
    "grid.color":        GRID_COLOR,
    "text.color":        TEXT_COLOR,
    "font.family":       "DejaVu Sans",
})

def save(fig: plt.Figure, name: str) -> None:
    path = os.path.join(PLOTS_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"   [SAVED] {name}")


# -------------------- 1. Load Data --------------------
def load_data():
    matches_path   = os.path.join(DATA_DIR, "ipl_matches.csv")
    deliveries_path = os.path.join(DATA_DIR, "ipl_deliveries.csv")

    if not os.path.exists(matches_path) or not os.path.exists(deliveries_path):
        raise FileNotFoundError(
            "Dataset not found.\n"
            "Please run:  python src/generate_data.py  first."
        )

    matches    = pd.read_csv(matches_path, parse_dates=["date"])
    deliveries = pd.read_csv(deliveries_path)
    return matches, deliveries


# -------------------- 2. Clean Data --------------------
def clean_data(matches: pd.DataFrame, deliveries: pd.DataFrame):
    # Matches
    matches["winner"].fillna("No Result", inplace=True)
    matches["player_of_match"].fillna("Unknown", inplace=True)
    matches.drop_duplicates(subset="id", inplace=True)

    # Deliveries
    deliveries.dropna(subset=["match_id", "inning", "batsman_runs"], inplace=True)
    deliveries["total_runs"] = deliveries["total_runs"].astype(int)
    deliveries["batsman_runs"] = deliveries["batsman_runs"].astype(int)
    return matches, deliveries


# -------------------- 3. Analyses --------------------

# 3.1  Season-wise match count
def plot_season_matches(matches: pd.DataFrame):
    print("\n[*] Season-wise Matches...")
    season_counts = matches.groupby("season").size().reset_index(name="matches")

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(season_counts["season"], season_counts["matches"],
                  color=PALETTE[:len(season_counts)], edgecolor="none", width=0.6)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(int(bar.get_height())), ha="center", va="bottom",
                color=TEXT_COLOR, fontsize=10, fontweight="bold")
    ax.set_title("IPL Matches Per Season", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Season", fontsize=12)
    ax.set_ylabel("Number of Matches", fontsize=12)
    ax.grid(axis="y", alpha=0.3)
    ax.set_xticks(season_counts["season"])
    fig.tight_layout()
    save(fig, "01_season_matches.png")


# 3.2  Team wins (overall)
def plot_team_wins(matches: pd.DataFrame):
    print("[*] Team Wins...")
    wins = (matches[matches["winner"] != "No Result"]
            .groupby("winner").size()
            .sort_values(ascending=False)
            .head(8))

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(wins.index[::-1], wins.values[::-1],
                   color=PALETTE[:len(wins)], edgecolor="none")
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1, bar.get_y() + bar.get_height() / 2,
                str(int(w)), va="center", color=TEXT_COLOR, fontsize=10, fontweight="bold")
    ax.set_title("Total IPL Wins by Team", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Total Wins", fontsize=12)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    save(fig, "02_team_wins.png")


# 3.3  Top run-scorers
def plot_top_batsmen(deliveries: pd.DataFrame):
    print("[*] Top Batsmen...")
    top = (deliveries.groupby("batsman")["batsman_runs"]
           .sum()
           .sort_values(ascending=False)
           .head(12))

    fig, ax = plt.subplots(figsize=(13, 6))
    bars = ax.bar(top.index, top.values,
                  color=sns.color_palette("viridis", len(top)),
                  edgecolor="none")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                f"{int(bar.get_height()):,}", ha="center", va="bottom",
                color=TEXT_COLOR, fontsize=9, fontweight="bold")
    ax.set_title("Top 12 Run-Scorers in IPL", fontsize=16, fontweight="bold", pad=15)
    ax.set_ylabel("Total Runs", fontsize=12)
    ax.set_xticklabels(top.index, rotation=35, ha="right", fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    save(fig, "03_top_batsmen.png")


# 3.4  Top wicket-takers
def plot_top_bowlers(deliveries: pd.DataFrame):
    print("[*] Top Bowlers...")
    top = (deliveries[deliveries["player_dismissed"].notna()]
           .groupby("bowler").size()
           .sort_values(ascending=False)
           .head(12))

    fig, ax = plt.subplots(figsize=(13, 6))
    bars = ax.bar(top.index, top.values,
                  color=sns.color_palette("rocket_r", len(top)),
                  edgecolor="none")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(int(bar.get_height())), ha="center", va="bottom",
                color=TEXT_COLOR, fontsize=9, fontweight="bold")
    ax.set_title("Top 12 Wicket-Takers in IPL", fontsize=16, fontweight="bold", pad=15)
    ax.set_ylabel("Total Wickets", fontsize=12)
    ax.set_xticklabels(top.index, rotation=35, ha="right", fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    save(fig, "04_top_bowlers.png")


# 3.5  Toss Decision Analysis
def plot_toss_analysis(matches: pd.DataFrame):
    print("[*] Toss Analysis...")
    toss_won_match = matches[matches["toss_winner"] == matches["winner"]]
    toss_wins = len(toss_won_match)
    toss_loss = len(matches[matches["winner"] != "No Result"]) - toss_wins

    # Subplot: toss decision distribution + toss outcome
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Pie - toss decision
    decision_counts = matches["toss_decision"].value_counts()
    axes[0].pie(decision_counts, labels=["Field First", "Bat First"],
                autopct="%1.1f%%", colors=[PALETTE[0], PALETTE[1]],
                textprops={"color": TEXT_COLOR, "fontsize": 12},
                startangle=90, pctdistance=0.75,
                wedgeprops={"edgecolor": BG_COLOR, "linewidth": 2})
    axes[0].set_title("Toss Decision: Bat vs Field", fontsize=14, fontweight="bold")

    # Pie - toss impact on result
    axes[1].pie([toss_wins, toss_loss],
                labels=["Toss Winner Won", "Toss Winner Lost"],
                autopct="%1.1f%%", colors=[PALETTE[2], PALETTE[3]],
                textprops={"color": TEXT_COLOR, "fontsize": 12},
                startangle=90, pctdistance=0.75,
                wedgeprops={"edgecolor": BG_COLOR, "linewidth": 2})
    axes[1].set_title("Did Winning Toss Help Win the Match?", fontsize=14, fontweight="bold")

    fig.suptitle("Toss Analysis", fontsize=18, fontweight="bold", y=1.02)
    fig.tight_layout()
    save(fig, "05_toss_analysis.png")


# 3.6  Runs per over (scoring pattern)
def plot_runs_per_over(deliveries: pd.DataFrame):
    print("[*] Scoring Pattern per Over...")
    over_runs = (deliveries.groupby("over")["total_runs"]
                 .mean()
                 .reset_index()
                 .rename(columns={"total_runs": "avg_runs"}))
    over_runs = over_runs[over_runs["over"] <= 20]

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.fill_between(over_runs["over"], over_runs["avg_runs"],
                    alpha=0.25, color=ACCENT)
    ax.plot(over_runs["over"], over_runs["avg_runs"],
            color=ACCENT, linewidth=2.5, marker="o", markersize=5)
    ax.axvline(6, color="#FF6B6B", linestyle="--", alpha=0.7, label="End of Powerplay (Ov 6)")
    ax.axvline(15, color="#FFD93D", linestyle="--", alpha=0.7, label="Death Overs start (Ov 15)")
    ax.set_title("Average Runs Per Over - Scoring Pattern", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Over", fontsize=12)
    ax.set_ylabel("Avg Runs", fontsize=12)
    ax.set_xticks(range(1, 21))
    ax.legend(fontsize=10, facecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    save(fig, "06_runs_per_over.png")


# 3.7  Top venues by average score
def plot_venue_analysis(deliveries: pd.DataFrame, matches: pd.DataFrame):
    print("[*] Venue Analysis...")
    # Merge venue into deliveries
    df = deliveries.merge(matches[["id", "venue"]], left_on="match_id", right_on="id")
    venue_scores = (df.groupby(["match_id", "venue", "inning"])["total_runs"]
                    .sum()
                    .reset_index())
    # First innings only (batting score)
    first_inn = venue_scores[venue_scores["inning"] == 1]
    top_venues = (first_inn.groupby("venue")["total_runs"]
                  .mean()
                  .sort_values(ascending=False)
                  .head(8))

    fig, ax = plt.subplots(figsize=(13, 6))
    colors = sns.color_palette("crest", len(top_venues))
    bars = ax.bar(top_venues.index, top_venues.values,
                  color=colors, edgecolor="none")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{bar.get_height():.0f}", ha="center", va="bottom",
                color=TEXT_COLOR, fontsize=10, fontweight="bold")
    ax.set_title("Top Venues by Average 1st Innings Score", fontsize=16, fontweight="bold", pad=15)
    ax.set_ylabel("Average Runs", fontsize=12)
    ax.set_xticklabels(top_venues.index, rotation=30, ha="right", fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    save(fig, "07_venue_analysis.png")


# 3.8  Player of the Match (most awards)
def plot_pom_awards(matches: pd.DataFrame):
    print("[*] Player of the Match Awards...")
    pom = (matches[matches["player_of_match"] != "Unknown"]
           .groupby("player_of_match").size()
           .sort_values(ascending=False)
           .head(12))

    fig, ax = plt.subplots(figsize=(13, 6))
    bars = ax.bar(pom.index, pom.values,
                  color=sns.color_palette("magma", len(pom)),
                  edgecolor="none")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                str(int(bar.get_height())), ha="center", va="bottom",
                color=TEXT_COLOR, fontsize=10, fontweight="bold")
    ax.set_title("Most Player of the Match Awards", fontsize=16, fontweight="bold", pad=15)
    ax.set_ylabel("Awards", fontsize=12)
    ax.set_xticklabels(pom.index, rotation=35, ha="right", fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    save(fig, "08_pom_awards.png")


# 3.9  Win Margin distribution (runs & wickets)
def plot_win_margins(matches: pd.DataFrame):
    print("[*] Win Margin Distribution...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    run_wins = matches[matches["win_by_runs"] > 0]["win_by_runs"]
    wkt_wins = matches[matches["win_by_wickets"] > 0]["win_by_wickets"]

    sns.histplot(run_wins, bins=20, kde=True, color=PALETTE[0], ax=axes[0],
                 edgecolor="none", line_kws={"linewidth": 2})
    axes[0].set_title("Wins by Runs - Distribution", fontsize=14, fontweight="bold")
    axes[0].set_xlabel("Winning Margin (Runs)", fontsize=12)
    axes[0].grid(alpha=0.3)

    sns.histplot(wkt_wins, bins=10, kde=True, color=PALETTE[1], ax=axes[1],
                 edgecolor="none", line_kws={"linewidth": 2})
    axes[1].set_title("Wins by Wickets - Distribution", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Winning Margin (Wickets)", fontsize=12)
    axes[1].grid(alpha=0.3)

    fig.suptitle("Win Margin Analysis", fontsize=17, fontweight="bold")
    fig.tight_layout()
    save(fig, "09_win_margins.png")


# 3.10  Season-wise top run-scorer heatmap
def plot_batsmen_heatmap(deliveries: pd.DataFrame, matches: pd.DataFrame):
    print("[*] Batsman x Season Heatmap...")
    df = deliveries.merge(matches[["id", "season"]], left_on="match_id", right_on="id")
    pivot = (df.groupby(["batsman", "season"])["batsman_runs"]
             .sum()
             .unstack(fill_value=0))

    # Keep only top 12 batsmen overall
    top_batsmen = df.groupby("batsman")["batsman_runs"].sum().nlargest(12).index
    pivot = pivot.loc[pivot.index.intersection(top_batsmen)]

    fig, ax = plt.subplots(figsize=(15, 7))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd",
                linewidths=0.5, linecolor=BG_COLOR,
                cbar_kws={"label": "Runs"},
                ax=ax, annot_kws={"size": 9})
    ax.set_title("Top Batsmen - Runs Per Season Heatmap", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Season", fontsize=12)
    ax.set_ylabel("Batsman", fontsize=12)
    fig.tight_layout()
    save(fig, "10_batsman_heatmap.png")


# 3.11  Summary Dashboard (4-panel)
def plot_dashboard(matches: pd.DataFrame, deliveries: pd.DataFrame):
    print("[*] Summary Dashboard...")
    fig = plt.figure(figsize=(18, 12), facecolor=BG_COLOR)
    fig.suptitle("IPL Analytics Dashboard", fontsize=22, fontweight="bold",
                 color=TEXT_COLOR, y=0.98)

    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)

    # Panel 1 - Team wins
    ax1 = fig.add_subplot(gs[0, 0])
    wins = (matches[matches["winner"] != "No Result"]
            .groupby("winner").size().sort_values(ascending=False).head(6))
    ax1.barh(wins.index[::-1], wins.values[::-1],
             color=PALETTE[:6], edgecolor="none")
    ax1.set_title("Top Teams by Wins", color=TEXT_COLOR, fontsize=13, fontweight="bold")
    ax1.tick_params(colors=TEXT_COLOR)
    ax1.set_facecolor("#16213E")
    ax1.grid(axis="x", alpha=0.3, color=GRID_COLOR)

    # Panel 2 - Scoring pattern
    ax2 = fig.add_subplot(gs[0, 1])
    over_runs = (deliveries.groupby("over")["total_runs"].mean()
                 .reset_index().rename(columns={"total_runs": "avg"}))
    over_runs = over_runs[over_runs["over"] <= 20]
    ax2.fill_between(over_runs["over"], over_runs["avg"], alpha=0.3, color=ACCENT)
    ax2.plot(over_runs["over"], over_runs["avg"], color=ACCENT, linewidth=2)
    ax2.set_title("Avg Runs Per Over", color=TEXT_COLOR, fontsize=13, fontweight="bold")
    ax2.tick_params(colors=TEXT_COLOR)
    ax2.set_facecolor("#16213E")
    ax2.grid(alpha=0.3, color=GRID_COLOR)

    # Panel 3 - Top batsmen
    ax3 = fig.add_subplot(gs[1, 0])
    top_bat = (deliveries.groupby("batsman")["batsman_runs"]
               .sum().sort_values(ascending=False).head(6))
    ax3.bar(range(len(top_bat)), top_bat.values,
            color=sns.color_palette("viridis", len(top_bat)), edgecolor="none")
    ax3.set_xticks(range(len(top_bat)))
    ax3.set_xticklabels(top_bat.index, rotation=25, ha="right",
                        color=TEXT_COLOR, fontsize=9)
    ax3.set_title("Top Run Scorers", color=TEXT_COLOR, fontsize=13, fontweight="bold")
    ax3.tick_params(colors=TEXT_COLOR)
    ax3.set_facecolor("#16213E")
    ax3.grid(axis="y", alpha=0.3, color=GRID_COLOR)

    # Panel 4 - Top bowlers
    ax4 = fig.add_subplot(gs[1, 1])
    top_bowl = (deliveries[deliveries["player_dismissed"].notna()]
                .groupby("bowler").size().sort_values(ascending=False).head(6))
    ax4.bar(range(len(top_bowl)), top_bowl.values,
            color=sns.color_palette("rocket_r", len(top_bowl)), edgecolor="none")
    ax4.set_xticks(range(len(top_bowl)))
    ax4.set_xticklabels(top_bowl.index, rotation=25, ha="right",
                        color=TEXT_COLOR, fontsize=9)
    ax4.set_title("Top Wicket Takers", color=TEXT_COLOR, fontsize=13, fontweight="bold")
    ax4.tick_params(colors=TEXT_COLOR)
    ax4.set_facecolor("#16213E")
    ax4.grid(axis="y", alpha=0.3, color=GRID_COLOR)

    save(fig, "00_dashboard.png")


# -------------------- Main --------------------
def main():
    print("=" * 55)
    print("  IPL Cricket Data Analysis  |  Starting...")
    print("=" * 55)

    matches, deliveries = load_data()
    matches, deliveries = clean_data(matches, deliveries)

    print(f"\n[INFO] Dataset loaded:")
    print(f"   - Matches    : {len(matches):,} rows x {matches.shape[1]} cols")
    print(f"   - Deliveries : {len(deliveries):,} rows x {deliveries.shape[1]} cols")
    print(f"\n[INFO] Generating plots -> {PLOTS_DIR}\n")

    plot_season_matches(matches)
    plot_team_wins(matches)
    plot_top_batsmen(deliveries)
    plot_top_bowlers(deliveries)
    plot_toss_analysis(matches)
    plot_runs_per_over(deliveries)
    plot_venue_analysis(deliveries, matches)
    plot_pom_awards(matches)
    plot_win_margins(matches)
    plot_batsmen_heatmap(deliveries, matches)
    plot_dashboard(matches, deliveries)

    print("\n" + "=" * 55)
    print("  [DONE] All 11 plots saved to outputs/plots/")
    print("=" * 55)


if __name__ == "__main__":
    main()
