import csv

input_filename = "gdp_usa.csv"


# зчитування даних із вхідного csv-файлу
def load_csv_data(filename):
    records = []
    try:
        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            print("Country, Year: GDP per capita (current US$)")
            print("-" * 50)
            for row in reader:
                try:
                    value = float(row["GDP per capita (current US$)"])
                    country = row["Country"]
                    year = row["Year"]
                    print(f"{country}, {year}: {value}")
                    records.append({
                        "Country": country,
                        "Year": year,
                        "Value": value
                    })
                except (ValueError, KeyError):
                    continue
        return records
    except FileNotFoundError:
        print(f"файл {filename} не знайдено")
        return None
    except OSError as e:
        print("помилка відкриття файлу:", e)
        return None


# пошук найнижчого та найвищого значень показника
def find_min_max(records):
    if not records:
        return None, None
    min_record = min(records, key=lambda x: x["Value"])
    max_record = max(records, key=lambda x: x["Value"])
    return min_record, max_record


# збереження результатів пошуку у новий csv-файл
def save_search_results(filename, min_rec, max_rec):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Type",
                "Country",
                "Year",
                "GDP per capita (current US$)"
            ])
            writer.writerow([
                "Minimum",
                min_rec["Country"],
                min_rec["Year"],
                min_rec["Value"]
            ])
            writer.writerow([
                "Maximum",
                max_rec["Country"],
                max_rec["Year"],
                max_rec["Value"]
            ])
        print(f"\nрезультати успішно збережено у файл {filename}")
        return True
    except OSError as e:
        print("помилка запису файлу:", e)
        return False


# головна частина програми
data_records = load_csv_data(input_filename)

if data_records:
    output_filename = input(
        "\nвведіть назву нового файлу для збереження (наприклад, result.csv): "
    ).strip()

    while not output_filename or not output_filename.endswith(".csv"):
        output_filename = input(
            "помилка, назва файлу має закінчуватися на .csv, введіть ще раз: "
        ).strip()

    min_row, max_row = find_min_max(data_records)

    print("\nрезультати пошуку:")
    print("-" * 50)
    print(
        f"найнижче значення: {min_row['Country']}, "
        f"{min_row['Year']} рік -> {min_row['Value']}"
    )
    print(
        f"найвище значення: {max_row['Country']}, "
        f"{max_row['Year']} рік -> {max_row['Value']}"
    )

    if save_search_results(output_filename, min_row, max_row):
        try:
            with open(output_filename, "r", encoding="utf-8") as file:
                print(f"\nвміст створеного файлу {output_filename}:")
                print("-" * 50)
                for line in file:
                    print(line.strip())
        except OSError as e:
            print("помилка читання створеного файлу:", e)
