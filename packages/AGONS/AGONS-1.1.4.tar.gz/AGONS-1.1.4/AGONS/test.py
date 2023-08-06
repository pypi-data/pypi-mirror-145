# %%
"""Test how custom functions work with sklearn package."""
import numpy as np
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
x = np.array([[1,2,3], [6,5,4], [8,7,9]])
print(x)
def SSRow(X):
    X_ = X.copy()
    X_t = StandardScaler().fit_transform(X_.T).T 
    return X_t

def MMRow(X):
    X_ = X.copy()
    X_t = MinMaxScaler().fit_transform(X_.T).T
    return X_t

d = FunctionTransformer(SSRow)
print(d.fit_transform(x))
e = FunctionTransformer(MMRow)
print(e.fit_transform(x))
# %%
"""Testing AGONS with Iris Dataset"""
