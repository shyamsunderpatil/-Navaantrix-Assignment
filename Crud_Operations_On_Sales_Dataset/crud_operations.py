import pandas as pd
import os

# File path
CSV_FILE = r"C:\Users\shyamsunder\OneDrive\Documents\pranjal sir\us_supermarket.csv"


def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, encoding="latin-1")
    else:
        raise FileNotFoundError("CSV file not found.")

def save_data(df):
    df.to_csv(CSV_FILE, index=False, encoding="latin-1")
    print("Changes saved to CSV.")

# CREATE
def create_record(new_record: dict):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    save_data(df)
    print("Record added.")

# READ
def read_records(**kwargs):
    df = load_data()
    query_df = df.copy()
    for col, val in kwargs.items():
        query_df = query_df[query_df[col] == val]
    print(query_df)
    return query_df

# UPDATE
def update_records(filter_col, filter_val, update_col, update_val):
    df = load_data()
    mask = df[filter_col] == filter_val
    df.loc[mask, update_col] = update_val
    save_data(df)
    print(f"Updated {mask.sum()} record(s).")

# DELETE
def delete_records(**kwargs):
    df = load_data()
    original_count = len(df)
    for col, val in kwargs.items():
        df = df[df[col] != val]
    save_data(df)
    deleted_count = original_count - len(df)
    print(f"Deleted {deleted_count} record(s).")

if __name__ == "__main__":
    # Example CREATE
    new_row = {
        "Row ID": 99999,
        "Order ID": "CA-2023-999999",
        "Order Date": "12/31/2023",
        "Ship Date": "01/05/2024",
        "Ship Mode": "Second Class",
        "Customer ID": "CU-99999",
        "Customer Name": "Test Customer",
        "Segment": "Consumer",
        "Country": "United States",
        "City": "Test City",
        "State": "Test State",
        "Postal Code": 99999,
        "Region": "West",
        "Product ID": "OFF-TEST-9999",
        "Category": "Office Supplies",
        "Sub-Category": "Paper",
        "Product Name": "Test Product",
        "Sales": 100.0,
        "Quantity": 5,
        "Discount": 0.1,
        "Profit": 20.0
    }
    create_record(new_row)

    # Example READ
    read_records(City="Test City")

    # Example UPDATE
    update_records("City", "Test City", "Sales", 150.0)

    # Example DELETE
    delete_records(City="Test City")
