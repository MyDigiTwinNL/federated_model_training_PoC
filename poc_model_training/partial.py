"""
This file contains all partial algorithm functions, that are normally executed
on all nodes for which the algorithm is executed.

The results in a return statement are sent to the vantage6 server (after
encryption if that is enabled). From there, they are sent to the partial task
or directly to the user (if they requested partial results).
"""
import pandas as pd
import time
from typing import Any
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from neural_network import NeuralNetwork
from data_preprocessor import preprocess_dataframe

from vantage6.algorithm.tools.util import info, warn, error
from vantage6.algorithm.tools.decorators import data


@data(1)
def partial(
    df1: pd.DataFrame, colname: str
) -> Any:

    df = preprocess_dataframe(df1)

    #TODO split data into training/validation subsets

    weights1, weights2, bias1, bias2 = model_train(df.to_numpy(), epochs=10, learning_rate=0.01)
    
    #TODO return the weights
    return df1[colname].max()
    

def model_train(data, epochs, learning_rate):
    """
    The first N-1 columns are used as features
    """
    #slice operation (remove last column [[A,B,C],[Q,W,E],[V,B,N]])    
    features = data[:, :-1]  # Features

    #get the elements of the last column as the target variable (1-dimension array) [3,6,9] , and turn into a 2d-one ([[3],[6],[9]])
    target = data[:, -1].reshape(-1, 1)  # Target variable

    # Ensure X and y are numpy arrays with float32 dtype
    features = np.asarray(features).astype(np.float32)
    target = np.asarray(target).astype(np.float32)
    
    model = NeuralNetwork(input_dim=features.shape[1], hidden_dim=64, output_dim=1)

    # Check for NaN values
    if np.isnan(features).any():
        raise ValueError("Input X contains NaN values")

    model.train(features, target, epochs, learning_rate)
    
    return model.weights1, model.weights2, model.bias1, model.bias2
