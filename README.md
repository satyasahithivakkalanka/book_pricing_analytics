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

# 8. Tools and Technologies Used

- Python  
- SQLite  
- Requests  
- BeautifulSoup  
- Pandas  
- Matplotlib  
- Seaborn  
- Statsmodels  

These tools were used for:

- Data collection  
- Data storage  
- Statistical analysis  
- Data visualization  

---

# 9. Conclusion

This project demonstrated a **complete data analytics workflow**, starting from automated web scraping to advanced data analysis and interpretation.

The results showed that **book prices are not strongly influenced by ratings or title characteristics**. However, small pricing differences based on title sentiment were observed.

The project highlights the value of **data-driven decision-making** and demonstrates how real-world data can be transformed into meaningful insights.
