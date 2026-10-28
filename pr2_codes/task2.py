def remove_second_and_penultimate(elements: list) -> tuple[list, any, any]:
    lst = list(elements)
    penultimate_item = lst.pop(-2)
    second_item = lst.pop(1)
    return lst, second_item, penultimate_item

def main():
    raw_input = input("Введіть елементи списку через пробіл: ").strip()
    items = raw_input.split()

    while len(items) < 4:
        print(f"Помилка: введено {len(items)} елементів, а потрібно щонайменше 4!")
        raw_input = input("Введіть елементи списку ще раз: ").strip()
        items = raw_input.split()

    print(f"\nПочатковий список ({len(items)} елементів):")
    print(items)

    updated_list, second, penultimate = remove_second_and_penultimate(items)

    print(f"\nВидалено 2-й елемент (індекс 1): '{second}'")
    print(f"Видалено передостанній елемент (індекс -2): '{penultimate}'")

    print(f"\nОновлений список ({len(updated_list)} елементів):")
    print(updated_list)

if __name__ == "__main__":
    main()
