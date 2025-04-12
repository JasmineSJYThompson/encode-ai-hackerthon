from utils.converter import DeFiConverter

def test_conversions(converter: DeFiConverter):
    # Test fiat-to-crypto conversion: USD to BTC
    amount_usd = 100
    btc_amount = converter.convert_currency(amount_usd, "usd", "btc")
    print(f"USD to BTC Conversion:\n  {amount_usd} USD -> {btc_amount:.8f} BTC\n")
    
    # Test crypto-to-fiat conversion: ETH to USD
    amount_eth = 1
    usd_amount = converter.convert_currency(amount_eth, "eth", "usd")
    print(f"ETH to USD Conversion:\n  {amount_eth} ETH -> {usd_amount:.2f} USD\n")
    
    # Test crypto-to-crypto conversion: ETH to BTC
    amount_eth = 1
    btc_from_eth = converter.convert_currency(amount_eth, "eth", "btc")
    print(f"ETH to BTC Conversion:\n  {amount_eth} ETH -> {btc_from_eth:.8f} BTC\n")

def test_historical_data(converter: DeFiConverter):
    # Optionally, test and plot historical conversion rate data.
    print("Plotting historical conversion rate for BTC to USD...")
    converter.plot_history("btc", "usd", days=1)

def main():
    converter = DeFiConverter()
    
    print("=== Testing Currency Conversions ===\n")
    test_conversions(converter)
    
    print("=== Testing Historical Data Plotting ===\n")
    test_historical_data(converter)

if __name__ == "__main__":
    main()
