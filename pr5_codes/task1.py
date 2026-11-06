import requests
import json
import csv

# основні параметри програми
country = "US"
indicator = "NY.GDP.PCAP.CD"
years = "1991:2019"
json_filename = "gdp_usa.json"
csv_filename = "gdp_usa.csv"

url = (
    f"https://api.worldbank.org/v2/country/{country}/"
    f"indicator/{indicator}?date={years}&format=json&per_page=100"
)


# одержання даних через api світового банку
def get_api_data(api_url):
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            print("помилка отримання даних:", response.status_code)
            return None

        data = response.json()
        if not isinstance(data, list) or len(data) < 2 or not data[1]:
            print("помилка: одержані дані відсутні або некоректні")
            return None

        print("дані успішно отримано")
        return data
    except requests.exceptions.RequestException as e:
        print("помилка виконання http-запиту:", e)
        return None
    except ValueError:
        print("помилка обробки json-відповіді")
        return None


# збереження даних у формат json
def save_to_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"створено файл {filename}")
        return True
    except OSError as e:
        print("помилка запису json-файлу:", e)
        return False


# перетворення даних та збереження у формат csv
def convert_to_csv(data, filename):
    csv_data = []
    for item in data[1]:
        if isinstance(item, dict) and item.get("value") is not None:
            country_name = item.get("country", {}).get("value", "")
            year_val = item.get("date", "")
            gdp_val = round(float(item["value"]), 2)
            csv_data.append([country_name, year_val, gdp_val])

    if not csv_data:
        print("помилка: немає коректних даних для запису у csv")
        return False

    csv_data.sort(key=lambda x: int(x[1]))

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Country", "Year", "GDP per capita (current US$)"])
            writer.writerows(csv_data)
        print(f"створено файл {filename}")
        return True
    except OSError as e:
        print("помилка запису csv-файлу:", e)
        return False


# виведення змісту json та csv файлів на екран
def display_files(json_file, csv_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            json_content = json.load(file)
        print("\nзміст json (перший запис):")
        print("-" * 50)
        for item in json_content[1][:1]:
            print(json.dumps(item, ensure_ascii=False, indent=4))
    except (OSError, ValueError, IndexError) as e:
        print("помилка читання json-файлу:", e)

    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            print("\nзміст csv:")
            print("-" * 50)
            for row in reader:
                print(f"{row[0]}, {row[1]}, {row[2]}")
    except OSError as e:
        print("помилка читання csv-файлу:", e)


# головна частина програми
data = get_api_data(url)
if data is not None:
    if save_to_json(data, json_filename) and convert_to_csv(data, csv_filename):
        display_files(json_filename, csv_filename)
