import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "Employee 1000x.csv"
DB_FILE  = BASE_DIR / "employee.db"


# load the csv into Df variable
df = pd.read_csv(CSV_FILE)

print("\nFirst few rows:\n")
print(df.head())
print(f"\nTotal records: {len(df)}")


# push it straight into sqlite database
conn = sqlite3.connect(DB_FILE)
df.to_sql("employees", conn, if_exists="replace", index=False)
print("\nCSV loaded into DB.")


# Confirming the data was fetched correctly
query = """
    SELECT `First Name`, `Last Name`, Email, Phone, `Job Title`
    FROM employees
    LIMIT 10
"""

preview = pd.read_sql(query, conn)
print("\nSample from DB:\n")
print(preview)

conn.close()
print("\nDone.")