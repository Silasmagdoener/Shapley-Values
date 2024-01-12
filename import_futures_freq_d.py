import pandas as pd
import zipfile
from io import StringIO
from pathlib import Path

# Pfad zum Verzeichnis mit den ZIP-Dateien in täglicher Frequenz
directory_path = Path(r'c:\Users\silas\Downloads\binance-public-data-master\binance-public-data-master\python\data\futures\um\monthly\indexPriceKlines\BTCUSDT\1d')

# Liste für die DataFrame-Akkumulation
dataframes = []

# Alle ZIP-Dateien im Verzeichnis durchlaufen
for file_path in directory_path.glob('*.zip'):
    with zipfile.ZipFile(file_path, 'r') as z:
        contained_file_name = z.namelist()[0]
        with z.open(contained_file_name) as csvfile:
            csv_content = StringIO(csvfile.read().decode('utf-8'))
            df = pd.read_csv(csv_content, header=None, sep=',')
            # Überprüfen, ob die erste Zeile ein String und die Kopfzeile ist
            if isinstance(df.iloc[0, 0], str) and df.iloc[0, 0].strip().lower() == 'open_time':
                df = df.iloc[1:]
            df[0] = pd.to_datetime(df[0], unit='ms')
            dataframes.append(df)

# Alle DataFrames zu einem DataFrame kombinieren
combined_df = pd.concat(dataframes, ignore_index=True)

# Spaltennamen hinzufügen
combined_df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Value1', 
                       'EndTimestamp', 'Value2', 'Volume', 'Value3', 
                       'Value4', 'Value5']

# DataFrame nach dem Zeitstempel sortieren
combined_df.sort_values('Timestamp', inplace=True)


# Speichern des DataFrames als CSV-Datei
csv_output_path = r'C:\Users\silas\OneDrive\Desktop\Bachelor Thesis\Model tests und Code\aggregated_futures_data_freq_d.csv'
combined_df.to_csv(csv_output_path, index=False)

print(f"DataFrame wurde als CSV unter {csv_output_path} gespeichert.")
