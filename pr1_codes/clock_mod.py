def count_clock_strikes():
    total_12h = 0
    total_24h = 0
    print("Година | Ударів (12-год) | Ударів (прямий рахунок)")
    print("-" * 45)
    for hour in range(0, 16):
        if hour == 0 or hour == 12:
            strikes_12h = 12
        elif hour < 12:
            strikes_12h = hour
        else:
            strikes_12h = hour - 12

        strikes_24h = hour
        total_12h += strikes_12h
        total_24h += strikes_24h
        print(f" {hour:02d}:00 |    {strikes_12h:2d}    |   {strikes_24h:2d}")

    print("-" * 45)
    print("Загальна кількість ударів (класичний циферблат 1-12):", total_12h)
    print("Загальна кількість ударів (якщо рахувати прямо за годинами 0..15):", total_24h)
    return total_12h
