import numpy as np
import random
import os
import time
from math import e,sqrt,sin,cos
import activation_functions
import prepare_data

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
    def add(self, units=1, dropout=0, activation="sigmoid", activation_deriv="none"):
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
                activations = activation_functions.select_function(self.each_layer_list[x][2], self.each_layer_list[x][2])
            else:
                activations = activation_functions.select_function(self.each_layer_list[x][2], self.each_layer_list[x][3])
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
    def train(self, x=None, y=None, x_test=None, y_test=None, epochs=1000, info=1, shake_data=False, batch_size=10):
        self.prepare_network()
        if len(self.each_layer_list) <= 1:
            print(f"TechAI.Error: No neural network found to train")
            return
        x,y = prepare_data.set_data(x,y,batch_size, shake_data)
        if self.ai_system_list[0].weights.shape[0] != x[0].shape[1]:
            print(f"TechAI.Error: Inputs {self.ai_system_list[0].weights.shape[0]} - InputData {x[0].shape[1]}")
        if self.ai_system_list[-1].weights.shape[1] != y[0].shape[1]:
            print(f"TechAI.Error: Outputs {self.ai_system_list[-1].weights.shape[1]} - OutputData {y[0].shape[1]}")
        for train in range(epochs):
            total_error = 0
            for nr in range(len(x)):
                forward = x[nr]
                for i in range(self.hidden_layers):
                    forward = self.activation_fucntions[i + 1](np.dot(forward,self.ai_system_list[i].weights))
                    self.ai_system_list[i].forward = forward

                self.ai_system_list[-1].error = y[nr] - self.ai_system_list[-1].forward
                self.ai_system_list[-1].delta = self.ai_system_list[-1].error * self.activation_fucntions_deriv[-1](self.ai_system_list[-1].forward)
                for i in range(self.hidden_layers - 1):
                    i += 1
                    ii = i + 1
                    self.ai_system_list[-ii].error = np.dot(self.ai_system_list[-i].delta, self.ai_system_list[-i].weights.T)
                    self.ai_system_list[-ii].delta = self.ai_system_list[-ii].error * self.activation_fucntions_deriv[-ii](self.ai_system_list[-ii].forward)
                total_error += np.mean(np.abs(self.ai_system_list[-1].error)).sum() / len(x)
                self.ai_system_list[0].weights += self.learning_rate * np.dot(x[nr].T, self.ai_system_list[0].delta)
                for i in range(1, self.hidden_layers):
                    self.ai_system_list[i].weights += self.learning_rate * np.dot(self.ai_system_list[i-1].forward.T, self.ai_system_list[i].delta)
            print(f"Iteration {train + 1}, Error {total_error}")
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