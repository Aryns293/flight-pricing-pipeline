import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_flight_data(num_records=5000):
    print(f"Generating {num_records} mock flight records...")
    
    airlines = {
        'Vistara': 1.5,      # Premium
        'Air India': 1.2,    # Standard
        'Indigo': 1.0,       # Budget
        'SpiceJet': 0.9,     # Budget
        'GoFirst': 0.8,      # Budget
        'AirAsia': 0.85      # Budget
    }
    
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai']
    
    data = []
    base_date = datetime.now()
    
    for _ in range(num_records):
        airline = random.choice(list(airlines.keys()))
        multiplier = airlines[airline]
        
        # Pick source and destination (ensure they are different)
        source, dest = random.sample(cities, 2)
        
        # Days left to departure
        days_left = random.randint(1, 49)
        
        # Base price between 3000 and 6000 INR
        base_price = random.randint(3000, 6000)
        
        # Price increases as days_left decreases (linear trend + random noise)
        urgency_premium = (50 - days_left) * 100
        
        noise = random.randint(-500, 500)
        
        final_price = int((base_price + urgency_premium) * multiplier + noise)
        final_price = max(2000, final_price) 
        
        flight_date = base_date + timedelta(days=days_left)
        
        # Randomly introduce a few nulls to simulate real-world messy data
        if random.random() < 0.02:
            final_price = None
        
        data.append({
            'flight_date': flight_date.strftime('%Y-%m-%d'),
            'airline': airline,
            'source': source,
            'destination': dest,
            'days_left': days_left,
            'price': final_price
        })
        
    df = pd.DataFrame(data)
    output_file = 'raw_flights.csv'
    df.to_csv(output_file, index=False)
    print(f"Successfully generated {output_file}!")

if __name__ == "__main__":
    generate_flight_data()
