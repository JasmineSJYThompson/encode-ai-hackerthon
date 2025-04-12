from utils.analyzer import TokenSwapAnalyzer

analyzer = TokenSwapAnalyzer()

report = analyzer.compare_tokens('bitcoin', 'ethereum')  # BTC → ETH
print(report)
