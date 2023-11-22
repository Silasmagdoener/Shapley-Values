import pandas as pd
# Die create_lag_features-Funktion ist für die Vorverarbeitung von Zeitreihendaten konzipiert. 
# Sie nimmt den Pfad zu einer CSV-Datei mit Bitcoin-Handelsdaten, lädt diese in einen DataFrame und konvertiert die 'Date'-Spalte in das datetime-Format, um sie als Index zu setzen. 
# Die Funktion erzeugt dann drei Lag-Features, die den Bitcoin-Schlusspreis von 1 Tag, 7 Tagen und 30 Tagen zuvor darstellen. 
# Nach der Erstellung der Lag-Features werden Zeilen mit fehlenden Werten entfernt, um die Daten für maschinelles Lernen vorzubereiten. 
# Das Ergebnis ist ein bereinigter DataFrame, der zur Modellierung verwendet werden kann.
def create_lag_features(btc_data):
    # Erstellen von Lag-Features
    btc_data['price_lag1'] = btc_data['Close'].shift(1)
    btc_data['price_lag7'] = btc_data['Close'].shift(7)
    btc_data['price_lag30'] = btc_data['Close'].shift(30)

    return btc_data
