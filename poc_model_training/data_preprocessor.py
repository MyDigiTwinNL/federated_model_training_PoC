import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer

def preprocess_dataframe(df: pd.DataFrame):
    """

    """
    # Separating numerical and categorical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns

    # Normalizing (scaling) all the numerical variables
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_numerical_scaled = pd.DataFrame(scaler.fit_transform(df[numerical_cols]),columns=numerical_cols)

    # Data imputation of missing numerical variables (after normalization)
    imputer = SimpleImputer(strategy='mean')
    df_scaled_imputed_numerical = pd.DataFrame(imputer.fit_transform(df_numerical_scaled[numerical_cols]), columns=numerical_cols)

    
    # Note: there is no missing data on (Medical) Conditions, as the on the harmonized FHIR data, according
    # to the mapping, can only be 'Active' or simply do not exist (None). While doing this I realized that in the defined
    # pairing rules (See ISSUE #X) we may be including 'undefined' (Medical) Conditions (with not certainity on wether the participant
    # had a prevalent or incident one), with the ones that are simply no present.
    # As it is not possible to represent an 'undefined' Condition status in FHIR, this means that this kind of
    # imputation will be needed BEFORE harmonizing the data.

    df_categorical = df[categorical_cols].copy()

    # Encoding condition statuses (Active/None) as numeric values
    df_categorical['CVD_STATUS'] = df_categorical['CVD_STATUS'].map({'Active': 1, None: 0})
    df_categorical['STROKE_STATUS'] = df_categorical['STROKE_STATUS'].map({'Active': 1, None: 0})
    df_categorical['MYOCARDIAL_INFARCTION_STATUS'] = df_categorical['MYOCARDIAL_INFARCTION_STATUS'].map({'Active': 1, None: 0})
    df_categorical['HEART_FAILURE_STATUS'] = df_categorical['HEART_FAILURE_STATUS'].map({'Active': 1, None: 0})
    df_categorical['T2D_STATUS'] = df_categorical['T2D_STATUS'].map({'Active': 1, None: 0})

    # One-hot encode the categorical column 'Gender'
    df_categorical = pd.get_dummies(df_categorical, columns=['GENDER'], dtype=int)

    # Combining both categorical and numerical variables
    df_preprocessed = pd.concat([df_scaled_imputed_numerical, df_categorical], axis=1)


    # Set the target variable as the last column
    target_col = df_preprocessed.pop('CVD_STATUS')
    df_preprocessed.insert(len(df_preprocessed.columns), 'CVD_STATUS', target_col)

    return df_preprocessed    