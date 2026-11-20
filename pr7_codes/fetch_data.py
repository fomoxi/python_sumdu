import csv
import io
import zipfile
import requests

# параметри для завантаження даних світового банку (варіант 5)
indicator = "NY.GDP.PCAP.CD"
countries = {"UKR": "Ukraine", "USA": "United States"}
start_year = 1991
end_year = 2019
output_csv = "gdp_ua_usa.csv"

url = f"https://api.worldbank.org/v2/en/indicator/{indicator}?downloadformat=csv"


# завантаження архіву світового банку та збереження даних у csv
def download_world_bank_csv(api_url, filename):
    try:
        response = requests.get(api_url, timeout=30)
        if response.status_code != 200:
            print("помилка завантаження даних:", response.status_code)
            return False

        rows_to_save = []
        with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
            data_files = [
                name for name in archive.namelist()
                if name.startswith(f"API_{indicator}")
            ]
            if not data_files:
                print("помилка: файл даних у архіві не знайдено")
                return False

            with archive.open(data_files[0]) as raw_file:
                lines = [line.decode("utf-8-sig") for line in raw_file]

        reader = csv.reader(lines[4:])
        header = next(reader)

        for row in reader:
            if len(row) > 1 and row[1] in countries:
                country_name = countries[row[1]]
                for year_str, val_str in zip(header[4:], row[4:]):
                    if year_str.isdigit() and start_year <= int(year_str) <= end_year:
                        if val_str:
                            rows_to_save.append([
                                country_name,
                                int(year_str),
                                round(float(val_str), 2),
                            ])

        rows_to_save.sort(key=lambda item: (item[0], item[1]))

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Country", "Year", "GDP per capita (current US$)"])
            writer.writerows(rows_to_save)

        print(f"дані збережено у файл {filename} ({len(rows_to_save)} записів)")
        return True
    except (requests.exceptions.RequestException, zipfile.BadZipFile, OSError, ValueError) as e:
        print("помилка підготовки даних:", e)
        return False


if __name__ == "__main__":
    download_world_bank_csv(url, output_csv)
