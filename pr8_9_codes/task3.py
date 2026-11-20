import string
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import gutenberg, stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer

# завантаження необхідних корпусів nltk за потреби
for resource in ["gutenberg", "stopwords", "wordnet", "omw-1.4"]:
    nltk.download(resource, quiet=True)

# список доступних текстів та завантаження тексту за варіантом 5
print("доступні тексти project gutenberg:")
print(gutenberg.fileids())

text_name = "blake-poems.txt"
words = gutenberg.words(text_name)

# 1. визначення кількості слів та унікальних слів у тексті
total_tokens = len(words)
unique_tokens = len(set(words))
unique_lower = len(set(w.lower() for w in words))

print(f"\nаналіз тексту: {text_name}")
print(f"загальна кількість токенів (слів і знаків): {total_tokens}")
print(f"кількість унікальних токенів (з урахуванням регістру): {unique_tokens}")
print(f"кількість унікальних токенів (у нижньому регістрі): {unique_lower}")
print(f"частка унікальних слів (у нижньому регістрі): {unique_lower / total_tokens * 100:.2f}%")

# 2. 10 найбільш уживаних слів у початковому тексті
fdist_raw = FreqDist(words)
top_10_raw = fdist_raw.most_common(10)
print("\n10 найбільш уживаних слів у початковому тексті:")
print(top_10_raw)

raw_labels, raw_counts = zip(*top_10_raw)
plt.figure(figsize=(9, 5))
plt.bar(raw_labels, raw_counts, color="steelblue")
plt.title(f"Top 10 most common words in {text_name} (raw)", fontsize=13)
plt.xlabel("Word / Token", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.show()

# 3. видалення стоп-слів і пунктуації
stop_words = set(stopwords.words("english"))
punct_table = str.maketrans("", "", string.punctuation)

cleaned_words = []
for word in words:
    cleaned = word.translate(punct_table).lower()
    if cleaned.isalpha() and cleaned not in stop_words:
        cleaned_words.append(cleaned)

print(f"\nкількість слів після видалення стоп-слів і пунктуації: {len(cleaned_words)}")
print("приклад перших 15 очищених слів:", cleaned_words[:15])

fdist_clean = FreqDist(cleaned_words)
top_10_clean = fdist_clean.most_common(10)
print("\n10 найбільш уживаних слів після очищення:")
print(top_10_clean)

clean_labels, clean_counts = zip(*top_10_clean)
plt.figure(figsize=(9, 5))
plt.bar(clean_labels, clean_counts, color="seagreen")
plt.title(f"Top 10 most common words in {text_name} (cleaned)", fontsize=13)
plt.xlabel("Word", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.show()

# 4. лематизація слів та визначення 10 найбільш уживаних слів
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(w) for w in cleaned_words]

fdist_lemma = FreqDist(lemmatized_words)
top_10_lemma = fdist_lemma.most_common(10)
print("\n10 найбільш уживаних слів після лематизації:")
print(top_10_lemma)
