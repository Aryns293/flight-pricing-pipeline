from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression

app = FastAPI(title="Flight Pricing Analytics API")

def get_db_connection():
    conn = sqlite3.connect('flights.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flight Pricing API. Use /docs to see endpoints."}

@app.get("/api/analytics/airlines")
def get_airline_averages():
    """Returns the historical average price for each airline."""
    try:
        conn = get_db_connection()
        query = '''
            SELECT airline, ROUND(AVG(price), 2) as avg_price, COUNT(*) as total_flights
            FROM cleaned_flights
            GROUP BY airline
            ORDER BY avg_price ASC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/trend")
def get_price_trend(airline: str = None):
    """
    Uses Simple Linear Regression to calculate how much the price increases 
    per day as the departure date approaches.
    """
    try:
        conn = get_db_connection()
        
        # If an airline is provided, filter by it. Otherwise, use all data.
        if airline:
            query = "SELECT days_left, price FROM cleaned_flights WHERE airline = ?"
            df = pd.read_sql_query(query, conn, params=(airline,))
        else:
            query = "SELECT days_left, price FROM cleaned_flights"
            df = pd.read_sql_query(query, conn)
            
        conn.close()
        
        if len(df) < 10:
            return {"error": "Not enough data for this airline to calculate a trend."}
            
        # Machine Learning: Simple Linear Regression
        # We want to predict price based on days_left
        X = df[['days_left']] # Features (must be 2D array)
        y = df['price']       # Target
        
        model = LinearRegression()
        model.fit(X, y)
        
        # The coefficient tells us how much price changes per 1 unit of days_left
        # Since fewer days left usually means higher price, the coefficient should be negative.
        price_change_per_day = model.coef_[0]
        
        return {
            "airline_analyzed": airline if airline else "All Airlines",
            "data_points": len(df),
            # Invert the coefficient for human readability: 
            # "Price goes UP by X rupees for every day closer to departure"
            "price_increase_per_day_closer": round(abs(price_change_per_day), 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # To run this script directly: python api.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
