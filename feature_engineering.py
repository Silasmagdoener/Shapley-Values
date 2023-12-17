
# Die create_lag_features-Funktion ist für die Vorverarbeitung von Zeitreihendaten konzipiert. 
# Sie nimmt den Pfad zu einer CSV-Datei mit Bitcoin-Handelsdaten, lädt diese in einen DataFrame und konvertiert die 'Date'-Spalte in das datetime-Format, um sie als Index zu setzen. 
# Die Funktion erzeugt dann drei Lag-Features, die den Bitcoin-Schlusspreis von 1 Tag, 7 Tagen und 30 Tagen zuvor darstellen. 
# Nach der Erstellung der Lag-Features werden Zeilen mit fehlenden Werten entfernt, um die Daten für maschinelles Lernen vorzubereiten. 
# Das Ergebnis ist ein bereinigter DataFrame, der zur Modellierung verwendet werden kann.



# def create_features(data, features_config):
#     # Erstellung der Lag-Features
#     for feature_name, lag in features_config['lag_features'].items():
#         data[feature_name] = data['Close'].shift(lag)
    
#     # Erstellung der SMA-Features
#     for feature_name, window in features_config['sma_features'].items():
#         data[feature_name] = data['Close'].rolling(window=window).mean()
    
#     # Hier weiter Features mit Config Datei erstellen
#     return data
import numpy as np
import pandas as pd
from scipy.fft import fft
from statsmodels.tsa.arima.model import ARIMA
from features_config import FEATURES_CONFIG



# def calculate_rsi(data, window):
#     delta = data['Close'].diff()
#     gain = (delta.clip(lower=0)).fillna(0)
#     loss = (-delta.clip(upper=0)).fillna(0)

#     avg_gain = gain.rolling(window=window, min_periods=window).mean()
#     avg_loss = loss.rolling(window=window, min_periods=window).mean()

#     rs = avg_gain / avg_loss
#     rsi = 100 - (100 / (1 + rs))
#     return rsi

# def calculate_macd(data, span1, span2, span3):
#     exp1 = data['Close'].ewm(span=span1, adjust=False).mean()
#     exp2 = data['Close'].ewm(span=span2, adjust=False).mean()
#     macd = exp1 - exp2
#     signal = macd.ewm(span=span3, adjust=False).mean()
#     return macd, signal

# def calculate_bollinger_bands(data, window):
#     rolling_mean = data['Close'].rolling(window=window).mean()
#     rolling_std = data['Close'].rolling(window=window).std()
#     upper_band = rolling_mean + (rolling_std * 2)
#     lower_band = rolling_mean - (rolling_std * 2)
#     return upper_band, lower_band

def create_features(data, features_config):
    # Erstellen einer Kopie des DataFrames, um Warnungen zu vermeiden
    data_copy = data.copy()

    # Erstellung der Lag-Features
    for feature_name, lag in features_config['lag_features'].items():
        data_copy[feature_name] = data['Close'].shift(lag)
    
    # Erstellung der SMA-Features
    for feature_name, window in features_config['sma_features'].items():
        data_copy[feature_name] = data['Close'].rolling(window=window).mean()

    # Erstellung der Volatilitäts-Features
    for feature_name, window in features_config['volatility_features'].items():
        data_copy[feature_name] = data['Close'].rolling(window=window).std()

    # # RSI
    # rsi_window = FEATURES_CONFIG['rsi']['window']
    # data_copy['rsi'] = calculate_rsi(data_copy, window=rsi_window)
    
    # # MACD
    # macd_span1 = FEATURES_CONFIG['macd']['span1']
    # macd_span2 = FEATURES_CONFIG['macd']['span2']
    # macd_span3 = FEATURES_CONFIG['macd']['span3']
    # macd, signal = calculate_macd(data_copy, span1=macd_span1, span2=macd_span2, span3=macd_span3)
    # data_copy['macd'] = macd
    # data_copy['macd_signal'] = signal
    
    # # Bollinger Bands
    # bollinger_window = FEATURES_CONFIG['bollinger']['window']
    # upper_band, lower_band = calculate_bollinger_bands(data_copy, window=bollinger_window)
    # data_copy['bollinger_upper'] = upper_band
    # data_copy['bollinger_lower'] = lower_band

    # # Fourier Transformations for seasonality
    # fft_component1 = FEATURES_CONFIG['fft_components']['component1']
    # fft_component2 = FEATURES_CONFIG['fft_components']['component2']
    
    # # Fourier Transformationen
    # fft_result = fft(data_copy['Close'].to_numpy())
    # data_copy['fft_component_1_magnitude'] = np.abs(fft_result[fft_component1])
    # data_copy['fft_component_2_magnitude'] = np.abs(fft_result[fft_component2])
  
    # Hier weiter Features mit Config Datei erstellen
    # # Stellen Sie sicher, dass Sie alle NaN-Werte bereinigen, die durch die Feature-Berechnungen entstehen können
    # data_copy.replace([np.inf, -np.inf], np.nan, inplace=True)
    # data_copy.dropna(inplace=True)
    
    return data_copy