#..............................ADDITIONAL PROGRAM.............................

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

print("Welcome To The Additional Program")
input("\nPress Enter To Start:")

#..............................PROGRAM STARTS.................................

# Load credentials from .env
load_dotenv()
HOST = os.getenv("MYSQL_HOST")
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")

if not all([HOST, USER, PASSWORD]):
    raise ValueError("❌ Missing MySQL credentials in .env file")

# Create engine (connects to MySQL server first, not a specific DB)
engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}")

# Create databases
with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS enterprise_sales;"))
    conn.execute(text("CREATE DATABASE IF NOT EXISTS module_add;"))

# Reconnect directly to module_add
engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/module_add")

# Insert defaults
with engine.connect() as conn:
    products = [
        "Air Conditioners","Cameras","Computers","Coolers","Gaming Consoles",
        "Headsets","Microwave Ovens","Mobile Phones","Tablets","Refrigerators",
        "Smart Watches","Speakers","Televisions","Washing Machines","Other Accessories"
    ]
    pd.DataFrame(products, columns=["Products"]).to_sql("products_list", conn, index=False, if_exists="replace")
    pd.DataFrame(["GGIA"], columns=["Password"]).to_sql("module_password", conn, index=False, if_exists="replace")

print("\n✅ Setup Completed Successfully")

input("\nPress Enter To Continue:")

print("\nIn The Main Module:-\nIf your response is YES, type 1\nIf your response is NO, type 0")
print("\nThank You")

#....................XXX...XXX...XXX...XXX...XXX....................
