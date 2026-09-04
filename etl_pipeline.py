import pandas as pd
import sqlite3
import os

def run_etl():
    print("Starting ETL Pipeline...")
    
    # --- 1. EXTRACT ---
    csv_file = 'raw_flights.csv'
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Run data_generator.py first.")
        return
        
    print("Extracting data...")
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} rows.")
    
    # --- 2. TRANSFORM ---
    print("Transforming data...")
    
    # 2a. Handle Missing Values (Null prices)
    # We will fill missing prices with the median price for that specific airline
    df['price'] = df.groupby('airline')['price'].transform(lambda x: x.fillna(x.median()))
    
    # 2b. Data type conversions
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    df['price'] = df['price'].astype(int)
    
    # 2c. Feature Engineering (Optional for basic pipelines)
    # Let's extract the month and day of week from the flight date
    df['month'] = df['flight_date'].dt.month
    df['day_of_week'] = df['flight_date'].dt.day_name()
    
    print("Transformation complete. Cleaned sample:")
    print(df.head())
    
    # --- 3. LOAD ---
    print("Loading data into SQLite database...")
    db_file = 'flights.db'
    conn = sqlite3.connect(db_file)
    
    # Save the dataframe to a SQL table called 'cleaned_flights'
    # if_exists='replace' will overwrite the table if it exists
    df.to_sql('cleaned_flights', conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"ETL Complete! Data saved to {db_file}")

if __name__ == "__main__":
    run_etl()
