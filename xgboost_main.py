import pandas as pd
from pipeline import get_full_pipeline
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

# Pfad zur BTC-USD.csv Datei
btc_file_path = r'C:\Users\silas\OneDrive\Desktop\Bachlor Thesis\BTC-USD.csv'

# Laden der Daten
btc_data = pd.read_csv(btc_file_path)
btc_data['Date'] = pd.to_datetime(btc_data['Date'])
btc_data.set_index('Date', inplace=True)

# Erhalten der Pipeline
full_pipeline = get_full_pipeline()

# Vorverarbeitung der Daten
btc_data_preprocessed = full_pipeline.fit_transform(btc_data)



############MODEL TRAINING UND TEST############

# Features sind alle Spalten außer 'Close'
X = btc_data.drop('Close', axis=1)

# Zielvariable 'Close'
y = btc_data['Close']

# Aufteilung der Daten in Trainings- und Testsets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Initialisierung und Training des XGBoost-Modells
xgb_model = XGBRegressor(objective='reg:squarederror')
xgb_model.fit(X_train, y_train)

# Hier können Sie Ihr Modell bewerten, indem Sie es auf dem Testdatensatz anwenden
predictions = xgb_model.predict(X_test)

# Hier könnten Sie die Leistung Ihres Modells bewerten, z.B. mit MAE
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae:.2f}")

# Anzeigen der ersten Zeilen der Tabelle
#print(X.head())


print(btc_data.describe())