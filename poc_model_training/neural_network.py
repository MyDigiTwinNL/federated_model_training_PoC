import pandas as pd
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(x, 0)

class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.weights1 = np.random.randn(input_dim, hidden_dim).astype(np.float32)
        self.weights2 = np.random.randn(hidden_dim, output_dim).astype(np.float32)
        self.bias1 = np.zeros((hidden_dim,), dtype=np.float32)
        self.bias2 = np.zeros((output_dim,), dtype=np.float32)
        
    def forward(self, features):
        self.hidden_layer = relu(np.dot(features.astype(np.float32), self.weights1) + self.bias1)
        self.output_layer = sigmoid(np.dot(self.hidden_layer, self.weights2) + self.bias2)
        return self.output_layer
    
    def backward(self, features, target, learning_rate):
        output_error_grad = target.astype(np.float32) - self.output_layer
        hidden_error_grad = output_error_grad.dot(self.weights2.T) * (self.hidden_layer > 0)
        
        self.weights2 += learning_rate * self.hidden_layer.T.dot(output_error_grad)
        self.bias2 += learning_rate * np.sum(output_error_grad, axis=0)
        
        self.weights1 += learning_rate * features.astype(np.float32).T.dot(hidden_error_grad)
        self.bias1 += learning_rate * np.sum(hidden_error_grad, axis=0)
    
    def train(self, features, target, epochs, learning_rate):
        for _ in range(epochs):
            self.forward(features)
            self.backward(features, target, learning_rate)
    
    def predict(self, features):
        return self.forward(features) > 0.5
