import random
import time
import numpy as np
import os
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def sigmoid_derivative(x):
    return x * (1 - x)

class TechNet():
    def __init__(self):
        self.Proccesses_list = []
        self.NeuralNetwosk_list = []
        self.NeuralNetwosk_Main = NeuralNetwork2(0)
        self.neurons_list = []
        self.learning_rate = 0.05
        self.droupout = 0
    def add(self, size):
        self.neurons_list.append(size)
        self.NeuralNetwosk_Main.add(size)
    def set_learning_rate(self, lr):
        self.learning_rate = lr
        self.NeuralNetwosk_Main.set_learning_rate(lr)
    def set_dropout(self, size):
        self.droupout = size
        self.NeuralNetwosk_Main.dropout_amount = size
    def set_ready(self):
        self.NeuralNetwosk_Main.set_ready(self.neurons_list, self.learning_rate, self.droupout)
    def save(self):
        pass
    def load(self):
        pass
    def scructure(self, klas):
        print("==============( Tech-AI)==============")
        for x in range(len(klas.neuron_each) - 2):
            print(f"Layer ({x+1}) - Neurons - {klas.neuron_each[x+1]}")
        print("==============( Tech-AI)==============")
    def train(self, X, Y, X_test=None, Y_test=None, epochs=1000, info=1, batch_size=10, shake_data=False):
        e = epochs
        i = info
        b = batch_size
        sd = shake_data

        self.best_network = []
        self.stats = []
        self.stats = None
        self.stats = self.NeuralNetwosk_Main.train(X, Y, X_test, Y_test, e, i, b, sd, self.neurons_list,self.learning_rate, self.droupout)


        return self.stats
    def forward_method(self, X):
        data = self.NeuralNetwosk_Main.forward_method(X)
        return data

        #NN.train(X, Y, epochs=10, info=1, batch_size=100, shake_data=False)
        #data = NN.forward_method(X)



class Layer2():
    def __init__(self, ins, outs):
        self.weights = np.random.uniform(low=-1, high=1, size=(ins, outs))
        self.forward = np.zeros(outs)
        self.error = np.zeros(outs)
        self.delta = np.zeros(outs)
        self.neurons = outs
        self.neurons_in = ins
        self.disabled_neurons = np.zeros(outs)

class NeuralNetwork2():
    def __init__(self, type):
        self.learning_rate = 0.165#0.0001
        self.dropout_amount = 0
        self.dropout_list = []
        self.neuron_each = []
        self.layersy = []
        self.stats = []
        self.interval_of_change_weights = 0
        self.interval_of_100 = 0
        self.batch_size = 0
        self.neuron_add_chance_list = []
        #self.best_training
        self.type = type

        #Dodawanie neurono z zmiana warstwy
        self.hidden_layers_sctucture = 0.60
        #Ile procent neuronow iwecej  dodac
        r = np.random.uniform(low=0.1, high=0.15)
        self.neurons_add_scructure = float(r)
    def set_dropout(self, size):
        self.dropout_amount = size
    def add(self, size):
        self.neuron_each.append(size)
    def set_learning_rate(self, lr):
        self.learning_rate = lr

    def forward_method(self, X):
        X, Y = self.fix_data(X, X, False)
        forward = X.copy()
        for x in range(0, len(self.neuron_each) - 1):
            forward = sigmoid(np.dot(forward, self.layersy[x].weights))
        return forward

    def fix_data(self, X, Y, shake_data):
        X = np.array(X)
        Y = np.array(Y)
        bufer = []
        try:
            if X.shape[1]:
                for x in range(len(X)):
                    bufer.append(X[x])
            X = np.array(bufer)
        except:
            X = np.array([X])
        bufer = []
        try:
            if Y.shape[1]:
                for x in range(len(Y)):
                    bufer.append(Y[x])
            Y = np.array(bufer)
        except:
            Y = np.array([Y])

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
            X = np.array(shaked_x)
            Y = np.array(shaked_y)
        return X, Y

    def set_batch(self, X, Y, batch_size):
        counter = len(X)
        batch_X = []
        batch_Y = []
        bufor_x = []
        bufor_y = []
        nr = 0
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
        #batch_X = np.array(batch_X)
        #batch_Y = np.array(batch_Y)

        return new_x_b, new_y_b
        #return batch_X, batch_Y

    def accuracy_test(self, X_T, Y_T, OUTPUT):
        pass
    def test_data_mse(self, X_T, Y_T):
        error = 0
        output = self.forward_method(X_T)
        error += np.mean(np.abs(Y_T - output)).sum()
        return error

    def save(self):
        pass
    def load(self):
        pass

    def train(self, X, Y, X_T=None, Y_T=None, epochs=1000, info=1, batch_size=10, shake_data=False, list_layers=None,lr=0.05 ,dropout=0):

        self.each_layer_neurons = list_layers.copy()
        self.neuron_each = list_layers.copy()
        self.dropout_amount = dropout
        self.learning_rate = lr

        self.test_error_stats = []
        self.train_error_stats = []

        self.batch_size = batch_size

        self.interval_of_change_weights = round(epochs * 0.01)
        self.interval_of_100 = round(epochs * 0.99)

        self.only_3_times_change_weights = 0

        if not self.dropout_list:
            for x in range(len(self.each_layer_neurons) - 1):
                self.layersy.append(Layer2(self.each_layer_neurons[x], self.each_layer_neurons[x + 1]))
                self.dropout_list.append(round(self.each_layer_neurons[x + 1] * self.dropout_amount))
            self.dropout_list.pop()
            self.hidden_layers = len(self.layersy) - 1



        X, Y = self.fix_data(X, Y, shake_data)
        X_T, Y_T = self.fix_data(X_T, Y_T, False)
        batch_X, batch_Y = self.set_batch(X,Y, batch_size)
        times = time.time()
        total_time = time.time()
        show_every = time.time()
        for training in range(epochs):
            training+=1
            total_error = 0
            for item in range(len(batch_X)):
                try:
                    X = np.array(batch_X[item])
                    X = np.reshape(X, (batch_size, X.shape[1]))
                except:
                    X = np.array(batch_X[item])
                    X = np.reshape(X, (len(batch_X[item]), X.shape[1]))

                try:
                    Y = np.array(batch_Y[item])
                    Y = np.reshape(Y, (batch_size, Y.shape[1]))
                except:
                    Y = np.array(batch_Y[item])
                    Y = np.reshape(Y, (len(batch_Y[item]), Y.shape[1]))


                for x in range(0, self.hidden_layers):
                    counter = self.dropout_list[x]
                    self.layersy[x].disabled_neurons = np.zeros(self.neuron_each[x + 1])
                    while counter > 0:
                        random_neuron = np.random.randint(low=0, high=len(self.layersy[x].disabled_neurons))
                        if self.layersy[x].disabled_neurons[random_neuron] == 0:
                            self.layersy[x].disabled_neurons[random_neuron] = 1
                            counter -= 1


                self.layersy[0].forward = sigmoid(np.dot(X, self.layersy[0].weights))
                for x in range(1,self.hidden_layers + 1):
                    self.layersy[x].forward = sigmoid(np.dot(self.layersy[x-1].forward, self.layersy[x].weights))

                self.layersy[-1].error = Y - self.layersy[-1].forward
                self.layersy[-1].delta = self.layersy[-1].error * sigmoid_derivative(self.layersy[-1].forward)

                for x in range(1, self.hidden_layers + 1):
                    xx = x + 1
                    self.layersy[-xx].error = np.dot(self.layersy[-x].delta, self.layersy[-x].weights.T)
                    self.layersy[-xx].delta = self.layersy[-xx].error * sigmoid_derivative(self.layersy[-xx].forward)

                for x in range(0, self.hidden_layers):
                    disable_list_delta = self.layersy[x].delta.flatten().tolist()
                    disable_list_forward = self.layersy[x].forward.flatten().tolist()
                    nr_counter = 0
                    for all in range(len(self.layersy[x].delta)):
                        for nr, value in enumerate(self.layersy[x].disabled_neurons):
                            if value == 1:
                                disable_list_delta[nr_counter] = 0
                            nr_counter += 1
                    new_array = np.array(disable_list_delta)
                    new_array = new_array.reshape(self.layersy[x].delta.shape[0], self.layersy[x].delta.shape[1])
                    self.layersy[x].delta = new_array

                    nr_counter = 0
                    for all in range(len(self.layersy[x].forward)):
                        for nr, value in enumerate(self.layersy[x].disabled_neurons):
                            if value == 1:
                                disable_list_forward[nr_counter] = 0
                            nr_counter += 1
                    new_array = np.array(disable_list_forward)
                    new_array = new_array.reshape(self.layersy[x].forward.shape[0], self.layersy[x].forward.shape[1])
                    self.layersy[x].forward = new_array


                self.layersy[0].weights += self.learning_rate * np.dot(X.T,self.layersy[0].delta)
                for x in range(1, self.hidden_layers + 1):
                    self.layersy[x].weights += self.learning_rate * np.dot(self.layersy[x - 1].forward.T,self.layersy[x].delta)

                total_error += np.mean(np.abs(self.layersy[-1].error))

            self.train_error_stats.append(self.test_data_mse(X,Y))
            self.test_error_stats.append(self.test_data_mse(X_T,Y_T))


            if info == 1 and time.time() - show_every > 0.7:
                print(f"iteration > {training}/{epochs} error > {total_error}")
                times = time.time()
                show_every = time.time()
            if training == epochs and self.type == 0:
                print(f"iteration > {training}/{epochs} error > {total_error} time > {time.time() - times}")

            self.stats.append(total_error)
            #times = time.time()
        if info == 1:
            print("====================(TechAI)====================")
            print(f"Error : {total_error}")
            print(f"Total time : {time.time() - total_time}")
            print("====================(TechAI)====================")
        return [self.train_error_stats, self.test_error_stats]

