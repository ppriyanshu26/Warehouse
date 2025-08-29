import sys
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from matplotlib.backends.backend_pdf import PdfPages

# ------------------ Helpers ------------------

def ask_yes_no(msg):
    while True:
        ans = input(f"{msg} (1=Yes, 0=No): ")
        if ans in ("0", "1"):
            return ans == "1"
        print("ERROR: Only 1 or 0 allowed.")

def get_positive_int(msg):
    while True:
        try:
            val = int(input(msg))
            if val >= 0:
                return val
        except ValueError:
            pass
        print("ERROR: Enter a positive integer.")

# ------------------ DB Setup ------------------

def connect_db(host, user, password, db=None):
    url = f"mysql+pymysql://{user}:{password}@{host}/{db or ''}"
    return create_engine(url).connect()

# ------------------ Data Entry ------------------

def enter_record(products, action="buy"):
    data = {"Brands": [], "Items": [], "Revenue": []}

    for p in products:
        print(f"\nData for {p}")
        brands = get_positive_int(f"How many brands {action} of {p}?: ")

        items, revenue = 0, 0
        for i in range(brands):
            print(f"Brand {i+1}")
            price = get_positive_int(f"Enter {action} price: ")
            qty = get_positive_int("Enter quantity: ")
            items += qty
            revenue += price * qty

        data["Brands"].append(brands)
        data["Items"].append(items)
        data["Revenue"].append(revenue)

    return pd.DataFrame(data, index=products)

# ------------------ Reports ------------------

def final_report(buying, selling):
    table = pd.concat([selling, buying], axis=1)
    table.columns = ["Brands Sold", "Products Sold", "Sell.Rev.",
                     "Brands Bought", "Products Bought", "Buy.Rev."]
    table["Net"] = table["Sell.Rev."] - table["Buy.Rev."]
    table.loc["All Products"] = table.sum(numeric_only=True)
    return table

import matplotlib.pyplot as plt

def save_graph(table, filename):
    df = table.drop("All Products", errors="ignore")[["Sell.Rev.", "Buy.Rev.", "Net"]]
    ax = df.plot(kind="bar", figsize=(10,6))
    ax.set_ylabel("Revenue")
    ax.set_title("Sales Overview")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print("Graph saved to", filename)


# ------------------ Main ------------------

def main():
    creds = pd.read_csv("Entry Data.csv")
    host, user, pwd = creds.Data[:3]
    conn1 = connect_db(host, user, pwd, "module_add")
    conn2 = connect_db(host, user, pwd, "enterprise_sales")

    # Load products
    products = pd.read_sql("select * from products_list;", conn1)["Products"].to_list()

    # Enter buy/sell records
    buying = enter_record(products, "buy")
    selling = enter_record(products, "sell")

    # Combine into final table
    report = final_report(buying, selling)
    print(report)

    # Save
    report.to_sql("sales_record", conn2, if_exists="replace", index=True)
    save_graph(report, "Sales_Report.pdf")

if __name__ == "__main__":
    main()
