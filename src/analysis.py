import time
from functools import wraps
from pathlib import Path

import pandas as pd

from src.data_loader import load_data, read_data_chunks


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"call: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def time_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"time: {func.__name__} {time.perf_counter() - start:.4f}s")
        return result
    return wrapper


def revenue_values(df):
    for value in df["revenue_discnt"]:
        yield value


def count_rows(path, chunk_size=50):
    total = 0
    for chunk in read_data_chunks(path, chunk_size=chunk_size):
        total += len(chunk)
    return total


def clean_data(df):
    df.drop_duplicates(inplace=True)
    df["is_returned"] = df["is_returned"].fillna(0)
    return df


def add_futures(df):
    df["revenue"] = df["price"] * df["quantity"]
    df["revenue_discnt"] = df["revenue"] * (1 - df["discount"] / 100)
    return df


def sorting(df):
    df = df.sort_values(["region", "revenue_discnt"], ascending=[False, False])
    return df


def user_analytics(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    last_date = df["date"].max()
    users = df.groupby("user_id").agg({
        "revenue_discnt": "sum",
        "order_id": "count",
        "price": "median",
        "is_returned": "mean",
        "rating": "mean",
        "date": "max"
    }).reset_index()
    users["avg_check"] = users["revenue_discnt"] / users["order_id"]
    users["is_returned"] = users["is_returned"] * 100
    users["days_from_last_order"] = (last_date - users["date"]).dt.days
    print(users.sort_values("revenue_discnt", ascending=False))
    print(users.sort_values("order_id", ascending=False))
    print(users.sort_values("days_from_last_order"))
    return users


def returns_analytics(df):
    returns_cat = df.groupby("category").agg({
        "is_returned": "mean",
        "revenue_discnt": "sum",
        "order_id": "count"
    }).reset_index()
    returns_city = df.groupby("city").agg({
        "is_returned": "mean",
        "delivery_days": "mean",
        "order_id": "count"
    }).reset_index()
    returns_cat["is_returned"] = returns_cat["is_returned"] * 100
    returns_city["is_returned"] = returns_city["is_returned"] * 100
    return returns_cat, returns_city


def channel_analytics(df):
    channels = df.groupby(["platform", "traffic_source"]).agg({
        "revenue_discnt": "sum",
        "order_id": "count",
        "is_returned": "mean"
    }).reset_index()
    channels["avg_check"] = channels["revenue_discnt"] / channels["order_id"]
    channels["is_returned"] = channels["is_returned"] * 100
    return channels


def city_analytic(df):
    cities = df.groupby("region").agg({
        "is_returned": "mean",
        "order_id": "count"
    }).reset_index()
    cities["is_returned"] = cities["is_returned"] * 100
    return cities.sort_values("is_returned", ascending=False)


def make_report(df):
    report = df.copy()
    report["date"] = pd.to_datetime(report["date"])
    report["weekday"] = report["date"].dt.day_name()
    report["is_weekend"] = report["date"].dt.weekday >= 5
    weekend = report.groupby("is_weekend")["revenue_discnt"].mean()
    weekday = report.groupby("weekday")["order_id"].count().sort_values(ascending=False).index[0]
    corr = report[["price", "discount", "delivery_days", "rating", "revenue_discnt"]].corr(numeric_only=True)["revenue_discnt"]
    source = report.groupby("traffic_source")["revenue_discnt"].mean().sort_values(ascending=False)
    return_rate = report.groupby("platform")["is_returned"].mean().sort_values()
    category = report.groupby("category")["revenue_discnt"].sum().sort_values(ascending=False)
    return [
        f"1. В выходные средняя выручка выше: {weekend[True]:.2f} против {weekend[False]:.2f} в будни.",
        f"2. Самый активный день по числу заказов: {weekday}.",
        f"3. Самая сильная связь с revenue_discnt у price: {corr['price']:.2f}.",
        f"4. Самый сильный источник по средней выручке: {source.index[0]} ({source.iloc[0]:.2f}).",
        f"5. Самая низкая доля возвратов у платформы {return_rate.index[0]} ({return_rate.iloc[0] * 100:.2f}%).",
        f"6. Категория с максимальной суммарной выручкой: {category.index[0]} ({category.iloc[0]:.2f}).",
    ]


def save_reports(path, users, returns_cat, returns_city, channels, insights):
    reports = Path(path).parent.parent / "reports"
    reports.mkdir(exist_ok=True)
    users.to_csv(reports / "users.csv", index=False)
    returns_cat.to_csv(reports / "returns_category.csv", index=False)
    returns_city.to_csv(reports / "returns_city.csv", index=False)
    channels.to_csv(reports / "channels.csv", index=False)
    (reports / "report.txt").write_text("\n".join(insights))
    return reports


@log_call
@time_call
def run(path="data/db.csv"):
    row_count = count_rows(path)
    df = load_data(path)
    if row_count != len(df):
        raise ValueError("Row count mismatch")
    df = clean_data(df)
    df = add_futures(df)
    df = sorting(df)
    users = user_analytics(df)
    returns_cat, returns_city = returns_analytics(df)
    channels = channel_analytics(df)
    save_reports(path, users, returns_cat, returns_city, channels, make_report(df))
    return df
