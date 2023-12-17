import pandas as pd
from statsmodels.tsa.stattools import adfuller

btc_file_path = r'C:\Users\silas\OneDrive\Desktop\Bachlor Thesis\BTC-USD.csv'

# Laden Sie Ihre Zeitreihendaten
# Beispiel: data = pd.read_csv('path_to_your_data.csv')
# Load the data
btc_data = pd.read_csv(btc_file_path)
    
   
# Set the 'Date' column as the index of the DataFrame
btc_data['Date'] = pd.to_datetime(btc_data['Date'])
btc_data.set_index('Date', inplace=True)
print(btc_data.columns)


# Wählen Sie die 'Close'-Spalte für den ADF-Test
time_series = btc_data['Close']

# Durchführen des Augmented Dickey-Fuller Tests
adf_test = adfuller(time_series, autolag='AIC')

print('ADF Statistik: %f' % adf_test[0])
print('p-Wert: %f' % adf_test[1])
print('Kritische Werte:')
for key, value in adf_test[4].items():
    print('\t%s: %.3f' % (key, value))

# Interpretation
if adf_test[1] < 0.05:
    print("Die Zeitreihe ist stationär")
else:
    print("Die Zeitreihe ist nicht stationär")

# Einfache Differenzierung
btc_data['Close_diff'] = btc_data['Close'].diff()

# Entfernen Sie NaN-Werte, die durch Differenzierung entstehen können
btc_data.dropna(inplace=True)

# Erneuter ADF-Test mit der differenzierten Zeitreihe
adf_test_diff = adfuller(btc_data['Close_diff'], autolag='AIC')
print('ADF Statistik: %f' % adf_test[0])
print('p-Wert: %f' % adf_test[1])
print('Kritische Werte:')
for key, value in adf_test[4].items():
    print('\t%s: %.3f' % (key, value))

# Interpretation
if adf_test_diff[1] < 0.05:
    print("Die Zeitreihe ist stationär")
else:
    print("Die Zeitreihe ist nicht stationär")