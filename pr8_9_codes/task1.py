import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

input_file = "gdp_usa_extended.csv"
output_analysis = "gdp_usa_analysis.csv"
output_grouped = "gdp_usa_grouped.csv"

# завантаження даних із csv-файлу
try:
    df = pd.read_csv(input_file)
    print("файл успішно завантажено")
except FileNotFoundError:
    print(f"помилка: файл {input_file} не знайдено")
    exit()

# базовий аналіз даних
print("\nпочатковий dataframe:")
print(df)

print("\nперші 3 рядки dataframe:")
print(df.head(3))

print("\nтипи даних у стовпцях:")
print(df.dtypes)

print("\nрозмір dataframe (рядки, стовпці):")
print(df.shape)

print("\nописова статистика:")
print(df.describe().round(2))

# попереднє оброблення даних та зміна типів
df["Year"] = df["Year"].astype(int)
df["Population"] = df["Population"].astype(int)

# додавання розрахункових стовпців
df["Total_GDP_bln"] = (
    df["GDP per capita (current US$)"] * df["Population"] / 1_000_000_000
).round(2)
df["Decade"] = (df["Year"] // 10 * 10).astype(str) + "s"

print("\ndataframe з новими стовпцями (перші 5 рядків):")
print(df.head(5))

# фільтрація записів за умовою (ввп на душу населення > 50000)
filtered_df = df[df["GDP per capita (current US$)"] > 50000]
print("\nрезультат фільтрації (GDP per capita > 50000):")
print(filtered_df[["Year", "GDP per capita (current US$)", "Total_GDP_bln", "Inflation_percent"]])

# сортування даних за спаданням ввп на душу населення
sorted_df = df.sort_values(by="GDP per capita (current US$)", ascending=False)
print("\nтоп-5 років за GDP per capita (після сортування):")
print(sorted_df[["Year", "GDP per capita (current US$)", "Total_GDP_bln"]].head(5))

# групування та агрегація за десятиліттями
grouped_df = (
    df.groupby("Decade")
    .agg(
        GDP_mean=("GDP per capita (current US$)", "mean"),
        GDP_min=("GDP per capita (current US$)", "min"),
        GDP_max=("GDP per capita (current US$)", "max"),
        Inflation_mean=("Inflation_percent", "mean"),
    )
    .round(2)
)
print("\nрезультат групування за десятиліттями:")
print(grouped_df)

# кількість унікальних значень у стовпцях
print("\nкількість унікальних десятиліть:", df["Decade"].nunique())
print("кількість унікальних років:", df["Year"].nunique())

# збереження результатів аналізу у нові csv-файли
sorted_df.to_csv(output_analysis, index=False)
grouped_df.to_csv(output_grouped)
print(f"\nрезультати збережено у файли {output_analysis} та {output_grouped}")
