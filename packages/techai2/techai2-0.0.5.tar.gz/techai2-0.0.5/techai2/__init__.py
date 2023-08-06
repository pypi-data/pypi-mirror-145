import numpy as np
import os
import time
from activation_functions import *
import time
import random
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
def set_data(X, Y, batch_size, shake_data):
    X = np.array(X)
    Y = np.array(Y)
    if len(X) != len(Y):
        print("TechAI.Error: Data(X) and Data(Y) in't same Length")
    try:
        X = X.tolist()
    except:
        pass
    try:
        Y = Y.tolist()
    except:
        pass
    new_x = []
    new_y = []
    for x in range(len(X)):
        new_x.append(X[x])
        new_y.append(Y[x])
    new_x = np.array(new_x)
    new_y = np.array(new_y)
    shaked_x = []
    shaked_y = []
    quick_list = []
    if shake_data == True:
        for x in range(len(X)):
            quick_list.append(x)
        for x in range(len(X)):
            nr = random.choice(quick_list)
            quick_list.remove(nr)
            shaked_x.append(X[nr])
            shaked_y.append(Y[nr])
        new_x = np.array(shaked_x)
        new_y = np.array(shaked_y)
    X = new_x.copy()
    Y = new_y.copy()
    batch_X = []
    batch_Y = []
    bufor_x = []
    bufor_y = []
    nr = 0
    counter = len(X)
    while counter > 0:
        for x in range(batch_size):
            bufor_x.append(X[nr])
            bufor_y.append(Y[nr])
            counter -= 1
            nr += 1
            if counter == 0:
                break
        batch_X.append(bufor_x.copy())
        batch_Y.append(bufor_y.copy())
        bufor_x = []
        bufor_y = []
    new_x_b = []
    new_y_b = []
    for batch in batch_X:
        new_x_b.append(np.array(batch))
    for batch in batch_Y:
        new_y_b.append(np.array(batch))
    return new_x_b, new_y_b
class NeuralNetwork():
    def __init__(self):
        '''
        self.ai_system_list Zawiera klase AI_SYSTEM
        self.each_layer_list Zawiera ([Units, dropout, activation,activation_deriv])
        '''
        self.ai_system_list = []
        self.each_layer_list = []
        self.activation_fucntions = []
        self.activation_fucntions_deriv = []
        self.hidden_layers = 0
        self.learning_rate = 0.05
        self.optimizer = "none"
    def set_optimizer_momentum(self, momentum=0.9):
        self.optimizer = "momentum"
        self.momentum = momentum
    def add(self, units=1, dropout=0.0, activation="sigmoid", activation_deriv="none"):
        self.each_layer_list.append([units,dropout,activation, activation_deriv])
    def set_learning_rate(self, lr):
        self.learning_rate = lr
    def save(self, name):
        if len(self.each_layer_list) <= 1:
            print(f"TechAI.Error: No neural network found to save")
            return
        try:
            os.mkdir(f"Tech_AI2_{name}")
        except:
            pass
        self.prepare_network()
        for x in range(99):
            try:
                np.savetxt(f"Tech_AI2_{name}/weights_{x}", self.ai_system_list[x].weights)
            except:
                pass
        with open(f"Tech_AI2_{name}/settings", 'w') as f:
            f.write(f"{self.each_layer_list[:]}")
    def load(self, name):
        layer_list_copy = self.each_layer_list.copy()
        try:
            copy_each_layer_list = self.each_layer_list.copy()
            self.each_layer_list = []
            with open(f"Tech_AI2_{name}/settings", 'r') as f:
                mainlist = [line for line in f]
                mainlist = f"{mainlist[0]}"
                mainlist = mainlist.replace("[", "")
                mainlist = mainlist.replace("]", "")
                mainlist = mainlist.replace(",", "")
                mainlist = list(mainlist.split(" "))
                for x in range(len(mainlist) // 4):
                    x *= 4
                    self.each_layer_list.append([int(mainlist[x]), float(mainlist[x+1]), mainlist[x+2].replace("'",""), mainlist[x+3].replace("'","")])
                self.select_functions()
                self.hidden_layers = len(self.each_layer_list) - 1
                self.ai_system_list = []
                for x in range(len(self.each_layer_list) - 1):
                    self.ai_system_list.append(AI_SYSTEM(self.each_layer_list[x][0], self.each_layer_list[x + 1][0],self.each_layer_list[x + 1][1], self.each_layer_list[x + 1][2],self.each_layer_list[x + 1][3]))
                for x in range(len(self.each_layer_list) - 1):
                    self.ai_system_list[x].weights = np.loadtxt(f"Tech_AI2_{name}/weights_{x}")
                if copy_each_layer_list != self.each_layer_list:
                    print(f"TechAI.Waring: Main NeuralNetwork is different than the loaded one NeuralNetwork")
        except:
            print(f"TechAI.Error: No neural network found to load")
            self.each_layer_list = layer_list_copy
    def select_functions(self):
        for x in range(len(self.each_layer_list)):
            if self.each_layer_list[x][3] == "none":
                #activations = activation_functions.select_function(self.each_layer_list[x][2], self.each_layer_list[x][2])
                activations = select_function(self.each_layer_list[x][2], self.each_layer_list[x][2])
            else:
                #activations = activation_functions.select_function(self.each_layer_list[x][2], self.each_layer_list[x][3])
                activations = select_function(self.each_layer_list[x][2], self.each_layer_list[x][3])
            self.activation_fucntions.append(activations[0])
            self.activation_fucntions_deriv.append(activations[1])
    def prepare_network(self):
        if len(self.ai_system_list) == 0:
            self.select_functions()
            self.hidden_layers = len(self.each_layer_list) - 1
            for x in range(len(self.each_layer_list) - 1):
                self.ai_system_list.append(AI_SYSTEM(self.each_layer_list[x][0], self.each_layer_list[x+1][0], self.each_layer_list[x+1][1], self.each_layer_list[x+1][2], self.each_layer_list[x+1][3]))
    def forward_method(self, data):
        self.prepare_network()
        forward = data
        for i in range(self.hidden_layers):
            forward = self.activation_fucntions[i + 1](np.dot(forward, self.ai_system_list[i].weights))
            self.ai_system_list[i].forward = forward
        return forward
    def error_mse(self, x,y):
        data = self.forward_method(x)
        error = y - data
        return np.mean(np.abs(error)).sum()
    def dropout(self, dropout_size, weights, nr):
        all_weights = []
        counter = weights.shape[1] * dropout_size
        while counter > 0:
            for x in range(weights.shape[1]):
                if self.ai_system_list[nr].dropout_list[x] == 1:
                    for xs in range(weights.shape[0]):
                        weights[xs][x] = 0
                        counter -= 1
        all_weights.append(weights)
        all_weights = np.array(weights)
        return all_weights
    def select_droupout_neurons(self):
        for i in range(self.hidden_layers):
            if self.ai_system_list[i].dropout > 0:
                self.ai_system_list[i].dropout_list = np.zeros(len(self.ai_system_list[i].dropout_list))
                counter = self.ai_system_list[i].weights.shape[1] * self.ai_system_list[i].dropout
                while counter > 0:
                    random_neuron = np.random.randint(0, self.ai_system_list[i].weights.shape[1])
                    if self.ai_system_list[i].dropout_list[random_neuron] == 0:
                        self.ai_system_list[i].dropout_list[random_neuron] = 1
                        counter -= 1
    def train(self, x=None, y=None, x_test=None, y_test=None, epochs=1000, info=1, shake_data=False, batch_size=10):
        self.prepare_network()
        if len(self.each_layer_list) <= 1:
            print(f"TechAI.Error: No neural network found to train")
            return
        #x,y = prepare_data.set_data(x,y,batch_size, shake_data)
        #x_test, y_test = prepare_data.set_data(x_test, y_test, 999999, False)
        x,y = set_data(x,y,batch_size, shake_data)
        x_test, y_test = set_data(x_test, y_test, 999999, False)
        self.stats_error = []
        self.stats_error_test = []
        if self.ai_system_list[0].weights.shape[0] != x[0].shape[1]:
            print(f"TechAI.Error: Inputs {self.ai_system_list[0].weights.shape[0]} - InputData {x[0].shape[1]}")
        if self.ai_system_list[-1].weights.shape[1] != y[0].shape[1]:
            print(f"TechAI.Error: Outputs {self.ai_system_list[-1].weights.shape[1]} - OutputData {y[0].shape[1]}")
        for train in range(epochs):
            self.update = [0]*len(self.ai_system_list)
            self.select_droupout_neurons()
            total_error = 0
            total_error_test = 0
            for nr in range(len(x)):
                forward = x[nr]
                for i in range(self.hidden_layers):
                    forward = self.activation_fucntions[i + 1](np.dot(forward,self.ai_system_list[i].weights))
                    #self.ai_system_list[i].forward = forward
                    if self.ai_system_list[i].dropout > 0:
                        forward = self.dropout(self.ai_system_list[i].dropout, forward, i)
                    self.ai_system_list[i].forward = forward

                self.ai_system_list[-1].error = y[nr] - self.ai_system_list[-1].forward
                self.ai_system_list[-1].delta = self.ai_system_list[-1].error * self.activation_fucntions_deriv[-1](self.ai_system_list[-1].forward)
                for i in range(self.hidden_layers - 1):
                    i += 1
                    ii = i + 1
                    self.ai_system_list[-ii].error = np.dot(self.ai_system_list[-i].delta, self.ai_system_list[-i].weights.T)
                    self.ai_system_list[-ii].delta = self.ai_system_list[-ii].error * self.activation_fucntions_deriv[-ii](self.ai_system_list[-ii].forward)
                    if self.ai_system_list[-ii].dropout > 0:
                        self.ai_system_list[-ii].delta = self.dropout(self.ai_system_list[-ii].dropout, self.ai_system_list[-ii].delta, -ii)
                total_error += np.mean(np.abs(self.ai_system_list[-1].error)).sum() / len(x)

                if self.optimizer == "none":
                    self.ai_system_list[0].weights += self.learning_rate * np.dot(x[nr].T, self.ai_system_list[0].delta)
                    for i in range(1, self.hidden_layers):
                        self.ai_system_list[i].weights += self.learning_rate * np.dot(self.ai_system_list[i-1].forward.T, self.ai_system_list[i].delta)
                elif self.optimizer == "momentum":
                    self.ai_system_list[0].weights += self.update[0]
                    self.update[0] = self.learning_rate * np.dot(x[nr].T, self.ai_system_list[0].delta) + self.momentum * self.update[0]
                    for i in range(1, self.hidden_layers):
                        self.ai_system_list[i].weights += self.update[i]
                        self.update[i] = self.learning_rate * np.dot(self.ai_system_list[i-1].forward.T, self.ai_system_list[i].delta) + self.momentum * self.update[i]
                else:
                    print(f"TechAI.Error: Optimizer not found")
                    return
            total_error_test += self.error_mse(x_test, y_test)
            self.stats_error.append(total_error)
            self.stats_error_test.append(total_error_test)
            print(f"Iteration {train + 1}/{epochs}, Error {total_error}")
        return  (self.stats_error, self.stats_error_test)
class AI_SYSTEM():
    def __init__(self, n_in, n_out, dropout, activation, activation_deriv):
        self.weights = np.random.uniform(low=-1, high=1, size=(n_in, n_out))
        self.forward = np.zeros(n_out)
        self.delta = np.zeros(n_out)
        self.error = np.zeros(n_out)
        self.input = n_in
        self.input = n_out
        self.dropout = dropout
        self.activation = activation
        self.activation_deriv = activation_deriv
        self.dropout_list = np.zeros(n_out)