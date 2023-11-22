# Konfiguration der zu erstellenden Features
FEATURES_CONFIG = {
    'lag_features': {
        'price_lag1': 1,
        'price_lag7': 7,
        'price_lag30': 30,
        # Fügen Sie hier weitere Lag-Features hinzu
    },
    # Hier können Sie weitere Arten von Features hinzufügen
    'sma_features': {
        'sma_3': 3,
        'sma_7': 7,
        'sma_30': 30
    },
}