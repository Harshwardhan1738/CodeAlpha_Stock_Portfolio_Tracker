import requests
from prettytable import PrettyTable

# Replace 'YOUR_API_KEY' with your actual API key from a stock data provider (e.g., Alpha Vantage)
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://www.alphavantage.co/query"

portfolio = {}

def fetch_stock_price(symbol):
    """Fetch real-time stock price for a given symbol."""
    try:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "1min",
            "apikey": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        latest_time = list(data["Time Series (1min)"].keys())[0]
        return float(data["Time Series (1min)"][latest_time]["1. open"])
    except KeyError:
        print(f"Error: Unable to fetch data for {symbol}. Check the stock symbol or API key.")
        return None

def add_stock(symbol, quantity):
    """Add stock to the portfolio."""
    price = fetch_stock_price(symbol)
    if price:
        portfolio[symbol] = portfolio.get(symbol, {"quantity": 0, "price": 0})
        portfolio[symbol]["quantity"] += quantity
        portfolio[symbol]["price"] = price
        print(f"Added {quantity} shares of {symbol} at ${price:.2f} each.")

def remove_stock(symbol):
    """Remove stock from the portfolio."""
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Removed {symbol} from your portfolio.")
    else:
        print(f"Error: {symbol} is not in your portfolio.")

def view_portfolio():
    """Display the current portfolio."""
    if not portfolio:
        print("Your portfolio is empty.")
        return

    table = PrettyTable(["Stock", "Quantity", "Current Price", "Total Value ($)"])
    total_value = 0

    for symbol, info in portfolio.items():
        current_price = fetch_stock_price(symbol)
        if current_price:
            total = current_price * info["quantity"]
            total_value += total
            table.add_row([symbol, info["quantity"], f"${current_price:.2f}", f"${total:.2f}"])

    print(table)
    print(f"Total Portfolio Value: ${total_value:.2f}")

def main():
    """Main function to interact with the portfolio tool."""
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            symbol = input("Enter stock symbol: ").upper()
            try:
                quantity = int(input("Enter quantity: "))
                add_stock(symbol, quantity)
            except ValueError:
                print("Invalid quantity. Please enter a number.")
        elif choice == "2":
            symbol = input("Enter stock symbol to remove: ").upper()
            remove_stock(symbol)
        elif choice == "3":
            view_portfolio()
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
