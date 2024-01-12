import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime

# Funktion, um ein Datum in einen Unix-Timestamp umzuwandeln
def to_unix_timestamp(date_str):
    """
    Konvertiert ein Datum im Format 'YYYY-MM-DD' in einen Unix-Timestamp.
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(time.mktime(dt.timetuple()))

def validate_data(data):
    """
    Validates the input data to ensure it contains the required columns and no missing values.
    
    :param data: DataFrame containing the data to validate.
    :raises ValueError: If expected columns are missing or if there are missing values in the data.
    """
    # Define the expected columns
    expected_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    
    # Check for missing columns
    if not all(column in data.columns for column in expected_columns):
        missing_columns = set(expected_columns) - set(data.columns)
        raise ValueError(f"Missing columns in the data: {missing_columns}")

    # Check for missing values
    if data.isnull().any().any():
        raise ValueError("Data contains missing values. Please handle these before proceeding.")
    
def calculate_returns(df, frequency='D'):
    """
    Berechnet diskrete (nicht addierbare) Renditen für den 'Close'-Preis in einem DataFrame mit variabler Frequenz.
    
    :param df: DataFrame, der die 'Close'-Preise enthält.
    :param frequency: String, der die Frequenz der Renditeberechnung angibt.
                      Akzeptiert 'D' für täglich, 'W' für wöchentlich, 'M' für monatlich.
    :return: Eine Serie von Renditen für die gegebene Frequenz.

    Beispiel der Funktionsanwendung:
    Ersetzen Sie 'example_df' mit Ihrem DataFrame, der die BTC-Daten enthält.
    daily_returns = calculate_returns(example_df, frequency='D')
    weekly_returns = calculate_returns(example_df, frequency='W')
    monthly_returns = calculate_returns(example_df, frequency='M')
    """
    # Resampling des DataFrames für die gegebene Frequenz und Forward-Filling der fehlenden Werte
    resampled_df = df['Close'].resample(frequency).ffill()
    # Berechnung der prozentualen Änderung der 'Close'-Preise
    returns = resampled_df.pct_change().dropna()
    return returns

def calculate_log_returns(df, frequency='D'):
    """
    Berechnet stetige (logarithmierte) Renditen für den 'Close'-Preis in einem DataFrame mit variabler Frequenz.
    
    :param df: DataFrame, der die 'Close'-Preise enthält.
    :param frequency: String, der die Frequenz der Renditeberechnung angibt.
                      Akzeptiert 'D' für täglich, 'W' für wöchentlich, 'M' für monatlich.
    :return: Eine Serie von stetigen Renditen für die gegebene Frequenz.
    """
    resampled_df = df['Close'].resample(frequency).ffill()
    log_returns = np.log(resampled_df / resampled_df.shift(1)).dropna()
    return log_returns

def plot_returns(returns, title, color):
    """
    Zeichnet ein Diagramm der berechneten Renditen.
    """
    plt.figure(figsize=(14, 4))
    plt.plot(returns, label=f'{title} Renditen', color=color)
    plt.title(f'{title} Renditen von BTC')
    plt.xlabel('Datum')
    plt.ylabel('Rendite')
    plt.legend()
    plt.show()