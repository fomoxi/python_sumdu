def analyze_latin_letters(text: str) -> tuple[set[str], set[str]]:
    seen = set()
    repeated = set()

    for char in text.lower():
        if "a" <= char <= "z":
            if char in seen:
                repeated.add(char)
            else:
                seen.add(char)

    set_at_least_two = repeated
    set_exactly_once = seen - repeated
    return set_at_least_two, set_exactly_once

def main():
    text = input("Введіть текст із латинських літер: ").strip()
    while not any("a" <= ch <= "z" for ch in text.lower()):
        print("Помилка: текст повинен містити хоча б одну латинську літеру")
        text = input("Введіть текст ще раз: ").strip()

    set_ge_2, set_eq_1 = analyze_latin_letters(text)

    print("\nАналіз тексту:")
    print(f'Початковий текст: "{text}"')

    print("\nа) Множина літер, які входять не менше ніж 2 рази:")
    if set_ge_2:
        print(f"   Множина: {set_ge_2}")
        print(f"   В алфавітному порядку: {', '.join(sorted(set_ge_2))}")
    else:
        print("   Таких літер немає (усі літери зустрічаються по одному разу).")

    print("\nб) Множина літер, які входять рівно 1 раз:")
    if set_eq_1:
        print(f"   Множина: {set_eq_1}")
        print(f"   В алфавітному порядку: {', '.join(sorted(set_eq_1))}")
    else:
        print("   Таких літер немає (усі літери повторюються від 2 разів).")


if __name__ == "__main__":
    main()
