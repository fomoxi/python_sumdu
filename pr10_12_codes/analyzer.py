import pandas as pd


# клас для фільтрації та статистичного аналізу даних каталогу
class CatalogAnalyzer:
    def __init__(self, records):
        self._df = pd.DataFrame(records)
        self._df["Total_Value"] = (self._df["Price"] * self._df["Stock"]).round(2)
        self._filtered_df = self._df.copy()

    def get_dataframe(self):
        return self._df.copy()

    def get_filtered(self):
        return self._filtered_df.copy()

    def get_categories(self):
        return sorted(self._df["Category"].unique().tolist())

    def reset_filters(self):
        self._filtered_df = self._df.copy()

    # застосування фільтрів за параметрами користувача
    def apply_filters(self, category=None, max_price=None, min_rating=None, only_available=False):
        result = self._df.copy()

        if category:
            result = result[result["Category"].str.lower() == category.lower()]
        if max_price is not None:
            result = result[result["Price"] <= max_price]
        if min_rating is not None:
            result = result[result["Rating"] >= min_rating]
        if only_available:
            result = result[result["Available"]]

        self._filtered_df = result.sort_values(by="Price", ascending=False)
        return self._filtered_df.copy()

    # обчислення загальних статистичних показників
    def get_summary(self):
        df = self._filtered_df
        if df.empty:
            return {
                "count": 0,
                "total_stock": 0,
                "total_value": 0.0,
                "avg_price": 0.0,
                "min_price": 0.0,
                "max_price": 0.0,
                "avg_rating": 0.0,
            }

        return {
            "count": int(len(df)),
            "total_stock": int(df["Stock"].sum()),
            "total_value": round(float(df["Total_Value"].sum()), 2),
            "avg_price": round(float(df["Price"].mean()), 2),
            "min_price": round(float(df["Price"].min()), 2),
            "max_price": round(float(df["Price"].max()), 2),
            "avg_rating": round(float(df["Rating"].mean()), 2),
        }

    # групування та агрегація даних за категоріями
    def get_category_stats(self):
        df = self._filtered_df
        if df.empty:
            return pd.DataFrame()

        stats = (
            df.groupby("Category")
            .agg(
                Count=("ID", "count"),
                Avg_Price=("Price", "mean"),
                Min_Price=("Price", "min"),
                Max_Price=("Price", "max"),
                Total_Stock=("Stock", "sum"),
                Total_Value=("Total_Value", "sum"),
            )
            .round(2)
            .sort_values(by="Avg_Price", ascending=False)
        )
        return stats
