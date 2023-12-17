# Konfiguration der zu erstellenden Features
FEATURES_CONFIG = {
    'lag_features': {
        'price_lag1': 1,
        'price_lag7': 7,
        'price_lag30': 30,
        # Hier weitere Lag-Features hinzufügen
    },
    # Hier weitere Arten von Features hinzufügen
    'sma_features': {
        'sma_3': 3,
        'sma_7': 7,
        'sma_30': 30
    },
    'volatility_features': {
        'volatility_3': 3,    # 3-Tage Volatilität
        'volatility_7': 7,    # 7-Tage Volatilität
        'volatility_30': 30   # 30-Tage Volatilität
    },
    # 'rsi': {
    #     'window': 14
    # },
    # 'macd': {
    #     'span1': 12,
    #     'span2': 26,
    #     'span3': 9
    # },
    # 'bollinger': {
    #     'window': 20
    # },
    # 'rolling_max_min': {
    #     'window': 7
    # },
    # 'rolling_avg_volume': {
    #     'window': 7
    # },
    # 'fft_components': {
    #     'component1': 0,
    #     'component2': 1
    # },

}