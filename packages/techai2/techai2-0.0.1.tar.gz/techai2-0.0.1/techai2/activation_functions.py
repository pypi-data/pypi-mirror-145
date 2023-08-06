import numpy as np
from math import e,sqrt,sin,cos
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def sigmoid_deriv(x):
    return x * (1 - x)
def tanh(x):
    return np.tanh(x)
def tanh_deriv(x):
    return 1.0 - np.tanh(x) ** 2
def arctan(x):
    return np.arctan(x)
def arctan_deriv(x):
    return 1 / ((x ** 2) + 1)
def isrlu(x,a=0.01):
    return np.where(x < 0, x/np.sqrt(1+(a*(x**2))), x)
def isrlu_deriv(x,a=0.01):
    return np.where(x < 0, (1/np.sqrt(1+(a*(x**2))))**3, 1)
def softsign(x):
    return x / (abs(x) + 1)
def softsign_dash(x):
    return 1 / (abs(x) + 1)**2
def bentid(x):
    return (np.sqrt(((x**2)+1)-1)/2)+x
def bentid_deriv(x):
    return (x/(2*(np.sqrt((x**2)+1))))+1
def elu(x, a=0.01):
    return np.where(x <= 0, a * (((e) ** 2) - 1), x)
def elu_deriv(x, a=0.01):
    return np.where(x <= 0, elu(x, a) + a, 1)
def relu(x):
    return np.where(x < 0.0, 0, x)
def relu_deriv(x):
    return np.where(x < 0.0, 0, 1)
def softplus(x):
    return np.log(1+((e)**x))
def softplus_deriv(x):
    return 1/(1+((e)**-x))
def SWISH(x):
    b = 1.0
    return x * sigmoid(b * x)
def SWISH_derivative(x):
    b = 1.0
    return b * SWISH(x) + sigmoid(b * x)* (1 - b * SWISH(x))
def the_softmax(Z):
    return np.exp(Z) / np.sum(np.exp(Z))
def select_function(activation, activation_deriv):
    new_activation = []
    new_activation_deriv = []
    if activation == "sigmoid":
        new_activation = sigmoid
    if activation_deriv == "sigmoid":
        new_activation_deriv = sigmoid_deriv
    if activation == "tanh":
        new_activation = tanh
    if activation_deriv == "tanh":
        new_activation_deriv = tanh_deriv
    if activation == "arctan":
        new_activation = arctan
    if activation_deriv == "arctan":
        new_activation_deriv = arctan_deriv
    if activation == "isrlu":
        new_activation = isrlu
    if activation_deriv == "isrlu":
        new_activation_deriv = isrlu_deriv
    if activation == "softsign":
        new_activation = softsign
    if activation_deriv == "softsign":
        new_activation_deriv = softsign_dash
    if activation == "bentid":
        new_activation = bentid
    if activation_deriv == "bentid":
        new_activation_deriv = bentid_deriv
    if activation == "elu":
        new_activation = elu
    if activation_deriv == "elu":
        new_activation_deriv = elu_deriv
    if activation == "relu":
        new_activation = relu
    if activation_deriv == "relu":
        new_activation_deriv = relu_deriv
    if activation == "softplus":
        new_activation = softplus
    if activation_deriv == "softplus":
        new_activation_deriv = softplus_deriv
    if activation == "swish":
        new_activation = SWISH
    if activation_deriv == "swish":
        new_activation_deriv = SWISH_derivative
    if activation_deriv == "softmax":
        new_activation_deriv = the_softmax
    return new_activation, new_activation_deriv