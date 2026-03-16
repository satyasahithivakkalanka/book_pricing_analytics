"""
nlp_analysis.py

NLP analysis of book titles from the books.toscrape.com dataset.

Techniques used:
  1. Word frequency analysis
  2. TF-IDF keyword extraction  (scikit-learn)
  3. Custom sentiment scoring   (rule-based lexicon)
  4. Word cloud visualization   (matplotlib)
  5. Sentiment vs. price / rating analysis
"""

import sqlite3
import re
import math
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# 0. LOAD DATA
conn = sqlite3.connect("books.db")
df = pd.read_sql_query("SELECT title, price, rating FROM books", conn)
conn.close()

print(f"Loaded {len(df):,} book records.\n")

# 1. TEXT CLEANING

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "in", "to", "for", "on",
    "at", "by", "is", "it", "its", "with", "from", "as", "be",
    "this", "that", "s", "my", "your", "his", "her", "their",
    "i", "we", "you", "he", "she", "they", "not", "but", "so",
    "up", "out", "about", "into", "than", "more", "1", "2", "3",
    "no", "are", "was", "were", "has", "have", "had", "do", "does",
}

def clean_title(text):
    """Lowercase, strip punctuation, remove stopwords."""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = [w for w in text.split() if w not in STOPWORDS and len(w) > 1]
    return tokens

df["tokens"] = df["title"].apply(clean_title)
df["clean_title"] = df["tokens"].apply(lambda t: " ".join(t))

# 2. WORD FREQUENCY ANALYSIS

all_words = [word for tokens in df["tokens"] for word in tokens]
word_freq = Counter(all_words)
top_words = word_freq.most_common(20)

print("TOP 20 MOST FREQUENT WORDS IN TITLES:")
for word, count in top_words:
    print(f"  {word:<20} {count}")

# 3. TF-IDF KEYWORD EXTRACTION

# Treats each title as a "document" — words with high TF-IDF
# are distinctive to individual titles, not just common everywhere.

vectorizer = TfidfVectorizer(max_features=500, min_df=2)
tfidf_matrix = vectorizer.fit_transform(df["clean_title"])
feature_names = vectorizer.get_feature_names_out()

# Mean TF-IDF score per word across all titles
mean_tfidf = tfidf_matrix.mean(axis=0).A1
tfidf_scores = dict(zip(feature_names, mean_tfidf))
top_tfidf = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:20]

print("\nTOP 20 TF-IDF KEYWORDS (most distinctive across titles):")
for word, score in top_tfidf:
    print(f"  {word:<20} {score:.4f}")
# 4. CUSTOM SENTIMENT SCORING
# A concise rule-based lexicon relevant to book marketing language.
# Scoring: positive word = +1, negative word = -1, normalised by title length.

POSITIVE_LEXICON = {
    "love", "best", "perfect", "amazing", "happy", "joy", "success",
    "guide", "wonderful", "great", "beautiful", "good", "new", "life",
    "hope", "dream", "light", "free", "power", "win", "bright",
    "magic", "wild", "hero", "brave", "inspire", "rise", "glory",
    "peace", "true", "bold", "rich", "strong",
}

NEGATIVE_LEXICON = {
    "dark", "dead", "death", "fear", "hate", "war", "evil", "lost",
    "blood", "kill", "black", "shadow", "curse", "doom", "pain",
    "horror", "rage", "ghost", "devil", "silent", "broken", "cold",
    "dangerous", "dirty", "secret", "lie", "fall", "trap",
}

def sentiment_score(tokens):
    if not tokens:
        return 0.0
    pos = sum(1 for t in tokens if t in POSITIVE_LEXICON)
    neg = sum(1 for t in tokens if t in NEGATIVE_LEXICON)
    return (pos - neg) / len(tokens)

df["sentiment"] = df["tokens"].apply(sentiment_score)

# Assign human-readable label
def sentiment_label(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

df["sentiment_label"] = df["sentiment"].apply(sentiment_label)

print("\nSENTIMENT DISTRIBUTION:")
print(df["sentiment_label"].value_counts().to_string())

print("\nAVERAGE PRICE BY SENTIMENT:")
print(df.groupby("sentiment_label")["price"].mean().round(2).to_string())

print("\nAVERAGE RATING BY SENTIMENT:")
print(df.groupby("sentiment_label")["rating"].mean().round(2).to_string())


# 5. VISUALISATIONS
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("NLP Analysis of Book Titles", fontsize=16, fontweight="bold", y=1.01)

# --- 5a. Top 15 word frequencies (bar chart) 
ax = axes[0, 0]
words_plot, counts_plot = zip(*top_words[:15])
colors = plt.cm.Blues_r(np.linspace(0.3, 0.85, 15))
bars = ax.barh(words_plot[::-1], counts_plot[::-1], color=colors[::-1])
ax.set_xlabel("Frequency")
ax.set_title("Top 15 Most Common Words in Titles")
ax.bar_label(bars, padding=3, fontsize=8)
ax.set_xlim(0, max(counts_plot) * 1.15)

# --- 5b. Word cloud via matplotlib scatter 
ax = axes[0, 1]
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("Word Cloud (Top 60 Words)")

top60 = word_freq.most_common(60)
max_count = top60[0][1]
np.random.seed(42)

cmap = plt.colormaps["tab20"]
placed = []

def overlaps(x, y, fs, placed, pad=0.015):
    for px, py, pfs in placed:
        if abs(x - px) < (fs + pfs) * 0.012 + pad and abs(y - py) < 0.06:
            return True
    return False

for word, count in top60:
    font_size = 8 + int(28 * (count / max_count) ** 0.6)
    color = cmap(hash(word) % 20 / 20)
    for _ in range(200):
        x = np.random.uniform(0.03, 0.97)
        y = np.random.uniform(0.05, 0.95)
        if not overlaps(x, y, font_size, placed):
            ax.text(x, y, word, fontsize=font_size, color=color,
                    ha="center", va="center", fontweight="bold", alpha=0.85)
            placed.append((x, y, font_size))
            break

# --- 5c. Sentiment distribution (pie) ---
ax = axes[1, 0]
sentiment_counts = df["sentiment_label"].value_counts()
wedge_colors = ["#4CAF50", "#9E9E9E", "#F44336"]
ax.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%",
    colors=wedge_colors[:len(sentiment_counts)],
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
)
ax.set_title("Sentiment Distribution of Book Titles")

# --- 5d. Average price by sentiment (bar) ---
ax = axes[1, 1]
sentiment_price = df.groupby("sentiment_label")["price"].mean().reindex(
    ["Positive", "Neutral", "Negative"]
).dropna()
bar_colors = ["#4CAF50", "#9E9E9E", "#F44336"][:len(sentiment_price)]
bars = ax.bar(sentiment_price.index, sentiment_price.values, color=bar_colors,
              edgecolor="white", linewidth=1.2)
ax.set_ylabel("Average Price (£)")
ax.set_title("Average Price by Title Sentiment")
ax.set_ylim(0, sentiment_price.max() * 1.2)
ax.bar_label(bars, fmt="£%.2f", padding=4, fontsize=9)
ax.yaxis.grid(True, linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("nlp_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n✅ Chart saved → nlp_analysis.png")

# 6. TF-IDF TOP KEYWORDS BAR CHART
fig, ax = plt.subplots(figsize=(9, 6))
tfidf_words, tfidf_vals = zip(*top_tfidf[:15])
colors = plt.cm.Purples_r(np.linspace(0.3, 0.85, 15))
bars = ax.barh(tfidf_words[::-1], tfidf_vals[::-1], color=colors[::-1])
ax.set_xlabel("Mean TF-IDF Score")
ax.set_title("Top 15 TF-IDF Keywords in Book Titles")
ax.bar_label(bars, fmt="%.4f", padding=3, fontsize=8)
ax.set_xlim(0, max(tfidf_vals) * 1.2)
plt.tight_layout()
plt.savefig("tfidf_keywords.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart saved → tfidf_keywords.png")

print("\n🎉 NLP analysis complete.")
