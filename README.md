## Setup

From the repository directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py analyze
```

Use `python main.py viz` for charts or `python main.py all` for both. The default dataset is `data/db.csv`; use `--path data/another.csv` to choose a different CSV with the same columns.

Analysis writes CSV summaries and `report.txt` to `reports/` next to the dataset's parent directory. Charts are saved as PNG files in the current directory. Run the tests with `python -m pytest`.

## 📈 Visuals

<table>
  <tr>
    <td><img src="reg_plot.png" width="420"></td>
    <td><img src="city_bar_plot.png" width="420"></td>
  </tr>
</table>

## 📊 Metrics

- `count`
- `mean`
- `median`
- `variance`
- `q50`
- `quartiles`
- `revenue`
- `revenue_discnt`
- `orders_count`
- `avg_check`
- `return_rate`
- `avg_rating`
- `last_order_date`
- `days_from_last_order`
- `revenue_by_category`
- `return_rate_by_category`
- `return_rate_by_city`
- `avg_delivery_days_by_city`
- `max_revenue_value`
- `revenue_values_over_200`
- `correlation`
