import pandas as pd
from sklearn.impute import SimpleImputer

def preprocess_input(input_df):
    if input_df.isnull().values.any():
        # Handle missing values using SimpleImputer only if there are non-missing values
        imputer = SimpleImputer(strategy='mean')  # You can choose a different strategy based on your needs
        input_df_imputed = pd.DataFrame(imputer.fit_transform(input_df), columns=input_df.columns)
    else:
        # If all values are missing, handle it according to your specific requirements
        # For example, you might choose to drop the column or replace missing values with a default value
        input_df_imputed = input_df.copy() 

    return input_df_imputed