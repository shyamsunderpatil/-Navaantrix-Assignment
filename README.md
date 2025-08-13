# Navaantrix — Data Analyst Assignment Solutions

Repository containing completed assignment tasks for the Data Analyst position at Navaantrix.

**Tasks implemented**
1. CRUD Operations on Sales Dataset (`crud_operations_on_sales_dataset/`)
2. Descriptive & Predictive Analysis with Interactive Dashboard (`descriptive_predictive_dashboard/`)
3. Web Scraping for Product Details (`web_scraping_product_details/`)

---

## Contents (top-level)
- `data/` — (optional) dataset(s). Add `us_supermarket.csv` here or a sample version `us_supermarket_sample.csv`.
- `crud_operations_on_sales_dataset/` — CRUD script and README.
- `descriptive_predictive_dashboard/` — Dash app, code, requirements and README.
- `web_scraping_product_details/` — scraper for Amazon & Flipkart, README and sample output.
- `requirements.txt` — core dependencies (see below).
- `README.md` — this file.
- `.gitignore` — recommended to exclude caches and output files.

---

## Quick start (full repository)

**Prerequisites**
- Python 3.8+
- `pip` available

Install core dependencies (optional — each module has its own requirements):
```bash
pip install -r requirements.txt
```

---

## Task 1 — CRUD Operations on Sales Dataset
**Folder:** `crud_operations_on_sales_dataset/`  
**Purpose:** Demonstrates Create, Read, Update, Delete operations on `data/us_supermarket.csv` using pandas.

**How to run**
```bash
cd crud_operations_on_sales_dataset
pip install -r requirements.txt
python crud_operations.py
```
The script demonstrates:
- `create_record(new_record)`
- `read_records(**filters)`
- `update_records(filter_col, filter_val, update_col, update_val)`
- `delete_records(**filters)`

**Notes**
- The script **backs up** the CSV before modifications (`us_supermarket.csv.bak`).
- If you want to use a sample dataset: `data/us_supermarket_sample.csv`.

---

## Task 2 — Descriptive & Predictive Dashboard (Dash)
**Folder:** `descriptive_predictive_dashboard/`  
**Purpose:** Interactive Plotly Dash app showing descriptive charts (sales trend, sales by product/city) and a 30-day sales forecast.

**How to run**
```bash
cd descriptive_predictive_dashboard
pip install -r requirements.txt
python dashboard.py
# open http://127.0.0.1:8050 in your browser
```

**Features**
- Line chart (daily/monthly sales)
- Bar charts (sales by sub-category and city)
- Forecast (Ridge regression, next 30 days)
- Filters: Date range, City, Sub-Category
- Cross-filtering: click a chart to filter others

**Notes**
- The app expects dataset at `../data/us_supermarket.csv` — modify `DATA_PATH` in `dashboard.py` if needed.
- Use `app.run()` (Dash ≥3) — code is compatible with Dash 3.x. If you have Dash 2.x, change to `app.run_server()`.

---

## Task 3 — Web Scraping (Amazon & Flipkart)
**Folder:** `web_scraping_product_details/`  
**Purpose:** Simple & robust script that searches Flipkart and Amazon and saves product `Name`, `Price`, and `Rating` to `products.xlsx`.

**How to run**
```bash
cd web_scraping_product_details
pip install -r requirements.txt
python scrape_products.py
# enter product search term when prompted
```

**Output**
- `products.xlsx` — Excel file with scraped product data.

##Important notes
- Amazon and Flipkart can block automated requests or change HTML structure; the script includes basic error handling and throttling.
- For production or blocked sites consider using Selenium with a webdriver, rotating user agents, or proxies.



## Recommended changes & improvements
1. Add small sample dataset to `data/` and exclude the real dataset from git if large.
2. Add per-module README files with screenshots.
   


## Contact
Prepared by: Shyamsunder Patil 
Email: shyamsunderst27@gmail.com



## License
This project is available under the **MIT License**. See `LICENSE` for details.
