import json
import os
import matplotlib.pyplot as plt


# клас для експорту результатів у csv, json, графіки png та html звіт
class ReportExporter:
    def __init__(self, output_dir="output"):
        self._output_dir = output_dir
        os.makedirs(self._output_dir, exist_ok=True)

    # збереження таблиці у формат csv
    def export_csv(self, df, filename="filtered_products.csv"):
        path = os.path.join(self._output_dir, filename)
        try:
            df.to_csv(path, index=False, encoding="utf-8")
            print(f"збережено csv-файл: {path}")
            return path
        except OSError as e:
            print("помилка запису csv:", e)
            return None

    # збереження даних у формат json
    def export_json(self, df, filename="filtered_products.json"):
        path = os.path.join(self._output_dir, filename)
        try:
            records = df.to_dict(orient="records")
            with open(path, "w", encoding="utf-8") as file:
                json.dump(records, file, ensure_ascii=False, indent=2)
            print(f"збережено json-файл: {path}")
            return path
        except OSError as e:
            print("помилка запису json:", e)
            return None

    # побудова та збереження двох діаграм matplotlib
    def save_charts(self, category_stats):
        if category_stats.empty:
            print("немає даних для побудови діаграм")
            return []

        saved_paths = []
        categories = category_stats.index.tolist()

        # 1. стовпчаста діаграма середньої ціни за категоріями
        bar_path = os.path.join(self._output_dir, "category_prices.png")
        plt.figure(figsize=(8, 4.8))
        plt.bar(categories, category_stats["Avg_Price"], color="steelblue", width=0.6)
        plt.title("Average product price by category (USD)", fontsize=13)
        plt.xlabel("Category", fontsize=11)
        plt.ylabel("Average price (USD)", fontsize=11)
        plt.grid(axis="y", alpha=0.5)
        plt.tight_layout()
        plt.savefig(bar_path, dpi=150)
        plt.close()
        saved_paths.append(bar_path)
        print(f"збережено графік: {bar_path}")

        # 2. кругова діаграма розподілу кількості товарів за категоріями
        pie_path = os.path.join(self._output_dir, "category_share.png")
        counts = category_stats["Count"].tolist()
        plt.figure(figsize=(7.5, 4.8))
        wedges, texts, autotexts = plt.pie(
            counts,
            labels=categories,
            autopct=lambda pct: f"{pct:.1f}%",
            startangle=120,
        )
        plt.title("Share of products by category", fontsize=13)
        plt.setp(autotexts, size=9, weight="bold")
        plt.legend(wedges, categories, title="Categories", loc="center left", bbox_to_anchor=(1.02, 0.5))
        plt.tight_layout()
        plt.savefig(pie_path, dpi=150)
        plt.close()
        saved_paths.append(pie_path)
        print(f"збережено діаграму: {pie_path}")

        return saved_paths

    # автоматичне формування підсумкового html звіту
    def export_html_report(self, shop_name, summary, category_stats, filtered_df, chart_paths, filename="report.html"):
        path = os.path.join(self._output_dir, filename)
        stats_html = category_stats.to_html(border=0) if not category_stats.empty else "<p>Дані відсутні</p>"
        items_html = filtered_df[["ID", "Name", "Brand", "Category", "Price", "Stock", "Rating", "Total_Value"]].to_html(
            index=False, border=0
        ) if not filtered_df.empty else "<p>Дані відсутні</p>"

        charts_html = ""
        for cpath in chart_paths:
            charts_html += f'<img src="{os.path.basename(cpath)}" style="max-width:520px;margin:10px 0;"><br>\n'

        html_content = f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<title>Звіт аналізу XML-каталогу {shop_name}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 28px; color: #222; }}
h1, h2 {{ color: #1f4e79; }}
table {{ border-collapse: collapse; margin: 12px 0 22px; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; }}
th {{ background: #eef3f8; }}
</style>
</head>
<body>
<h1>Звіт аналізу XML-каталогу ({shop_name})</h1>
<p>Кількість товарів: <b>{summary["count"]}</b> | Залишок на складі: <b>{summary["total_stock"]}</b> |
Загальна вартість: <b>{summary["total_value"]} USD</b> | Середня ціна: <b>{summary["avg_price"]} USD</b> |
Середній рейтинг: <b>{summary["avg_rating"]}</b></p>
<h2>Статистика за категоріями</h2>
{stats_html}
<h2>Візуалізація результатів</h2>
{charts_html}
<h2>Список відфільтрованих товарів</h2>
{items_html}
</body>
</html>
"""
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(html_content)
            print(f"збережено html звіт: {path}")
            return path
        except OSError as e:
            print("помилка запису html звіту:", e)
            return None
