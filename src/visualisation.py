import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import scatter_matrix

from src.analysis import add_futures, clean_data, city_analytic
from src.data_loader import load_data

PINK = "pink"
GRID = "white"
plt.rcParams.update({
    "figure.facecolor": "black",
    "axes.facecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black",
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "text.color": "white",
    "legend.facecolor": "black",
    "legend.edgecolor": "white",
})


def save_plot(name):
    plt.savefig(name, dpi=300, transparent=True)


def line_plot(df):
    daily = df.groupby("date")["revenue_discnt"].sum().reset_index()
    plt.figure(figsize=(12, 6))
    plt.plot(daily["date"], daily["revenue_discnt"], color=PINK, linestyle="--", marker="o", label="Revenue")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.title("Revenue dynamics")
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", color=GRID)
    plt.ylim(0, daily["revenue_discnt"].max() + 500)
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_plot("line_plot.png")
    plt.close()


def bar_plot(df):
    cat = df.groupby("category")["revenue_discnt"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    plt.bar(cat.index, cat.values, color=PINK, width=0.7, alpha=0.7, label="Revenue")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.title("Revenue by category")
    plt.legend(loc="upper right")
    plt.grid(True, axis="y", linestyle="--", color=GRID)
    plt.ylim(0, cat.max() + 5000)
    plt.tight_layout()
    save_plot("bar_plot.png")
    plt.close()


def hist_plot(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df["revenue_discnt"], bins=15, color=PINK, alpha=0.7, label="Revenue")
    plt.xlabel("Revenue with discount")
    plt.ylabel("Count")
    plt.title("Distribution of revenue")
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", color=GRID)
    plt.xlim(0, 1000)
    plt.ylim(0, 2500)
    plt.tight_layout()
    save_plot("hist_plot.png")
    plt.close()


def reg_plot(df):
    x = df["price"]
    y = df["revenue_discnt"]
    k, b = np.polyfit(x, y, 1)
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color=PINK, s=22, alpha=0.25, label="Orders")
    plt.plot(x, k * x + b, color="#c85a8d", linestyle="--", label="Trend")
    plt.xlabel("Price")
    plt.ylabel("Revenue with discount")
    plt.title("Regression price and revenue")
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", color=GRID)
    plt.xlim(0, 1000)
    plt.ylim(0, 2000)
    plt.tight_layout()
    save_plot("reg_plot.png")
    plt.close()


def corr_plot(df):
    cols = ["price", "quantity", "discount", "delivery_days", "is_returned", "rating", "revenue", "revenue_discnt"]
    corr = df[cols].corr()
    plt.figure(figsize=(10, 8))
    plt.imshow(corr, cmap="PuRd", interpolation="nearest", alpha=0.85)
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Correlation matrix")
    plt.tight_layout()
    save_plot("corr_plot.png")
    plt.close()
    print(corr)


def pair_plot(df):
    cols = ["price", "quantity", "discount", "delivery_days", "rating", "revenue_discnt"]
    fig = scatter_matrix(df[cols], figsize=(12, 12), diagonal="hist", alpha=0.6, color=PINK)
    for ax in np.array(fig).reshape(-1):
        ax.grid(True, linestyle="--", color=GRID)
    plt.suptitle("Pair plot", y=1.02)
    plt.tight_layout()
    save_plot("pair_plot.png")
    plt.close()


def city_bar(df):
    cities = city_analytic(df)
    plt.figure(figsize=(12, 6))
    plt.bar(cities["region"], cities["is_returned"], color=PINK, width=0.7, alpha=0.7, label="Returns")
    plt.xlabel("Region")
    plt.ylabel("Returns, %")
    plt.title("Returns by region")
    plt.legend(loc="upper right")
    plt.grid(True, axis="y", linestyle="--", color=GRID)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    save_plot("city_bar_plot.png")
    plt.close()



def run(path="data/db.csv"):
    df = load_data(path, show_info=False)
    df = clean_data(df)
    df["date"] = np.array(df["date"], dtype="datetime64[ns]")
    df = add_futures(df)
    line_plot(df)
    bar_plot(df)
    hist_plot(df)
    reg_plot(df)
    corr_plot(df)
    pair_plot(df)
    city_bar(df)
