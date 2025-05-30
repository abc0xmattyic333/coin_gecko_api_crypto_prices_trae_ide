import requests
import json
from datetime import datetime
import csv

def get_crypto_prices():
    # CoinGecko API endpoint for getting prices
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    # List of cryptocurrencies to fetch (can be modified)
    cryptocurrencies = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana"]
    
    # Parameters for the API request
    params = {
        "ids": ",".join(cryptocurrencies),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    
    try:
        # Make API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse response
        data = response.json()
        
        # Get current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Print results
        print(f"\nCryptocurrency Prices ({current_time})")
        print("-" * 50)
        
        # Prepare data for CSV
        csv_data = []
        
        for crypto in cryptocurrencies:
            if crypto in data:
                price = data[crypto]["usd"]
                change_24h = data[crypto].get("usd_24h_change", 0)
                print(f"{crypto.capitalize()}:")
                print(f"  Price: ${price:,.2f}")
                print(f"  24h Change: {change_24h:.2f}%\n")
                
                # Add data to CSV list
                csv_data.append({
                    'timestamp': current_time,
                    'cryptocurrency': crypto,
                    'price_usd': price,
                    '24h_change': change_24h
                })
            else:
                print(f"Could not fetch data for {crypto}")
        
        # Save to CSV
        csv_file = 'crypto_prices.csv'
        file_exists = False
        try:
            with open(csv_file, 'r') as f:
                file_exists = True
        except FileNotFoundError:
            pass
            
        with open(csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'cryptocurrency', 'price_usd', '24h_change'])
            if not file_exists:
                writer.writeheader()
            writer.writerows(csv_data)
            
        print(f"\nData has been saved to {csv_file}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except json.JSONDecodeError:
        print("Error parsing response from CoinGecko")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    get_crypto_prices()