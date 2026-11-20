# 🏏 IPL Cricket Data Analytics Project

> A complete **Data Analyst portfolio project** for freshers, analyzing IPL (Indian Premier League) T20 cricket data using Python, pandas, matplotlib, and seaborn.

---

## 📂 Project Structure

```
DA/
├── data/
│   ├── ipl_matches.csv          # Match-level data  (~500 rows)
│   └── ipl_deliveries.csv       # Ball-by-ball data (~55,000 rows)
├── notebooks/
│   └── ipl_analysis.ipynb       # Jupyter notebook (optional)
├── outputs/
│   └── plots/                   # All generated charts saved here
├── src/
│   ├── generate_data.py         # Synthetic IPL dataset generator
│   └── ipl_analysis.py          # Main analysis script (11 plots)
├── requirements.txt
└── README.md
```

---

## 📊 Analyses Included

| # | Analysis | File |
|---|----------|------|
| 00 | Summary Dashboard (4-panel) | `00_dashboard.png` |
| 01 | Season-wise Match Count | `01_season_matches.png` |
| 02 | Team Win Comparison | `02_team_wins.png` |
| 03 | Top 12 Run-Scorers | `03_top_batsmen.png` |
| 04 | Top 12 Wicket-Takers | `04_top_bowlers.png` |
| 05 | Toss Decision & Impact | `05_toss_analysis.png` |
| 06 | Scoring Pattern per Over | `06_runs_per_over.png` |
| 07 | Best Batting Venues | `07_venue_analysis.png` |
| 08 | Player of the Match Awards | `08_pom_awards.png` |
| 09 | Win Margin Distributions | `09_win_margins.png` |
| 10 | Batsman × Season Heatmap | `10_batsman_heatmap.png` |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate sample IPL dataset

```bash
python src/generate_data.py
```

### 3. Run the full analysis

```bash
python src/ipl_analysis.py
```

All 11 charts will be saved in `outputs/plots/`.

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| pandas | 2.2.2 | Data loading, cleaning, manipulation |
| numpy | 1.26.4 | Numerical operations |
| matplotlib | 3.9.0 | Core plotting engine |
| seaborn | 0.13.2 | Statistical visualizations |
| jupyter | 1.0.0 | Interactive notebook support |

---

## 🔑 Key Insights Explored

- 📈 **Scoring trends**: Which overs produce the most runs?
- 🏆 **Team dominance**: Which teams have won the most titles?
- 🏏 **Batting stars**: Who are the all-time top run-scorers?
- 🎳 **Bowling heroes**: Who takes the most wickets?
- 🪙 **Toss effect**: Does winning the toss improve your chances?
- 🏟️ **Venue impact**: Which grounds favor batsmen?

---

## 👤 Author

**Fresher Data Analyst Portfolio Project**  
Built with Python · pandas · seaborn · matplotlib

---

## 📄 License

MIT License — Free to use for portfolio & learning purposes.
