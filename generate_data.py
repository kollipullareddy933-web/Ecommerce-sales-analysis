
import random
from pathlib import Path

import numpy as np
import pandas as pd

# Make the generated data reproducible
random.seed(42)
np.random.seed(42)

# Sample products and categories
products = {
    "Laptop": ("Electronics", 45000, 85000),
    "Headphones": ("Electronics", 800, 5000),
    "Mobile Phone": ("Electronics", 10000, 45000),
    "T-Shirt": ("Clothing", 300, 1200),
    "Jeans": ("Clothing", 800, 2500),
    "Shoes": ("Footwear", 1000, 5000),
    "Coffee Maker": ("Home", 1500, 6000),
    "Backpack": ("Accessories", 500, 3000),
    "Watch": ("Accessories", 1000, 10000),
    "Water Bottle": ("Home", 200, 1000),
}

cities = ["Hyderabad", "Bengaluru", "Chennai",
          "Mumbai", "Delhi", "Pune"]

rows = []

for i in range(1, 1001):
    product = random.choice(list(products.keys()))
    category, min_price, max_price = products[product]

    price = round(random.uniform(min_price, max_price), 2)
    quantity = random.randint(1, 5)
    discount = random.choice([0, 0.05, 0.10, 0.15])

    order_date = pd.Timestamp("2025-01-01") + pd.Timedelta(
        days=random.randint(0, 364)
    )

    rows.append({
        "Order_ID": f"ORD{i:05d}",
        "Order_Date": order_date,
        "Customer_ID": f"CUST{random.randint(1, 350):04d}",
        "City": random.choice(cities),
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "Unit_Price": price,
        "Discount": discount,
    })

df = pd.DataFrame(rows)

# Calculate sales after discount
df["Revenue"] = (
    df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"])
).round(2)

# Save the dataset inside the data folder
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

output_file = data_dir / "ecommerce_sales.csv"
df.to_csv(output_file, index=False)

print("Dataset created successfully!")
print("File:", output_file)
print("Rows and columns:", df.shape)
print(df.head())
