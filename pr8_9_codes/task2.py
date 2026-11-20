import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

csv_file = "comptagevelo20152.csv"

# завантаження даних про велодоріжки за 2015 рік (варіант 5)
try:
    df = pd.read_csv(
        csv_file,
        parse_dates=["Date"],
        dayfirst=True,
        index_col="Date",
    )
    if "Unnamed: 1" in df.columns:
        df = df.drop(columns=["Unnamed: 1"])
    print("файл успішно завантажено")
except FileNotFoundError:
    print(f"помилка: файл {csv_file} не знайдено")
    exit()

# первинний аналіз dataframe
print("\nперші 5 рядків dataframe (перші 5 велодоріжок):")
print(df.iloc[:, :5].head())

print("\nінформація про dataframe:")
df.info()

print("\nописова статистика (перші 5 велодоріжок):")
print(df.iloc[:, :5].describe().round(1))

# загальна кількість велосипедистів за 2015 рік для всіх велодоріжок
total_cyclists = int(df.sum().sum())
print(f"\nзагальна кількість велосипедистів за 2015 рік (усі велодоріжки): {total_cyclists}")

# групування даних за місяцями
monthly_df = df.groupby(df.index.month).sum()

month_names = {
    1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
    5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
    9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень",
}

# найбільш популярний місяць для трьох обраних велодоріжок
selected_paths = ["Berri1", "Maisonneuve_2", "Parc"]
print("\nнайбільш популярний місяць для трьох обраних велодоріжок:")
for path in selected_paths:
    best_month = int(monthly_df[path].idxmax())
    max_count = int(monthly_df[path].max())
    print(f"  {path}: {month_names[best_month]} ({best_month}-й місяць) -> {max_count} велосипедистів")

# динаміка використання велодоріжки Berri1 за місяцями
target_path = "Berri1"
berri_monthly = monthly_df[target_path]
print(f"\nдинаміка використання велодоріжки {target_path} за місяцями (2015):")
for month_num, count in berri_monthly.items():
    print(f"  {month_num:2d} ({month_names[month_num]:8s}): {int(count)}")

# побудова графіка зміни кількості велосипедистів за місяцями
months_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
plt.figure(figsize=(10, 5))
plt.plot(berri_monthly.index, berri_monthly.values, marker="o", linewidth=2, color="tab:blue")
plt.title(f"Monthly cyclists on {target_path} bike path (2015)", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Number of cyclists", fontsize=12)
plt.xticks(range(1, 13), months_labels)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()
