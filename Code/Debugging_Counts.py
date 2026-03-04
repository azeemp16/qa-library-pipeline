# %%
# For Python 3
import pyodbc as py
import pandas as pd
import sqlalchemy as sq
import unittest
##pip install pandas 

# %%
import os
os.chdir(r"C:\Users\Admin\qa-library-pipeline\data")


# %%
Books = pd.read_csv(r"03_Library Systembook.csv")
Customers = pd.read_csv(r"03_Library SystemCustomers.csv")


# %%
Customers = Customers[Customers["Customer ID"].notna()]
Customers["Customer ID"] = (
    pd.to_numeric(Customers["Customer ID"], errors="coerce")
    .astype("Int64")
)
Customers["Customer Name"] = Customers["Customer Name"].replace( ["NaN", "nan", ""], pd.NA ) 
Customers["Customer Name"] = Customers["Customer Name"].fillna("NA")
Customers.head()

# %%
Books[["Customer ID", "Id"]] = Books[["Customer ID", "Id"]].apply(
    lambda col: pd.to_numeric(col, errors="coerce").astype("Int64")
)
Books["Book checkout"] = pd.to_datetime(
    Books["Book checkout"].str.replace('"', '', regex=False),
    dayfirst=True,
    errors="coerce"
)
Books["Book checkout"] = Books["Book checkout"].dt.strftime("%d/%m/%Y")

Books["Days allowed to borrow"] = (
    Books["Days allowed to borrow"]
    .str.extract(r"(\d+)")      
    .astype("Int64")              
    * 7                           
)
Books = Books[Books["Books"].notna()]


Books.head()

# %%
Customers.head(50)

# %%

books_before = pd.read_csv(r"03_Library Systembook.csv")
books_after = Books  

books_cleaned_count = len(books_before) - len(books_after)
print("Rows cleaned in Books:", books_cleaned_count)
invalid_returns = Books[Books["Book Returned"] < Books["Book checkout"]]

invalid_count = len(invalid_returns)

print("Number of records where Book Returned is before Book Checkout:", invalid_count)
print(invalid_returns)

import pandas as pd

summary_df = pd.DataFrame({
    "Metric": ["Rows cleaned in Books", "Invalid return records"],
    "Value": [books_cleaned_count, invalid_count]
})


summary_df.to_csv("library_cleaning_summary.csv", index=False)


invalid_returns.to_csv("invalid_book_returns.csv", index=False)

print("CSV files created:")
print(" - library_cleaning_summary.csv")
print(" - invalid_book_returns.csv")
