import numpy as np
import pandas as pd
import pytest

from src import analysis


class TestAnalysis:
    @pytest.fixture
    def df(self):
        return pd.DataFrame({
            "order_id": [1, 2, 2, 3],
            "user_id": [10, 11, 11, 12],
            "date": ["2024-01-06", "2024-01-07", "2024-01-07", "2024-01-08"],
            "region": ["A", "B", "B", "C"],
            "city": ["X", "Y", "Y", "Z"],
            "platform": ["App", "Web", "Web", "Mobile"],
            "traffic_source": ["Direct", "Email", "Email", "Social"],
            "category": ["tech", "home", "home", "tech"],
            "product_name": ["a", "b", "b", "c"],
            "price": [100.0, 200.0, 200.0, 300.0],
            "quantity": [1, 2, 2, 1],
            "discount": [10, 0, 0, 20],
            "payment_method": ["Card", "Cash", "Cash", "Card"],
            "delivery_days": [1, 3, 3, 2],
            "is_returned": [0, 1, 1, np.nan],
            "rating": [5.0, 4.0, 4.0, 3.0],
            "revenue": [100.0, 400.0, 400.0, 300.0],
        })

    def test_clean_data__ok(self, df):
        result = analysis.clean_data(df.copy())
        assert len(result) == 3
        assert result["is_returned"].isna().sum() == 0

    def test_add_futures__ok(self, df):
        df = analysis.clean_data(df)
        result = analysis.add_futures(df.copy())
        assert "revenue_discnt" in result.columns
        assert result.loc[result["order_id"] == 1, "revenue_discnt"].iloc[0] == 90.0

    def test_read_data_chunks__ok(self, tmp_path, df):
        path = tmp_path / "test.csv"
        df.to_csv(path, index=False)
        chunks = list(analysis.read_data_chunks(path, chunk_size=2))
        assert len(chunks) == 2
        assert sum(len(chunk) for chunk in chunks) == len(df)

    def test_count_rows__ok(self, tmp_path, df):
        path = tmp_path / "test.csv"
        df.to_csv(path, index=False)
        row_count = analysis.count_rows(path, chunk_size=2)
        assert row_count == len(df)

    def test_revenue_values__ok(self, df):
        df = analysis.add_futures(analysis.clean_data(df))
        values = list(analysis.revenue_values(df))
        assert values == [90.0, 400.0, 240.0]

    def test_make_report__ok(self, df):
        df = analysis.add_futures(analysis.clean_data(df))
        insights = analysis.make_report(df)
        assert len(insights) >= 5
        assert any("Самый активный день" in item for item in insights)
        assert any("выходные" in item for item in insights)

    def test_save_reports__ok(self, tmp_path):
        users = pd.DataFrame({"user_id": [1]})
        returns_cat = pd.DataFrame({"category": ["tech"]})
        returns_city = pd.DataFrame({"city": ["X"]})
        channels = pd.DataFrame({"platform": ["App"]})
        insights = ["one", "two"]
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        path = data_dir / "db.csv"
        path.write_text("a\n1\n")
        reports_dir = analysis.save_reports(path, users, returns_cat, returns_city, channels, insights)
        assert reports_dir.exists()
        assert (reports_dir / "users.csv").exists()
        assert (reports_dir / "returns_category.csv").exists()
        assert (reports_dir / "returns_city.csv").exists()
        assert (reports_dir / "channels.csv").exists()
        assert (reports_dir / "report.txt").exists()
