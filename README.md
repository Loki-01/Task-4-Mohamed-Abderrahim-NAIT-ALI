# Data Analytics Project 4 — Data Visualization

**DecodeLabs Batch 2026 | Optional Mastery Phase**

---

## Overview

This project is the final optional milestone of the DecodeLabs Data Analytics internship. The objective shifts from exploratory analysis to **explanatory communication** — transforming raw e-commerce data into boardroom-ready visual insights that drive executive decisions.

The work is structured around three professional disciplines:

- **The Architect** — select the right chart for the right question
- **The Editor** — maximize signal, eliminate noise
- **The Storyteller** — make every insight impossible to ignore

---

## Dataset

| Attribute | Detail |
|---|---|
| Source | DecodeLabs E-Commerce Dataset (Project 3 continuation) |
| Records | 1,200 orders |
| Period | FY 2023 (January – December) |
| Features | Order ID, Date, Category, Region, Quantity, Unit Price, Revenue, Payment Method, Customer Segment, Order Status |

---

## Visualizations

### Chart 1 — Revenue by Category
**Type:** Horizontal Bar Chart

**Insight:** Electronics Dominates Revenue, Contributing ~34% of Total Annual Sales

Horizontal bars chosen for clean label readability across 5 categories. Single accent color highlights the top performer; all others muted. Direct value labels eliminate the need for axis decoding. Zero baseline enforced.

---

### Chart 2 — Monthly Revenue Trend
**Type:** Line Chart

**Insight:** Revenue Surged in Q4, with December Peaking 60%+ Above January Baseline

Continuous line connects 12 monthly data points. Area fill provides volume context. Peak annotated directly on the chart with an arrow — no legend required. SCR narrative structure: stable baseline (Situation) → Q4 spike (Complication) → seasonal strategy implication (Resolution).

---

### Chart 3 — Revenue by Region × Quarter
**Type:** Stacked Bar Chart

**Insight:** West Region Leads Every Quarter; Q4 Drives 35%+ of Full-Year Revenue

Stacked bar chosen to show both composition (regional share) and total volume simultaneously. Value labels embedded inside each segment in white for high-contrast readability. Quarterly grouping reveals seasonality pattern across all regions.

---

### Chart 4 — Quantity vs Revenue Relationship
**Type:** Scatter Plot

**Insight:** Higher Quantity Orders Correlate Strongly with Revenue Across All Categories

Scatter plot reveals the linear relationship between order quantity and revenue. Redundant encoding applied: each category is encoded by both color and marker shape to ensure accessibility for color-blind viewers. Pearson correlation coefficient (r) annotated directly on the chart. Trend line confirms the positive relationship.

---

### Chart 5 — Payment Method Distribution
**Type:** Horizontal Bar Chart (replaces pie chart per Project 4 strict rule)

**Insight:** Credit Cards Process 42% of Orders — Optimising Card Checkout Is the #1 UX Priority

Pie chart deliberately avoided. Horizontal bars with percentage labels allow precise comparison that the human eye cannot perform accurately on pie slices. Accent on the dominant method; actionable business recommendation embedded in the title.

---

### Chart 6 — KPI Executive Dashboard
**Type:** Multi-panel Dashboard

**Insight:** Electronics and Q4 Seasonality Drive 70%+ of Annual E-Commerce Revenue

Boardroom-ready layout following the 5-second rule: three KPI cards top-left where the eye begins, supporting charts below. Return Rate in red for immediate visual flagging. Analyst attribution in footnote for credibility. One dashboard, one central narrative.

---

## Design Principles Applied

| Principle | Implementation |
|---|---|
| Zero-baseline rule | All bar charts start at 0 |
| Data-ink ratio | No 3D effects, no heavy gridlines, no decorative backgrounds |
| Chartjunk elimination | Removed borders, unnecessary tick marks, and redundant axes |
| Direct labeling | Value labels on all bars; no standalone legends where avoidable |
| Color as spotlight | Single accent (#1B6CA8) on the key insight; all context in muted grey |
| Redundant encoding | Scatter plot uses both color and shape per category |
| Accessibility | Never rely on color alone to convey meaning |
| Action titles | Every chart title states the conclusion, not just the topic |
| SCR framework | Monthly trend structured as Situation → Complication → Resolution |
| 5-second rule | KPI dashboard: core insight readable within 5 seconds |

---

## Tech Stack

- Python 3.x
- pandas
- NumPy
- Matplotlib

---

## Project Structure

```
project4-data-visualization/
├── project4_visualizations.py       # Full visualization script
├── chart1_revenue_by_category.png
├── chart2_monthly_trend.png
├── chart3_region_quarter.png
├── chart4_quantity_vs_revenue.png
├── chart5_payment_methods.png
├── chart6_kpi_dashboard.png
└── README.md
```

---

## How to Run

```bash
pip install pandas numpy matplotlib
python project4_visualizations.py
```

All 6 charts are saved as high-resolution PNG files (150 DPI) in the working directory.

To use your own dataset, replace the synthetic data block with:

```python
df = pd.read_csv("your_ecommerce_data.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
```

---

## Key Business Insights

1. **Electronics** is the single largest revenue driver at ~34% — any supply chain disruption here has disproportionate business impact.
2. **Q4 seasonality** is the strongest revenue lever — a 60%+ revenue spike in October–December demands dedicated inventory and marketing planning.
3. **West Region** consistently leads all quarters — resource allocation should reflect this concentration.
4. **Quantity scales revenue linearly** (r ≈ 0.84) — bulk order incentives are a viable growth strategy.
5. **Credit Card is the dominant payment channel** at 42% — checkout optimization should prioritize card UX above all other payment flows.
6. **Return rate at ~11.7%** is a risk flag — warrants deeper investigation by category to identify quality or expectation-mismatch issues.

---

## Author

**NAIT ALI Mohamed Abderrahim**
Energy & Mechanical Engineer | Data Scientist
[GitHub](https://github.com/Loki-01) | [LinkedIn](https://linkedin.com/in/nait-ali-mohamed-abderrahim-663a252a5)

DecodeLabs Batch 2026 | Data Analytics Internship
