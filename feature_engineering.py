import pandas as pd
# Die create_lag_features-Funktion ist für die Vorverarbeitung von Zeitreihendaten konzipiert. 
# Sie nimmt den Pfad zu einer CSV-Datei mit Bitcoin-Handelsdaten, lädt diese in einen DataFrame und konvertiert die 'Date'-Spalte in das datetime-Format, um sie als Index zu setzen. 
# Die Funktion erzeugt dann drei Lag-Features, die den Bitcoin-Schlusspreis von 1 Tag, 7 Tagen und 30 Tagen zuvor darstellen. 
# Nach der Erstellung der Lag-Features werden Zeilen mit fehlenden Werten entfernt, um die Daten für maschinelles Lernen vorzubereiten. 
# Das Ergebnis ist ein bereinigter DataFrame, der zur Modellierung verwendet werden kann.

from features_config import FEATURES_CONFIG

def create_features(btc_data, features_config):
    
    # Erstellung der Lag-Features
    for feature_name, lag in features_config['lag_features'].items():
        btc_data[feature_name] = btc_data['Close'].shift(lag)
    
    # Erstellung der SMA-Features
    for feature_name, window in features_config['sma_features'].items():
        btc_data[feature_name] = btc_data['Close'].rolling(window=window).mean()
    
    # Hier weiter Features mit Config Datei erstellen
    return btc_data
