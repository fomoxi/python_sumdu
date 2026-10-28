def find_matching_words(sentence: str) -> list[str]:
    words = sentence.split()
    result = []

    for word in words:
        clean_word = word.strip(".,!?:;\"'()[]{}«»—–")
        if len(clean_word) >= 2 and clean_word[0].lower() == clean_word[-1].lower():
            result.append(clean_word)

    return result

def main():
    sentence = input("Введіть речення (щонайменше 7 слів): ").strip()
    words = sentence.split()

    while len(words) < 7:
        print(f"Помилка: у реченні лише {len(words)} слів, а потрібно не менше 7!")
        sentence = input("Введіть речення ще раз: ").strip()
        words = sentence.split()

    matched = find_matching_words(sentence)

    print("\nВведене речення:")
    print(sentence)

    if matched:
        print(f"\nСлова, які починаються і закінчуються на одну й ту саму літеру ({len(matched)}):")
        for w in matched:
            print(f"- {w}")
    else:
        print("\nСлів, які починаються і закінчуються на одну й ту саму літеру, не знайдено.")

if __name__ == "__main__":
    main()
