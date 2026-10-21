def calculate_x(a, b):
    if a > b:
        x = (a / b) - 1
    elif a == b:
        x = -25
    else:
        x = (a**3 - 5) / a
    return x


def draw_pyramid(n):
    print(f"\nПіраміда чисел для N = {n}:")

    # верхня частина піраміди (разом із серединою)
    for i in range(1, n + 1):
        print(" " * (n - i), end="")
        if i == 1:
            print(1)
        else:
            for j in range(2, i + 1):
                print(j, end=" ")
            print(1)

    # нижня частина піраміди
    for i in range(n - 1, 0, -1):
        print(" " * (n - i), end="")
        if i == 1:
            print(1)
        else:
            for j in range(2, i + 1):
                print(j, end=" ")
            print(1)


print("Завдання 1. Перша функція (обчислення X)")

a = float(input("Введіть число a (a > 0): "))
while a <= 0:
    a = float(input("Число a має бути додатним! Введіть a ще раз: "))

b = float(input("Введіть число b (b > 0): "))
while b <= 0:
    b = float(input("Число b має бути додатним! Введіть b ще раз: "))

result_x = calculate_x(a, b)
print("Результат обчислення X:", result_x)

print("\nЗавдання 1. Друга функція (побудова піраміди)")
n = int(input("Введіть число N від 1 до 10: "))
while n < 1 or n > 10:
    n = int(input("Число має бути в діапазоні від 1 до 10! Введіть ще раз N: "))

draw_pyramid(n)
