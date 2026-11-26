import xml.etree.ElementTree as ET


# клас для завантаження та парсингу xml-каталогу товарів
class XmlCatalogLoader:
    def __init__(self, filepath):
        self._filepath = filepath
        self._records = []
        self._shop_name = "Unknown"

    def load(self):
        self._records = []
        try:
            tree = ET.parse(self._filepath)
            root = tree.getroot()
        except FileNotFoundError:
            print(f"помилка: файл {self._filepath} не знайдено")
            return False
        except ET.ParseError as e:
            print(f"помилка структури xml у файлі {self._filepath}: {e}")
            return False
        except OSError as e:
            print(f"помилка відкриття файлу: {e}")
            return False

        self._shop_name = root.attrib.get("shop", "Unknown")

        # обхід усіх елементів product та виділення полів
        for item in root.findall("product"):
            try:
                price_el = item.find("price")
                record = {
                    "ID": item.attrib.get("id", "").strip(),
                    "Available": item.attrib.get("available", "false").lower() == "true",
                    "Name": item.findtext("name", "").strip(),
                    "Brand": item.findtext("brand", "").strip(),
                    "Category": item.findtext("category", "").strip(),
                    "Price": float(price_el.text) if price_el is not None else 0.0,
                    "Currency": price_el.attrib.get("currency", "USD") if price_el is not None else "USD",
                    "Stock": int(item.findtext("stock", "0")),
                    "Rating": float(item.findtext("rating", "0")),
                    "Year": int(item.findtext("year", "0")),
                }
                if record["Name"] and record["Price"] >= 0:
                    self._records.append(record)
            except (ValueError, TypeError):
                continue

        if not self._records:
            print("помилка: у xml-файлі не знайдено коректних записів")
            return False

        print(f"завантажено {len(self._records)} товарів із каталогу {self._shop_name}")
        return True

    def get_records(self):
        return list(self._records)

    def get_shop_name(self):
        return self._shop_name
