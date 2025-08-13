# CRUD Operations on Sales Dataset

## Objective
The purpose of this project is to perform **Create**, **Read**, **Update**, and **Delete** (CRUD) operations on a sales dataset stored in a CSV file.

We are using the **`us_supermarket.csv`** dataset to demonstrate how to manipulate sales records directly using Python and the Pandas library.

---

## Dataset
The dataset contains details of supermarket sales including:
- Order Details
- Customer Details
- Product Details
- Sales, Profit, and Discounts

File: `data/us_supermarket.csv`

---

## Features Implemented

### 1. Create
Insert new records into the dataset using a Python dictionary.
```python
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
```

### 2. Read
Retrieve records that match specific filter criteria.
```python
read_records(City="Test City")
```

### 3. Update
Modify existing records based on filter conditions.
```python
update_records("City", "Test City", "Sales", 150.0)
```

### 4. Delete
Remove specific records from the dataset.
```python
delete_records(City="Test City")
```

---

## Requirements
- Python 3.x
- Pandas

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## How to Run
1. Clone this repository or extract the ZIP file.
2. Navigate to the project directory:
```bash
cd crud_operations_on_sales_dataset
```
3. Run the CRUD script:
```bash
python crud_operations.py
```

---

## Output Example
```
    Record added.
     Changes saved to CSV.
     Row ID        Order ID  ... Sales Quantity
0    99999  CA-2023-999999  ... 100.0       5
    Updated 1 record(s).
    Deleted 1 record(s).
```

---

## Author
Prepared for **Assignment: CRUD Operations on Sales Dataset**
