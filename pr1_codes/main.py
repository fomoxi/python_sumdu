from expression_mod import calculate_y
from clock_mod import count_clock_strikes

def main():
    while True:
        print("\nМеню вибору функцій (Завдання 2)")
        print("1 - Обчислити значення виразу y = (a^2 + b^2) / (1 + |c|)")
        print("2 - Знайти кількість ударів годинника від 00 год до 15 год")
        print("0 - Вихід з програми")

        choice = input("Ваш вибір (1, 2 або 0): ")

        if choice == "1":
            print("\nОбчислення виразу y = (a^2 + b^2) / (1 + |c|)")
            a = float(input("Введіть число a: "))
            b = float(input("Введіть число b: "))
            c = float(input("Введіть число c: "))
            y = calculate_y(a, b, c)
            print("Значення виразу y =", y)

        elif choice == "2":
            print("\nПідрахунок ударів годинника")
            count_clock_strikes()

        elif choice == "0":
            print("Вихід з програми. Роботу завершено.")
            break

        else:
            print("Некоректний вибір! Будь ласка, введіть 1, 2 або 0.")

if __name__ == "__main__":
    main()
