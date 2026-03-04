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

import pyodbc

# List all ODBC drivers installed on the system
drivers = [driver for driver in pyodbc.drivers()]
print("ODBC Drivers available:")
for driver in drivers:
    print(driver)


from sqlalchemy import create_engine

# Define the connection string to your MS SQL Server
server = 'localhost'  
database = 'DE5_Module5'
username = 'python_app'
password = 'password'

# Create the connection string with Windows Authentication
connection_string = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'


# Create the SQLAlchemy engine
engine = create_engine(connection_string)

Customers.to_sql('customers_bronz', con=engine, if_exists='replace', index=False)
Books.to_sql('books_bonz', con=engine, if_exists='replace', index=False)
