from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer, make_column_selector
from feature_engineering import create_features
from features_config import FEATURES_CONFIG

def get_numerical_preprocessing_pipeline():
    # Definieren Sie die Schritte für die Preprocessing-Pipeline
    numerical_transformers = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),  # Fehlende Werte mit dem Durchschnitt ersetzen
        ('scaler', StandardScaler()),  # Daten skalieren
    ])
    
    # Erstellen der Preprocessing-Pipeline nur für numerische Spalten
    preprocessing_pipeline = ColumnTransformer(transformers=[
        ('num', numerical_transformers, make_column_selector(dtype_include='number')),  # Verwendung von make_column_selector
    ])
    
    return preprocessing_pipeline


def get_full_pipeline():
    # Holen Sie die Preprocessing-Pipeline für numerische Daten
    numerical_preprocessing_pipeline = get_numerical_preprocessing_pipeline()
    
    # Kombinieren Sie die Feature-Engineering-Schritte und die Preprocessing-Pipeline
    full_pipeline = Pipeline(steps=[
        ('feature_creation', FunctionTransformer(create_features, kw_args={'features_config': FEATURES_CONFIG})),
        ('num_preprocessing', numerical_preprocessing_pipeline),  # Fügen Sie die Preprocessing-Pipeline hinzu
    ])
    
    return full_pipeline