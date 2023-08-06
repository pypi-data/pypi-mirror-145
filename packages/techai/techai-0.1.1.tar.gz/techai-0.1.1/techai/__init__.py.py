import time

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def sigmoid_derivative(x):
    return x * (1 - x)



class Layer():
    def __init__(self, ins, outs):
        self.weights = np.random.uniform(low=-1, high=1, size=(ins, outs))
        self.forward = np.zeros(outs)
        self.error = np.zeros(outs)
        self.delta = np.zeros(outs)
        self.neurons = outs
        self.neurons_in = ins

class NeuralNetwork():
    def __init__(self):
        self.learning_rate = 0.065#0.0001

        self.neuron_each = []
        self.layersy = []
    def add(self, size):
        self.neuron_each.append(size)
    def set_ready(self):
        for x in range(len(self.neuron_each) - 1):
            self.layersy.append(Layer(self.neuron_each[x], self.neuron_each[x+1]))
        self.hidden_layers = len(self.layersy) - 1

    def forward_method(self, X):
        X, Y = self.fix_data(X, X)
        forward = X
        for x in range(0, self.hidden_layers + 1):
            forward = sigmoid(np.dot(forward, self.layersy[x].weights))
        return forward


    def fix_data(self, X, Y):
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
        return X, Y
    def train(self, X, Y, epochs=1000):
        X, Y = self.fix_data(X, Y)
        times = time.time()
        total_time = time.time()
        for training in range(epochs):
            training+=1
            total_error = 0
            for item in range(len(X)):
                for neuron in range(self.layersy[0].neurons):
                    self.layersy[0].forward[neuron] = sigmoid(np.dot(X[item], self.layersy[0].weights.T[neuron]))
                for x in range(1,self.hidden_layers):
                    for neuron in range(self.layersy[x].neurons):
                        self.layersy[x].forward[neuron] = sigmoid(np.dot(self.layersy[x-1].forward, self.layersy[x].weights.T[neuron]))
                for neuron in range(self.layersy[-1].neurons):
                    self.layersy[-1].forward[neuron] = sigmoid(np.dot(self.layersy[-2].forward, self.layersy[-1].weights.T[neuron]))


                for neuron in range(self.layersy[-1].neurons):
                    self.layersy[-1].error[neuron] = Y[item][neuron] - self.layersy[-1].forward[neuron]
                for neuron in range(self.layersy[-1].neurons):
                    self.layersy[-1].delta[neuron] = self.layersy[-1].error[neuron] * sigmoid_derivative(self.layersy[-1].forward[neuron])

                for x in range(1, self.hidden_layers + 1):
                    xx = x + 1
                    for neuron in range(self.layersy[-xx].neurons):
                        self.layersy[-xx].error[neuron] = np.dot(self.layersy[-x].delta,self.layersy[-x].weights[neuron])
                        self.layersy[-xx].delta[neuron] = self.layersy[-xx].error[neuron] * sigmoid_derivative(self.layersy[-xx].forward[neuron])


                self.layersy[0].weights += self.learning_rate * np.dot(np.array([X[0]]).T,np.array([self.layersy[0].delta]))

                for x in range(1, self.hidden_layers + 1):
                    self.layersy[x].weights += self.learning_rate * np.dot(np.array([self.layersy[x-1].forward]).T,np.array([self.layersy[x].delta]))


                total_error += np.mean(np.abs(self.layersy[-1].error))

            print(f"iteration > {training}/{epochs} error > {total_error} time > {time.time() - times}")
            times = time.time()
        print(f"Finished in > {time.time() - total_time}")