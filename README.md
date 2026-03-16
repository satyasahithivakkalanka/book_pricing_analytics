# Automated Web Crawling and Data Analytics of Online Book Listings

## Data Source
https://books.toscrape.com

---

# 1. Introduction

The objective of this project is to demonstrate a complete real-world data analytics pipeline that includes web crawling, database creation, descriptive analysis, regression analysis, and text-based analytics.

The website **Books to Scrape** was selected as the data source because it provides a structured, multi-page dataset that is well-suited for web scraping and statistical analysis.

Using Python, we automatically collected book information from multiple pages, stored the data in a SQLite database, and performed multiple analytical methods to extract meaningful insights. This project demonstrates practical skills in data acquisition, storage, analysis, and interpretation.

---

# 2. Data Collection (Web Crawling)

Python along with the **Requests** and **BeautifulSoup** libraries was used to scrape data from the website. The crawler automatically accessed all catalogue pages and extracted the following attributes for each book:

- Book Title  
- Price  
- Rating  
- Category  
- Title Length  
- Presence of Positive Words in Title  

During the scraping process, data cleaning was applied by:

- Removing special characters  
- Converting numeric values into appropriate formats  

A total of **over 1,000 book records** were successfully collected from the website, which satisfies the project requirement of collecting at least **250 records**.

---

# 3. Database Design

A **SQLite database** named `books.db` was created to store all scraped data.

The data was stored in a table named `books` with the following fields:

- `id` (Primary Key)  
- `title`  
- `price`  
- `rating`  
- `category`  
- `title_length`  
- `has_positive_word`  

The database contains **over 1,000 rows** and includes more than four data fields, fully meeting the database requirements.

SQL queries were used to validate and retrieve data for further analysis.

---

# 4. Descriptive Analysis and Data Visualization

Descriptive statistics were generated to understand the overall dataset.

## Summary Statistics

- **Average Book Price:** $35.07  
- **Average Rating:** 2.92  
- **Average Title Length:** 39 characters  

## Visualizations Created

- Histogram showing the distribution of book prices  
- Bar chart showing rating distribution  
- Category-wise average pricing for the top 10 categories  

These descriptive results provide a clear understanding of how prices and ratings are distributed across various book categories.

---

# 5. First Analysis – Regression Analysis

## Objective

To analyze whether **book ratings can predict book prices**.

## Method Used

**Ordinary Least Squares (OLS) Regression** using the **Statsmodels** library.

## Results

- **R² Value:** 0.001  
- **Regression Coefficient for Rating:** 0.2836  
- **p-value:** 0.208  

## Interpretation

The regression results show that book ratings have a **very weak and statistically insignificant relationship with book prices**. This indicates that book pricing is not strongly driven by customer ratings.

## Why This Is Interesting

Many users assume that higher ratings lead to higher prices. This analysis shows that, in this dataset, that assumption does not hold true.

---

# 6. Second Analysis – Title Sentiment Analysis

This analysis tested whether book titles that contain **positive words** influence book ratings and pricing.

## Results

### Average Rating
- Without positive words: **2.93**  
- With positive words: **2.79**

### Average Price
- Without positive words: **$34.88**  
- With positive words: **$38.12**

## Interpretation

Books with positive words in their titles tend to be **slightly more expensive**, but they **do not receive higher customer ratings**.

## Why This Is Interesting

This result suggests that **marketing language in book titles may influence pricing strategies**, but it does not necessarily improve customer satisfaction.

---

# 7. Third Analysis – Title Length vs Price

This analysis examined whether **longer book titles are associated with higher prices**.

## Result

- **Correlation Coefficient:** 0.0067  

## Interpretation

There is **almost no relationship** between title length and book pricing. Title length has **no meaningful impact on price**.

---

# 8. Fourth Analysis – NLP Text Analysis of Book Titles

To further explore the textual characteristics of book titles, **Natural Language Processing (NLP)** techniques were applied.

## Methods Used

The following text analytics techniques were performed:

### Word Frequency Analysis
Common words appearing in book titles were extracted after removing stopwords and punctuation. This analysis helps identify frequently used keywords in book titles across the catalog.

### TF-IDF (Term Frequency – Inverse Document Frequency)
TF-IDF was used to determine which words are most important within book titles relative to the entire dataset. This helps highlight distinctive keywords that appear frequently in specific titles but less often overall.

### Sentiment Scoring
Sentiment analysis was applied to evaluate whether book titles generally convey positive, neutral, or negative language. A sentiment scoring method was used to assign polarity values to titles.

## Key Observations

- Words related to **adventure, mystery, love, and life** appeared frequently in book titles.
- TF-IDF analysis identified distinctive words that differentiate books within similar categories.
- Most book titles exhibited **neutral sentiment**, with a smaller proportion containing strongly positive or negative wording.

## Interpretation

The NLP analysis provides insights into how language is used in book titles and how certain words may be used for marketing appeal. While title wording may influence reader interest, it does not necessarily correlate strongly with book ratings or pricing.

---

# 9. Tools and Technologies Used

- Python  
- SQLite  
- Requests  
- BeautifulSoup  
- Pandas  
- Matplotlib  
- Seaborn  
- Statsmodels  
- Scikit-learn (TF-IDF)  
- NLTK / TextBlob (Sentiment Analysis)

These tools were used for:

- Data collection  
- Data storage  
- Statistical analysis  
- Natural language processing  
- Data visualization  

---

# 10. Conclusion

This project demonstrated a **complete data analytics workflow**, starting from automated web scraping to advanced data analysis and interpretation.

The results showed that **book prices are not strongly influenced by ratings or title characteristics**. However, small pricing differences based on title sentiment were observed. Additionally, NLP analysis of book titles revealed common language patterns used in book marketing but showed limited impact on pricing or ratings.

The project highlights the value of **data-driven decision-making** and demonstrates how real-world data can be transformed into meaningful insights using statistical analysis and natural language processing.
