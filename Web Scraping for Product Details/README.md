# Web Scraping – Amazon & Flipkart

## Overview
This project scrapes **product details** from **Amazon** and **Flipkart** based on a search term you provide.  
It collects:
- **Product Name**
- **Price**
- **Ratings**

The results are saved in an **Excel file** (`products.xlsx`).

---

## ⚙ Requirements
Before running the script, install the required Python libraries:
```bash
pip install -r requirements.txt
```
`requirements.txt` contains:
- `requests`
- `beautifulsoup4`
- `pandas`
- `openpyxl`

---

##  How to Run
1. **Open a terminal or command prompt** in the project folder.
2. Run the script:
   ```bash
   python scrape_products.py
   ```
3. Enter a **search term** (example: `laptop`, `mobile`, `headphones`).
4. Wait while the script fetches data from **Flipkart** and **Amazon**.
5. The results will be saved to:
   ```
   products.xlsx
   ```

---

##  Example Output
| Site      | Name                  | Price    | Rating |
|-----------|-----------------------|----------|--------|
| Flipkart  | HP Laptop 15s         | ₹45,990  | 4.3    |
| Amazon    | Dell Inspiron 3520    | ₹47,999  | 4.2    |

---

##  Notes
- The script scrapes the **first page only** for simplicity.
- Some products might not have price or rating displayed (marked as `N/A`).
- If you get empty results, it may be due to **website blocking** or **page structure changes**.
- For more reliability, you can use **Selenium** with a web driver.
