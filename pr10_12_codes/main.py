import pandas as pd
from xml_loader import XmlCatalogLoader
from analyzer import CatalogAnalyzer
from exporter import ReportExporter

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


# зчитування необов'язкового дійсного числа з перевіркою
def read_optional_float(prompt):
    while True:
        raw = input(prompt).strip()
        if not raw:
            return None
        try:
            val = float(raw)
            if val < 0:
                print("помилка: значення не може бути від'ємним")
                continue
            return val
        except ValueError:
            print("помилка: введіть коректне число або натисніть enter")


# головний цикл інтерактивної програми
def main():
    default_file = "products.xml"
    loader = XmlCatalogLoader(default_file)
    if not loader.load():
        return

    analyzer = CatalogAnalyzer(loader.get_records())
    exporter = ReportExporter("output")

    while True:
        print("\n=== меню аналізу xml-каталогу ===")
        print("1 - завантажити інший xml-файл")
        print("2 - показати товари та загальну статистику")
        print("3 - відфільтрувати товари за параметрами")
        print("4 - показати статистику за категоріями")
        print("5 - експортувати результати (csv, json, графіки, html)")
        print("6 - скинути фільтри")
        print("0 - вихід")

        choice = input("оберіть дію (0-6): ").strip()

        if choice == "1":
            new_path = input("введіть назву xml-файлу: ").strip()
            new_loader = XmlCatalogLoader(new_path)
            if new_loader.load():
                loader = new_loader
                analyzer = CatalogAnalyzer(loader.get_records())

        elif choice == "2":
            df = analyzer.get_filtered()
            summary = analyzer.get_summary()
            print("\nтовари у вибірці:")
            if df.empty:
                print("записи за заданими умовами відсутні")
            else:
                print(df[["ID", "Name", "Brand", "Category", "Price", "Stock", "Rating", "Total_Value"]].to_string(index=False))
            print(
                f"\nпідсумок: товарів = {summary['count']}, залишок = {summary['total_stock']} шт, "
                f"вартість = {summary['total_value']} usd, середня ціна = {summary['avg_price']} usd, "
                f"середній рейтинг = {summary['avg_rating']}"
            )

        elif choice == "3":
            categories = analyzer.get_categories()
            print("доступні категорії:", ", ".join(categories))
            cat_input = input("категорія (enter - усі): ").strip()
            if cat_input and cat_input.lower() not in [c.lower() for c in categories]:
                print("помилка: такої категорії немає у каталозі")
                continue

            max_price = read_optional_float("максимальна ціна usd (enter - без обмежень): ")
            min_rating = read_optional_float("мінімальний рейтинг 0-5 (enter - без обмежень): ")
            avail_input = input("тільки в наявності? (y/n): ").strip().lower()
            only_avail = avail_input in ("y", "yes", "т", "так")

            filtered = analyzer.apply_filters(
                category=cat_input or None,
                max_price=max_price,
                min_rating=min_rating,
                only_available=only_avail,
            )
            print(f"знайдено записів після фільтрації: {len(filtered)}")

        elif choice == "4":
            stats = analyzer.get_category_stats()
            if stats.empty:
                print("немає даних для групування")
            else:
                print("\nстатистика за категоріями:")
                print(stats)

        elif choice == "5":
            df = analyzer.get_filtered()
            if df.empty:
                print("помилка: вибірка порожня, нічого зберігати")
                continue
            stats = analyzer.get_category_stats()
            summary = analyzer.get_summary()
            exporter.export_csv(df)
            exporter.export_json(df)
            charts = exporter.save_charts(stats)
            exporter.export_html_report(loader.get_shop_name(), summary, stats, df, charts)

        elif choice == "6":
            analyzer.reset_filters()
            print("фільтри скинуто до повного каталогу")

        elif choice == "0":
            print("завершення роботи програми")
            break
        else:
            print("помилка: оберіть пункт меню від 0 до 6")


if __name__ == "__main__":
    main()
