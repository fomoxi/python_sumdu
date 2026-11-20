import csv
import matplotlib.pyplot as plt
import numpy as np

csv_filename = "gdp_ua_usa.csv"
indicator_name = "GDP per capita (current US$)"


# зчитування даних із csv-файлу та формування словника за країнами
def load_csv_data(filename):
    records = {}
    try:
        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    country = row["Country"].strip()
                    year = int(row["Year"])
                    value = float(row[indicator_name])
                    if country not in records:
                        records[country] = {}
                    records[country][year] = value
                except (ValueError, KeyError):
                    continue

        if len(records) < 2:
            print("помилка: недостатньо даних у файлі для аналізу двох країн")
            return None

        return records
    except FileNotFoundError:
        print(f"файл {filename} не знайдено")
        return None
    except OSError as e:
        print("помилка відкриття файлу:", e)
        return None


# формування масивів numpy та виведення аналізу зміни показника в часі
def prepare_and_analyze(records, country1, country2):
    common_years = sorted(set(records[country1]) & set(records[country2]))
    if not common_years:
        print("помилка: відсутні спільні роки для порівняння")
        return None, None, None

    years = np.array(common_years)
    values1 = np.array([records[country1][y] for y in common_years])
    values2 = np.array([records[country2][y] for y in common_years])

    print(f"показник: {indicator_name} ({years[0]}-{years[-1]})")
    print("-" * 60)
    for name, vals in [(country1, values1), (country2, values2)]:
        min_idx = int(np.argmin(vals))
        max_idx = int(np.argmax(vals))
        avg_val = round(float(np.mean(vals)), 2)
        print(
            f"{name}: старт ({years[0]}) = {vals[0]}, "
            f"кінець ({years[-1]}) = {vals[-1]}, середнє = {avg_val}"
        )
        print(
            f"  min = {vals[min_idx]} ({years[min_idx]} рік), "
            f"max = {vals[max_idx]} ({years[max_idx]} рік)"
        )

    ratio = round(float(values2[-1] / values1[-1]), 2)
    print(f"у {years[-1]} році показник {country2} перевищує {country1} у {ratio} раза")
    return years, values1, values2


# побудова лінійного графіка динаміки показника для двох країн
def plot_line_chart(years, values1, values2, country1, country2):
    plt.figure(figsize=(10, 5))
    plt.plot(years, values1, marker="o", markersize=4, linewidth=2, label=country1)
    plt.plot(years, values2, marker="s", markersize=4, linewidth=2, label=country2)
    plt.title(f"{indicator_name} dynamics for {country1} and {country2}", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel(indicator_name, fontsize=12)
    plt.xticks(years[::2], rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show()


# побудова стовпчастої діаграми для введеної користувачем країни
def plot_bar_chart(years, values, country_name):
    plt.figure(figsize=(10, 5))
    plt.bar(years, values, width=0.7, color="steelblue")
    plt.title(f"{indicator_name} for {country_name}", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel(indicator_name, fontsize=12)
    plt.xticks(years, rotation=45, fontsize=9)
    plt.grid(axis="y", alpha=0.5)
    plt.tight_layout()
    plt.show()


# форматування підпису секторів кругової діаграми
def format_pie_value(pct, allvals):
    absolute = np.round(pct / 100 * np.sum(allvals), 2)
    return f"{pct:.1f}%\n({absolute})"


# побудова кругової діаграми порівняння двох країн за обраний рік
def plot_pie_chart(val1, val2, country1, country2, year):
    data = np.array([val1, val2])
    labels = [country1, country2]

    plt.figure(figsize=(8, 5))
    wedges, texts, autotexts = plt.pie(
        data,
        labels=labels,
        explode=(0.08, 0),
        autopct=lambda pct: format_pie_value(pct, data),
        pctdistance=0.76,
        startangle=140,
    )
    plt.title(f"{indicator_name}: {country1} vs {country2} ({year})", fontsize=13)
    plt.setp(autotexts, size=8, weight="bold")
    plt.legend(
        wedges,
        labels,
        title="Countries",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
    )
    plt.tight_layout()
    plt.show()


# головна частина програми
def main():
    data_records = load_csv_data(csv_filename)
    if data_records is None:
        return

    country_ua = "Ukraine"
    country_other = "United States"

    years_arr, ua_arr, us_arr = prepare_and_analyze(
        data_records, country_ua, country_other
    )
    if years_arr is None:
        return

    # 1. лінійний графік динаміки зміни показника
    plot_line_chart(years_arr, ua_arr, us_arr, country_ua, country_other)

    # 2. введення назви країни та побудова стовпчастої діаграми
    country_map = {name.lower(): name for name in data_records}
    available = ", ".join(data_records.keys())
    user_country = input(
        f"\nвведіть назву країни для стовпчастої діаграми ({available}): "
    ).strip()

    while user_country.lower() not in country_map:
        user_country = input(
            f"помилка, країну не знайдено, введіть одну з ({available}): "
        ).strip()

    selected_country = country_map[user_country.lower()]
    selected_values = np.array(
        [data_records[selected_country][int(y)] for y in years_arr]
    )
    plot_bar_chart(years_arr, selected_values, selected_country)

    # 3. введення року та побудова кругової діаграми
    year_input = input(
        f"\nвведіть рік для кругової діаграми ({years_arr[0]}-{years_arr[-1]}): "
    ).strip()

    while not year_input.isdigit() or int(year_input) not in years_arr:
        year_input = input(
            f"помилка, введіть рік від {years_arr[0]} до {years_arr[-1]}: "
        ).strip()

    selected_year = int(year_input)
    ua_val = data_records[country_ua][selected_year]
    other_val = data_records[country_other][selected_year]
    plot_pie_chart(ua_val, other_val, country_ua, country_other, selected_year)


if __name__ == "__main__":
    main()
