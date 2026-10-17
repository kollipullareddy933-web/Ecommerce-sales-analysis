
# E-commerce Sales Analysis Dashboard

An interactive e-commerce sales analytics dashboard built using
Python, Pandas, Matplotlib, and Streamlit.

## Features
- Total revenue and sales KPIs
- Top 5 products ranked by revenue
- Monthly sales summary and growth
- Customer analysis and repeat-customer rate
- Category-wise and city-wise revenue
- Interactive date, category, and city filters
- Downloadable filtered sales data

## Technologies
Python, Pandas, NumPy, Matplotlib, Streamlit

## Project Structure
- app.py: Main Streamlit dashboard
- generate_data.py: Generates sample sales data
- requirements.txt: Python dependencies
- data/ecommerce_sales.csv: Generated dataset

## Run Locally

Install the dependencies:

    python -m pip install -r requirements.txt

Generate the dataset:

    python generate_data.py

Run the dashboard:

    python -m streamlit run app.py

## Dataset
The project uses simulated data generated for learning
and portfolio demonstration. It does not represent real
company transactions or actual customer information.

## Future Enhancements
- SQL database integration
- Profitability analysis
- Customer segmentation
- Integration with real retail datasets
