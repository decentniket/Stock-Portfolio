# Stock-Portfolio
import requests

class StockPortfolio:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}

    def fetch_stock_data(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={self.api_key}'
        response = requests.get(url)
        data = response.json()
        if "Time Series (5min)" in data:
            latest_time = sorted(data["Time Series (5min)"].keys())[0]
            latest_data = data["Time Series (5min)"][latest_time]
            return float(latest_data["1. open"]), float(latest_data["4. close"])
        else:
            print(f"Error fetching data for {symbol}: {data.get('Error Message', 'Unknown error')}")
            return None, None

    def add_stock(self, symbol, shares):
        if symbol in self.portfolio:
            self.portfolio[symbol]['shares'] += shares
        else:
            self.portfolio[symbol] = {'shares': shares, 'initial_price': self.fetch_stock_data(symbol)[0]}
        print(f"Added {shares} shares of {symbol} to your portfolio.")

    def remove_stock(self, symbol, shares):
        if symbol in self.portfolio:
            if self.portfolio[symbol]['shares'] >= shares:
                self.portfolio[symbol]['shares'] -= shares
                if self.portfolio[symbol]['shares'] == 0:
                    del self.portfolio[symbol]
                print(f"Removed {shares} shares of {symbol} from your portfolio.")
            else:
                print(f"You do not have enough shares of {symbol} to remove.")
        else:
            print(f"{symbol} is not in your portfolio.")

    def track_performance(self):
        total_investment = 0
        current_value = 0
        for symbol, info in self.portfolio.items():
            shares = info['shares']
            initial_price = info['initial_price']
            current_price, _ = self.fetch_stock_data(symbol)
            if current_price is not None:
                total_investment += shares * initial_price
                current_value += shares * current_price
                print(f"{symbol}: {shares} shares, Initial Price: ${initial_price:.2f}, Current Price: ${current_price:.2f}")
            else:
                print(f"Could not fetch current price for {symbol}.")
        
        print(f"\nTotal Investment: ${total_investment:.2f}")
        print(f"Current Value: ${current_value:.2f}")
        print(f"Profit/Loss: ${current_value - total_investment:.2f}")

def main():
    api_key = 'YOUR_API_KEY'  # Replace with your Alpha Vantage API key
    portfolio = StockPortfolio(api_key)

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Performance")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(symbol, shares)
        elif choice == '3':
            portfolio.track_performance()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
