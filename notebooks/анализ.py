from pathlib import Path
import sys

import numpy as np
from scipy import stats


ROOT = Path.cwd().resolve()

if not (ROOT / "src").exists():
    for parent in ROOT.parents:
        if (parent / "src").exists() and (parent / "data").exists():
            ROOT = parent
            break

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from src.analysis import add_futures, clean_data, sorting
from src.data_loader import load_data


path = ROOT / "data" / "db.csv"

df = load_data(path, show_info=False)
df = clean_data(df)
df = add_futures(df)
df = sorting(df)

print(df.head())

arr = np.array(df["price"])

print("count: ", arr.size)
print("mean: ", np.mean(arr))
print("median: ", np.median(arr))
print("var: ", np.var(arr))
print("q50: ", np.quantile(arr, 0.5))
print("quartiles: ", np.quantile(arr, [0.25, 0.5, 0.75]))

print(df[df["platform"] == "App"])
print(df[df["platform"] == "Web"])

revenue_arr = np.array(df["revenue_discnt"])

print(revenue_arr[np.argmax(revenue_arr)])
print(revenue_arr[revenue_arr > 200])

generator_arr = np.fromiter((value for value in df["revenue_discnt"]), dtype=float)

print("generator mean revenue: ", np.mean(generator_arr))
print("generator median revenue: ", np.median(generator_arr))

t_stat, p_value = stats.ttest_1samp(revenue_arr, 150)

print(t_stat, p_value)

app = np.array(df[df["platform"] == "App"]["revenue_discnt"].dropna())
web = np.array(df[df["platform"] == "Web"]["revenue_discnt"].dropna())

stat, p_value = stats.mannwhitneyu(app, web)

print(stat, p_value)
