import pandas as pd
from pipeline import get_full_pipeline, get_numerical_preprocessing_pipeline, get_feature_engineering_pipeline
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from xgboost import XGBRegressor
from feature_engineering import create_features
from features_config import FEATURES_CONFIG
import shap
import matplotlib.pyplot as plt
import numpy as np


# Set the path to the BTC-USD.csv file
btc_file_path = r'C:\Users\silas\OneDrive\Desktop\Bachlor Thesis\BTC-USD.csv'

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

def prepare_data(data):
    """
    Applies feature engineering and preprocessing to the input data.
    
    :param data: DataFrame containing the data to prepare.
    :return: Tuple containing the prepared feature matrix X and target vector y.
    """
    # Apply feature engineering using the provided configuration
    features = create_features(data, FEATURES_CONFIG)
    
    # Separate the features (X) from the target (y)
    X = features.drop('Close', axis=1)
    y = features['Close']
    return X, y

def train_and_evaluate_model(X_train, y_train, X_test, y_test):
    """
    Trains the model and evaluates it using mean absolute error.
    
    :param X_train: Training feature matrix.
    :param y_train: Training target vector.
    :param X_test: Testing feature matrix.
    :param y_test: Testing target vector.
    :return: Trained model.
    """
    # Get the preprocessing pipeline and apply it to the training data
    preprocessing_pipeline = get_numerical_preprocessing_pipeline()
    X_train_preprocessed = preprocessing_pipeline.fit_transform(X_train)
    
    # Apply the same preprocessing steps to the testing data
    X_test_preprocessed = preprocessing_pipeline.transform(X_test)

    # Initialize the XGBoost regressor and train it
    model = XGBRegressor(objective='reg:squarederror')
    model.fit(X_train_preprocessed, y_train)
    
    # Make predictions on the testing data
    predictions = model.predict(X_test_preprocessed)

    # Calculate and print the mean absolute error
    mae = mean_absolute_error(y_test, predictions)
    print(f"Mean Absolute Error: {mae:.2f}")

    return model


def analyze_model_with_shap(model, X_test_preprocessed, specific_sample=None):
    """
    Analyzes the trained model using SHAP values to interpret the model's predictions.
    
    :param model: The trained model to analyze.
    :param X_test_preprocessed: The preprocessed testing feature matrix.
    :param specific_sample: An optional specific sample index to analyze in detail.
    """
    # Initialize the SHAP explainer with the model and calculate SHAP values
    explainer = shap.Explainer(model)
    shap_values = explainer(X_test_preprocessed)
    
    # Plot the SHAP values for a summary plot
    shap.summary_plot(shap_values, X_test_preprocessed)

    # # Calculate the index of the feature with the highest mean absolute SHAP value
    # most_important_feature_index = np.argmax(np.abs(shap_values.values).mean(0))
    
    # # Plot the SHAP dependence plot for the most important feature
    # shap.plots.scatter(shap_values[:, most_important_feature_index], 
    #                    color=shap_values.values[:, most_important_feature_index])

    # # If a specific sample is provided, plot the SHAP force plot for that sample
    # if specific_sample is not None:
    #     shap.force_plot(explainer.expected_value, shap_values[specific_sample,:], X_test_preprocessed.iloc[specific_sample,:])

    # # If a specific sample is provided, plot the SHAP decision plot for that sample
    # if specific_sample is not None:
    #     shap.decision_plot(explainer.expected_value, shap_values[specific_sample,:], X_test_preprocessed.iloc[specific_sample,:])



def main():
    """
    The main execution function for the script. It loads the data, validates it, performs cross-validation,
    and trains and evaluates the model, saving it and analyzing with SHAP after each split.
    """
    # Load the data
    btc_data = pd.read_csv(btc_file_path)
    
    # Validate the data to ensure it meets the requirements
    validate_data(btc_data)
    
    # Set the 'Date' column as the index of the DataFrame
    btc_data['Date'] = pd.to_datetime(btc_data['Date'])
    btc_data.set_index('Date', inplace=True)

    # Initialize time-series cross-validation
    tscv = TimeSeriesSplit(n_splits=5)
    
    # Loop through each time-series split
    for i, (train_index, test_index) in enumerate(tscv.split(btc_data)):
        # Prepare the training and testing data
        train_data, test_data = btc_data.iloc[train_index], btc_data.iloc[test_index]
        X_train, y_train = prepare_data(train_data)
        X_test, y_test = prepare_data(test_data)

        # Train and evaluate the model
        model = train_and_evaluate_model(X_train, y_train, X_test, y_test)
        
        # Save the model in JSON format
        model.save_model(f'xgboost_model_split_{i}.json')
    
        # Analyze the model with SHAP
        analyze_model_with_shap(model, X_test)

# Check if the script is being run directly (as opposed to being imported) and execute main function
if __name__ == "__main__":
    main()
