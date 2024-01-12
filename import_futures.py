import pandas as pd
import zipfile
from io import StringIO
from pathlib import Path

# Pfad zum Verzeichnis mit den ZIP-Dateien
directory_path = Path(r'c:\Users\silas\Downloads\binance-public-data-master\binance-public-data-master\python\data\futures\um\monthly\indexPriceKlines\BTCUSDT\1mo')

# Liste für die DataFrame-Akkumulation
dataframes = []

# Alle ZIP-Dateien im Verzeichnis durchlaufen
for file_path in directory_path.glob('*.zip'):
    with zipfile.ZipFile(file_path, 'r') as z:
        # Name der enthaltenen CSV-Datei extrahieren
        contained_file_name = z.namelist()[0]
        with z.open(contained_file_name) as csvfile:
            # CSV-Daten in StringIO umwandeln, um sie mit pandas zu lesen
            csv_content = StringIO(csvfile.read().decode('utf-8'))
            # DataFrame erstellen, annehmen, dass das Trennzeichen ein Komma ist
            df = pd.read_csv(csv_content, header=None, sep=',')
            # Überprüfen, ob die erste Zeile die Kopfzeile ist
            if df.iloc[0, 0] == 'open_time':
                df = df.iloc[1:]  # Entfernen der Kopfzeile
            # Konvertieren der Unix-Zeitstempel in lesbare Datumsformate
            df[0] = pd.to_datetime(df[0], unit='ms')
            # DataFrame der Liste hinzufügen
            dataframes.append(df)

# Alle DataFrames zu einem DataFrame kombinieren
combined_df = pd.concat(dataframes, ignore_index=True)

# Spaltennamen hinzufügen
combined_df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Value1', 
                       'EndTimestamp', 'Value2', 'Volume', 'Value3', 
                       'Value4', 'Value5']

# DataFrame nach dem Zeitstempel sortieren
combined_df.sort_values('Timestamp', inplace=True)

# Ausgabe des kombinierten und sortierten DataFrames
print(combined_df)

# Speichern des DataFrames als CSV-Datei
csv_output_path = r'C:\Users\silas\OneDrive\Desktop\Bachelor Thesis\Model tests und Code\aggregated_futures_data.csv'  # Pfad, unter dem die CSV-Datei gespeichert werden soll
combined_df.to_csv(csv_output_path, index=False)  # Setzen Sie `index=False`, wenn Sie nicht möchten, dass der Index mitgespeichert wird

print(f"DataFrame wurde als CSV unter {csv_output_path} gespeichert.")