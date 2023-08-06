from math import lgamma
import os 
import joblib
import numpy as np 
import logging as lg
 


class Perceptron(object):
    
    
    def __init__(self , eta : float = None , epochs : int = None ):
        
        lg.info(f"Initializing Perceptron {str(self)} with eta {eta} and epochs {epochs}")
        self.weights = np.random.randn(3)*1e-4 # small random weight 
        is_training =  (eta is not None) and (epochs is not None)
        if is_training:
            lg.info(f"initial weights before training: \n{self.weights}")
        self.eta = eta
        self.epochs = epochs
    
    def _z_outcome(self , input , weights):
        lg.info(f"Calculating z outcome with input {input} and weights {weights}")
        return np.dot(input, weights)
    
    def activate_function(self  ,Z ):
        lg.info(f"Activating function with Z {Z}")
        return np.where(Z > 0.0 , 1 , 0)
    
    def fit(self, X, y):
        self.X = X
        self.y = y
        X_with_bias = np.c_[self.X,-np.ones((len(self.X),1))]
        lg.info(f"X_with_bias: \n{X_with_bias}")
        for epoch in range(self.epochs):
            
            lg.info("--"*10)
            lg.info(f"for epoch >> {epoch}")
            lg.info("--"*10)
            
            z = self._z_outcome(X_with_bias, self.weights)
            y_hat   = self.activate_function(z)
            lg.info(f"predicted value after forward pass : \n{y_hat}")
            
            self.error = self.y - y_hat
            lg.info(f"error after forward pass : \n{self.error}")
            self.weights = self.weights +  self.eta  * np.dot(X_with_bias.T, self.error)
            lg.info(f"weights after forward pass epos {epoch} of {self.epochs}: \n{self.weights}")
            lg.info("-*-"*10)
        
            
    def predict(self, X):
        X_with_bias = np.c_[X,-np.ones((len(X),1))]
        z = self._z_outcome(X_with_bias , self.weights)
        return self.activate_function(z)
    
    def total_loss(self):
        total_loss = np.sum(self.error)
        lg.info(f"total loss : {total_loss}\n")
        return total_loss
    
        
    
    def _create_dir_return_path(self, model_dir , filename):
        os.makedirs(model_dir , exist_ok= True )
        return os.path.join(model_dir, filename)
        
    
    
    def save_model(self, filename , model_dir = None):
        if model_dir is not None:
            model_file_path = self._create_dir_return_path(model_dir , filename)
            joblib.dump(self, model_file_path)
            lg.info(f"Model save {model_file_path}")
        else : 
            model_file_path = self._create_dir_return_path("model" , filename)
            joblib.dump(self , model_file_path)
            lg.info(f"Model save {model_file_path}")
        
        
    
    def load_model(self, model_file_path):
        lg.info(f"Loading model from {model_file_path}")
        return joblib.load(model_file_path)
    