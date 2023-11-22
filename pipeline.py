import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from feature_engineering import create_lag_features

def get_preprocessing_pipeline(numerical_features):
    # Pipeline für numerische Features
    numerical_pipeline = Pipeline(steps=[
        ('imputation', SimpleImputer(strategy='mean')),  # Fehlende Werte ersetzen
        ('scaling', StandardScaler())  # Skalierung der Features
    ])
    
    # Gesamte Vorverarbeitungspipeline
    preprocessing_pipeline = ColumnTransformer(transformers=[
        ('num', numerical_pipeline, numerical_features),  # 'numerical_features' ist die Liste Ihrer numerischen Spalten
    ])
    
    return preprocessing_pipeline

def get_feature_engineering_pipeline():
    # Pipeline, die Feature-Engineering und Vorverarbeitung kombiniert
    full_pipeline = Pipeline(steps=[
        ('lag_features', FunctionTransformer(create_lag_features)),
        ('preprocessing', get_preprocessing_pipeline(numerical_features=['price_lag1', 'price_lag7', 'price_lag30'])),
    ])
    
    return full_pipeline
