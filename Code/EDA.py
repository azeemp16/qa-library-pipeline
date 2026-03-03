# %%
import pandas as pd

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
Books.head(50)

from datetime import datetime

def calculate_days_on_loan(df, checkout_col="Book checkout", returned_col="Book Returned", dayfirst=True):

    df[checkout_col] = pd.to_datetime(df[checkout_col], dayfirst=dayfirst, errors="coerce")
    df[returned_col] = pd.to_datetime(df[returned_col], dayfirst=dayfirst, errors="coerce")
    
    return (df[returned_col] - df[checkout_col]).dt.days.astype("Int64")
Books["Days on loan"] = calculate_days_on_loan(Books)

print(Books.head())


