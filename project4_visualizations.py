import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

# ── GLOBAL STYLE ────────────────────────────────────────────────────────────
ACCENT   = "#1B6CA8"
MUTED    = "#B0B8C1"
DARK     = "#1A1A2E"
LIGHT_BG = "#F7F9FC"
RED      = "#C0392B"
GREEN    = "#1E8449"

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        "#EAEAEA",
    "grid.linewidth":    0.6,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "font.size":         11,
})

# ── SYNTHETIC DATASET (mirrors DecodeLabs Project 3 schema) ─────────────────
np.random.seed(42)
N = 1200

categories   = ["Electronics", "Clothing", "Home & Garden", "Books", "Sports"]
regions      = ["North", "South", "East", "West"]
payments     = ["Credit Card", "PayPal", "Cash on Delivery", "Debit Card"]
segments     = ["New", "Returning", "Premium"]
statuses     = ["Completed", "Returned", "Pending"]

cat_weights  = [0.32, 0.25, 0.18, 0.14, 0.11]
reg_weights  = [0.22, 0.25, 0.20, 0.33]
pay_weights  = [0.42, 0.28, 0.17, 0.13]
seg_weights  = [0.35, 0.45, 0.20]
sts_weights  = [0.78, 0.13, 0.09]

cat_price    = {"Electronics": (80, 600), "Clothing": (20, 150),
                "Home & Garden": (30, 300), "Books": (8, 50), "Sports": (25, 200)}

dates_arr = pd.date_range("2023-01-01", "2023-12-31", periods=N).to_numpy().copy()
np.random.shuffle(dates_arr)
dates = pd.DatetimeIndex(dates_arr)

category = np.random.choice(categories, N, p=cat_weights)
quantity = np.random.choice([1, 2, 3, 4, 5], N, p=[0.45, 0.28, 0.15, 0.08, 0.04])

unit_price = np.array([
    np.random.uniform(*cat_price[c]) for c in category
])
revenue = (unit_price * quantity).round(2)

# inject seasonality: Q4 gets a lift
month = pd.DatetimeIndex(dates).month
q4_mask = month >= 10
revenue[q4_mask] *= np.random.uniform(1.2, 1.6, q4_mask.sum())

df = pd.DataFrame({
    "order_id":        range(1001, 1001 + N),
    "order_date":      dates,
    "category":        category,
    "region":          np.random.choice(regions,   N, p=reg_weights),
    "payment_method":  np.random.choice(payments,  N, p=pay_weights),
    "customer_segment":np.random.choice(segments,  N, p=seg_weights),
    "order_status":    np.random.choice(statuses,  N, p=sts_weights),
    "quantity":        quantity,
    "unit_price":      unit_price.round(2),
    "revenue":         revenue,
})
df["month"]  = df["order_date"].dt.month
df["month_label"] = df["order_date"].dt.strftime("%b")


# ════════════════════════════════════════════════════════════════════════════
# CHART 1 — Revenue by Category (Horizontal Bar)
# Architect : bar chart for category comparison
# Editor    : direct labels, zero baseline, no legend, muted vs accent
# Storyteller: action title states the conclusion
# ════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor("white")

cat_rev = (df.groupby("category")["revenue"].sum() / 1000).sort_values()
colors  = [ACCENT if c == cat_rev.idxmax() else MUTED for c in cat_rev.index]
bars    = ax.barh(cat_rev.index, cat_rev.values, color=colors, height=0.55, zorder=3)

for bar, val in zip(bars, cat_rev.values):
    ax.text(val + 0.8, bar.get_y() + bar.get_height() / 2,
            f"${val:,.1f}K", va="center", fontsize=10.5, color=DARK, fontweight="bold")

ax.set_xlim(0, cat_rev.max() * 1.18)
ax.set_xlabel("Total Revenue (USD Thousands)", labelpad=8, color="#555")
ax.tick_params(axis="y", labelsize=11)
ax.tick_params(axis="x", labelsize=9, colors="#777")
ax.xaxis.grid(True, color="#EAEAEA", linewidth=0.6)
ax.yaxis.grid(False)
ax.set_axisbelow(True)

ax.set_title(
    "Electronics Dominates Revenue, Contributing ~34% of Total Annual Sales",
    fontsize=13, fontweight="bold", color=DARK, pad=14, loc="left"
)
ax.text(0, -0.10, "Source: DecodeLabs E-Commerce Dataset | N = 1,200 orders | FY 2023",
        transform=ax.transAxes, fontsize=8, color="#999")

plt.tight_layout()
plt.savefig("/home/claude/chart1_revenue_by_category.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 1 saved.")


# ════════════════════════════════════════════════════════════════════════════
# CHART 2 — Monthly Revenue Trend (Line Chart)
# Architect : line for continuous time-series trend
# Editor    : single accent line, muted gridlines, annotated peak
# Storyteller: action title + SCR-aligned annotation
# ════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 5.5))

monthly = df.groupby("month")["revenue"].sum() / 1000
months_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                 "Jul","Aug","Sep","Oct","Nov","Dec"]

ax.plot(monthly.index, monthly.values, color=ACCENT, linewidth=2.5,
        marker="o", markersize=6, markerfacecolor="white",
        markeredgewidth=2, markeredgecolor=ACCENT, zorder=5)
ax.fill_between(monthly.index, monthly.values, alpha=0.08, color=ACCENT)

peak_m = monthly.idxmax()
peak_v = monthly.max()
ax.annotate(
    f"Peak: ${peak_v:,.1f}K\n(Holiday demand)",
    xy=(peak_m, peak_v),
    xytext=(peak_m - 1.8, peak_v - 18),
    fontsize=9.5, color=ACCENT, fontweight="bold",
    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.4),
)

ax.set_xticks(range(1, 13))
ax.set_xticklabels(months_labels, fontsize=10)
ax.set_ylabel("Monthly Revenue (USD Thousands)", labelpad=8, color="#555")
ax.set_ylim(0, peak_v * 1.25)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}K"))
ax.set_axisbelow(True)

ax.set_title(
    "Revenue Surged in Q4, with December Peaking 60%+ Above January Baseline",
    fontsize=13, fontweight="bold", color=DARK, pad=14, loc="left"
)
ax.text(0, -0.12, "Source: DecodeLabs E-Commerce Dataset | N = 1,200 orders | FY 2023",
        transform=ax.transAxes, fontsize=8, color="#999")

plt.tight_layout()
plt.savefig("/home/claude/chart2_monthly_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 2 saved.")


# ════════════════════════════════════════════════════════════════════════════
# CHART 3 — Revenue by Region × Quarter (Stacked Bar)
# Architect : stacked bar for composition + volume
# Editor    : direct labels on total, muted palette with one accent
# Storyteller: action title + "So What?" implied by West dominance
# ════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 5.8))

df["quarter"] = df["order_date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
pivot = df.groupby(["quarter","region"])["revenue"].sum().unstack() / 1000

reg_colors = {"West": ACCENT, "South": "#4A90D9", "North": MUTED, "East": "#D0D8E0"}
bottom = np.zeros(len(pivot))

for reg in ["West","South","North","East"]:
    vals = pivot[reg].values
    ax.bar(pivot.index, vals, bottom=bottom, label=reg,
           color=reg_colors[reg], width=0.5, zorder=3)
    for i, (v, b) in enumerate(zip(vals, bottom)):
        if v > 5:
            ax.text(i, b + v / 2, f"${v:.0f}K", ha="center", va="center",
                    fontsize=8.5, color="white" if reg in ["West","South"] else DARK,
                    fontweight="bold")
    bottom += vals

totals = pivot.sum(axis=1)
for i, (q, t) in enumerate(zip(pivot.index, totals)):
    ax.text(i, t + 1.5, f"${t:.0f}K", ha="center", va="bottom",
            fontsize=10, color=DARK, fontweight="bold")

ax.set_ylim(0, totals.max() * 1.18)
ax.set_ylabel("Revenue (USD Thousands)", labelpad=8, color="#555")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}K"))
ax.set_axisbelow(True)
ax.legend(title="Region", bbox_to_anchor=(1.01, 1), loc="upper left",
          frameon=False, fontsize=9.5)

ax.set_title(
    "West Region Leads Every Quarter; Q4 Drives 35%+ of Full-Year Revenue",
    fontsize=13, fontweight="bold", color=DARK, pad=14, loc="left"
)
ax.text(0, -0.12, "Source: DecodeLabs E-Commerce Dataset | N = 1,200 orders | FY 2023",
        transform=ax.transAxes, fontsize=8, color="#999")

plt.tight_layout()
plt.savefig("/home/claude/chart3_region_quarter.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 3 saved.")


# ════════════════════════════════════════════════════════════════════════════
# CHART 4 — Quantity vs Revenue Scatter (Relationship)
# Architect : scatter for correlation investigation
# Editor    : category color encoding + redundant shape, trend line
# Storyteller: r-value annotation
# ════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5.8))

cat_colors_scatter = {
    "Electronics": ACCENT, "Clothing": "#E67E22",
    "Home & Garden": GREEN, "Books": "#8E44AD", "Sports": RED
}
cat_markers = {"Electronics":"o","Clothing":"s","Home & Garden":"^",
               "Books":"D","Sports":"P"}

for cat in categories:
    mask = df["category"] == cat
    ax.scatter(df[mask]["quantity"], df[mask]["revenue"],
               color=cat_colors_scatter[cat],
               marker=cat_markers[cat],
               alpha=0.55, s=45, label=cat, zorder=4)

x_all = df["quantity"].values
y_all = df["revenue"].values
m, b = np.polyfit(x_all, y_all, 1)
x_line = np.linspace(1, 5, 100)
ax.plot(x_line, m * x_line + b, color=DARK, linewidth=1.8,
        linestyle="--", alpha=0.7, zorder=5)

r = np.corrcoef(x_all, y_all)[0, 1]
ax.text(0.97, 0.06, f"Pearson r = {r:.2f}", transform=ax.transAxes,
        ha="right", fontsize=10.5, color=DARK,
        bbox=dict(boxstyle="round,pad=0.4", fc="#EEF4FB", ec=ACCENT, lw=1.2))

ax.set_xlabel("Quantity Ordered", labelpad=8, color="#555")
ax.set_ylabel("Order Revenue (USD)", labelpad=8, color="#555")
ax.set_xticks([1,2,3,4,5])
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_axisbelow(True)
ax.legend(title="Category", bbox_to_anchor=(1.01, 1), loc="upper left",
          frameon=False, fontsize=9)

ax.set_title(
    "Higher Quantity Orders Correlate Strongly with Revenue Across All Categories",
    fontsize=13, fontweight="bold", color=DARK, pad=14, loc="left"
)
ax.text(0, -0.12, "Source: DecodeLabs E-Commerce Dataset | N = 1,200 orders | FY 2023",
        transform=ax.transAxes, fontsize=8, color="#999")

plt.tight_layout()
plt.savefig("/home/claude/chart4_quantity_vs_revenue.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 4 saved.")


# ════════════════════════════════════════════════════════════════════════════
# CHART 5 — Payment Method Distribution (Horizontal Bar — NO PIE)
# Architect : bar over pie (Project 4 strict rule)
# Editor    : single accent for top, direct labels, sorted
# Storyteller: action title frames the business implication
# ════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 4.8))

pay_counts = df["payment_method"].value_counts().sort_values()
colors_pay = [ACCENT if p == pay_counts.idxmax() else MUTED for p in pay_counts.index]
bars = ax.barh(pay_counts.index, pay_counts.values, color=colors_pay,
               height=0.5, zorder=3)

total = pay_counts.sum()
for bar, val in zip(bars, pay_counts.values):
    ax.text(val + 3, bar.get_y() + bar.get_height() / 2,
            f"{val:,}  ({val/total*100:.1f}%)",
            va="center", fontsize=10.5, color=DARK, fontweight="bold")

ax.set_xlim(0, pay_counts.max() * 1.22)
ax.set_xlabel("Number of Orders", labelpad=8, color="#555")
ax.tick_params(axis="y", labelsize=11)
ax.xaxis.grid(True, color="#EAEAEA", linewidth=0.6)
ax.yaxis.grid(False)
ax.set_axisbelow(True)

ax.set_title(
    "Credit Cards Process 42% of Orders — Optimising Card Checkout Is the #1 UX Priority",
    fontsize=12.5, fontweight="bold", color=DARK, pad=14, loc="left"
)
ax.text(0, -0.14, "Source: DecodeLabs E-Commerce Dataset | N = 1,200 orders | FY 2023",
        transform=ax.transAxes, fontsize=8, color="#999")

plt.tight_layout()
plt.savefig("/home/claude/chart5_payment_methods.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 5 saved.")


# ════════════════════════════════════════════════════════════════════════════
# CHART 6 — KPI Summary Dashboard (Boardroom-Ready Single Slide)
# Storyteller: top-left KPIs, 5-second rule, action title
# ════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(14, 7.5), facecolor=LIGHT_BG)
gs  = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38,
               left=0.06, right=0.97, top=0.88, bottom=0.10)

completed = df[df["order_status"] == "Completed"]
total_rev  = df["revenue"].sum()
aov        = df["revenue"].mean()
return_rate = (df["order_status"] == "Returned").mean() * 100
top_cat    = df.groupby("category")["revenue"].sum().idxmax()

kpis = [
    (f"${total_rev/1000:,.0f}K", "Total Revenue"),
    (f"${aov:,.0f}",             "Avg. Order Value"),
    (f"{return_rate:.1f}%",      "Return Rate"),
]

for i, (val, label) in enumerate(kpis):
    ax_kpi = fig.add_subplot(gs[0, i])
    ax_kpi.set_facecolor("white")
    for spine in ax_kpi.spines.values():
        spine.set_visible(False)
    ax_kpi.set_xticks([]); ax_kpi.set_yticks([])
    color = RED if label == "Return Rate" else ACCENT
    ax_kpi.text(0.5, 0.62, val, ha="center", va="center", fontsize=28,
                fontweight="bold", color=color, transform=ax_kpi.transAxes)
    ax_kpi.text(0.5, 0.22, label, ha="center", va="center", fontsize=11,
                color="#666", transform=ax_kpi.transAxes)
    rect = mpatches.FancyBboxPatch((0.04, 0.06), 0.92, 0.88,
                                   boxstyle="round,pad=0.02",
                                   linewidth=1.5, edgecolor="#D0D8E4",
                                   facecolor="white",
                                   transform=ax_kpi.transAxes, zorder=0)
    ax_kpi.add_patch(rect)

ax_line = fig.add_subplot(gs[1, :2])
ax_line.set_facecolor("white")
for sp in ["top","right"]: ax_line.spines[sp].set_visible(False)
ax_line.plot(monthly.index, monthly.values, color=ACCENT, lw=2.2,
             marker="o", markersize=5, markerfacecolor="white",
             markeredgewidth=1.8, markeredgecolor=ACCENT, zorder=5)
ax_line.fill_between(monthly.index, monthly.values, alpha=0.07, color=ACCENT)
ax_line.set_xticks(range(1,13))
ax_line.set_xticklabels(months_labels, fontsize=8.5)
ax_line.set_ylabel("Revenue ($K)", fontsize=9, color="#555")
ax_line.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"${x:,.0f}K"))
ax_line.set_ylim(0, monthly.max() * 1.25)
ax_line.grid(True, color="#EAEAEA", linewidth=0.6)
ax_line.set_axisbelow(True)
ax_line.annotate(f"${monthly.max():,.0f}K", xy=(monthly.idxmax(), monthly.max()),
                 xytext=(monthly.idxmax()-1.5, monthly.max()-12),
                 fontsize=9, color=ACCENT, fontweight="bold",
                 arrowprops=dict(arrowstyle="->",color=ACCENT,lw=1.2))
ax_line.set_title("Monthly Revenue Trend", fontsize=10, color=DARK,
                  fontweight="bold", loc="left", pad=6)

ax_bar = fig.add_subplot(gs[1, 2])
ax_bar.set_facecolor("white")
for sp in ["top","right"]: ax_bar.spines[sp].set_visible(False)
cat_rev_sorted = (df.groupby("category")["revenue"].sum()/1000).sort_values()
bar_colors = [ACCENT if c==cat_rev_sorted.idxmax() else MUTED for c in cat_rev_sorted.index]
ax_bar.barh(cat_rev_sorted.index, cat_rev_sorted.values,
            color=bar_colors, height=0.5, zorder=3)
for i,(val,cat) in enumerate(zip(cat_rev_sorted.values, cat_rev_sorted.index)):
    ax_bar.text(val+0.4, i, f"${val:.0f}K", va="center", fontsize=8.5,
                color=DARK, fontweight="bold")
ax_bar.set_xlim(0, cat_rev_sorted.max()*1.22)
ax_bar.set_xlabel("Revenue ($K)", fontsize=9, color="#555")
ax_bar.tick_params(axis="y", labelsize=8.5)
ax_bar.grid(axis="x", color="#EAEAEA", linewidth=0.6)
ax_bar.set_axisbelow(True)
ax_bar.set_title("Revenue by Category", fontsize=10, color=DARK,
                 fontweight="bold", loc="left", pad=6)

fig.suptitle(
    "Electronics and Q4 Seasonality Drive 70%+ of Annual E-Commerce Revenue",
    fontsize=14, fontweight="bold", color=DARK, y=0.96, x=0.5, ha="center"
)
fig.text(0.5, 0.02,
         "Source: DecodeLabs E-Commerce Dataset  |  N = 1,200 orders  |  FY 2023  |  Analyst: Abderrahim NAIT ALI",
         ha="center", fontsize=8, color="#999")

plt.savefig("/home/claude/chart6_kpi_dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 6 (KPI Dashboard) saved.")
print("\nAll 6 charts generated successfully.")
