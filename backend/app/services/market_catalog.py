from app.domain.market import MarketGroup, MarketInstrument

# Seed catalogue only: symbols are identifiers, not live prices or recommendations.
INSTRUMENTS = [
    MarketInstrument(symbol="EURUSD", display_name="EUR/USD", group=MarketGroup.FOREX, quote_currency="USD"),
    MarketInstrument(symbol="GBPUSD", display_name="GBP/USD", group=MarketGroup.FOREX, quote_currency="USD"),
    MarketInstrument(symbol="USDJPY", display_name="USD/JPY", group=MarketGroup.FOREX, quote_currency="JPY"),
    MarketInstrument(symbol="AUDUSD", display_name="AUD/USD", group=MarketGroup.FOREX, quote_currency="USD"),
    MarketInstrument(symbol="BTCUSD", display_name="Bitcoin / USD", group=MarketGroup.CRYPTO, quote_currency="USD"),
    MarketInstrument(symbol="ETHUSD", display_name="Ether / USD", group=MarketGroup.CRYPTO, quote_currency="USD"),
    MarketInstrument(symbol="SOLUSD", display_name="Solana / USD", group=MarketGroup.CRYPTO, quote_currency="USD"),
    MarketInstrument(symbol="XRPUSD", display_name="XRP / USD", group=MarketGroup.CRYPTO, quote_currency="USD"),
    MarketInstrument(symbol="XAUUSD", display_name="Gold / USD", group=MarketGroup.COMMODITIES, quote_currency="USD"),
    MarketInstrument(symbol="XAGUSD", display_name="Silver / USD", group=MarketGroup.COMMODITIES, quote_currency="USD"),
    MarketInstrument(symbol="VIX", display_name="CBOE Volatility Index", group=MarketGroup.VOLATILITY),
    MarketInstrument(symbol="DERIV_VOL10", display_name="Deriv Volatility 10", group=MarketGroup.DERIV_SYNTHETIC, provider="deriv"),
    MarketInstrument(symbol="DERIV_VOL25", display_name="Deriv Volatility 25", group=MarketGroup.DERIV_SYNTHETIC, provider="deriv"),
    MarketInstrument(symbol="DERIV_VOL50", display_name="Deriv Volatility 50", group=MarketGroup.DERIV_SYNTHETIC, provider="deriv"),
    MarketInstrument(symbol="DERIV_VOL75", display_name="Deriv Volatility 75", group=MarketGroup.DERIV_SYNTHETIC, provider="deriv"),
    MarketInstrument(symbol="DERIV_VOL100", display_name="Deriv Volatility 100", group=MarketGroup.DERIV_SYNTHETIC, provider="deriv"),
]
