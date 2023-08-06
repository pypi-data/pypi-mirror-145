# Nait
# Neural Artificial Intelligence Tool
# Version 2.0.2

"""
Nait

Neural Articicial Intelligence Tool
Version 2.0.2

Utility:

Network - class
|
| train - method
| predict - method
| save - method
| load - method
| evaluate - method
| values - method
"""

import random
import math
import copy
import time
import json
import os

class Network:
    """
    Nait
    
    class for creating a neural network
    containing everything needed for training, using and testing a neural network
    
    Network values:
    
    * weights
    * biases
    * activation_function
    
    usage:
    
    Network()
    
    methods:
    
    * train
    * predict
    * save
    * load
    * evaluate
    * values
    """
    def __init__(self):

        # Generating layers
        self.weights = []
        for _ in range(2):
            layer = []

            for _ in range(4):
                layer.append([0]*4)
            self.weights.append(layer)

        self.biases = []
        for _ in range(2):
            self.biases.append([0]*4)

    def train(self,
              x=[[1, 1, 1, 1]],
              y=None,
              structure=(4, 4, 4),
              activation_function="linear",
              generate_network=True,
              learning_rate=0.01,
              batch_size=10,
              sample_size=None,
              loss_function=None,
              epochs=100,
              backup=False,
              verbose=True):
        """
        Nait
        
        function for training a network to improve at a given task
        comes with a large variety of customization options for the training process
        
        usage:
        
        train(x=[[1, 1, 1, 1]],
              y=None,
              structure=(4, 4, 4),
              activation_function="linear",
              generate_network=True,
              learning_rate=0.01,
              batch_size=10,
              sample_size=None,
              loss_function=None,
              epochs=100,
              backup=None,
              verbose=True)
        """
        
        print("initiating network training")

        # Verifying training data
        if verbose == True: print("verifying training data... ", end="")
        if loss_function == None:
            if len(x) != len(y):
                raise ValueError("length of x should equal the length of y")
        if len(structure) < 2:
            raise ValueError("can not have less than 2 layers")
        if verbose == True: print("OK")

        start_time = time.time()

        # Generating layers
        if generate_network == True:
            if verbose == True: print("creating network structure... ", end="")
            self.activation_function = activation_function
            self.weights = []
            self.biases = []
            
            for structure_i in range(1, len(structure)):
                
                self.weights.append([[round(random.uniform(-1, 1), 8) for _ in range(structure[structure_i - 1])] for _ in range(structure[structure_i])])
                self.biases.append([0.0 for _ in range(structure[structure_i])])

            if verbose == True: print("OK")

        if verbose == True: print("creating forward functions... ", end="")
        
        # Layer foward function
        def layer_forward(layer_input, layer_weights, layer_biases):
            layer_output = []

            for neuron_index in range(len(layer_weights)):
                neuron_output = []

                for weight_index in range(len(layer_weights[neuron_index])):
                    neuron_output.append(layer_input[weight_index] * layer_weights[neuron_index][weight_index])

                neuron_output = sum(neuron_output) + layer_biases[neuron_index]

                if self.activation_function == 'relu':
                    if neuron_output < 0:
                        neuron_output = 0

                if self.activation_function == 'step':
                    if neuron_output >= 1:
                        neuron_output = 1
                    else:
                        neuron_output = 0

                if self.activation_function == 'sigmoid':
                    sig = 1 / (1 + math.exp(-neuron_output))
                    neuron_output = sig

                if self.activation_function == 'leaky_relu':
                    if neuron_output < 0:
                        neuron_output = neuron_output * 0.1

                layer_output.append(round(neuron_output, 8))

            return layer_output

        # Forward function
        def network_forward(network_input, weights, biases):
            network_output = network_input
            for weight_index in range(len(weights)):
                network_output = layer_forward(network_output, weights[weight_index], biases[weight_index])
            return network_output
        
        if verbose == True: print("OK")

        # Training
        epoch = 0
        starting_loss = None

        while epoch < epochs:

            epoch += 1

            # Generating training samples for this epoch
            if sample_size != None:
                x_samples = random.sample(x, sample_size)
                if loss_function == None:
                    y_samples = [y[x_samples.index(x_input)] for x_input in x_samples]
                else:
                    y_samples = []
            else:
                x_samples = x
                y_samples = y

            # Generating batch
            batch_weights = [self.weights]
            batch_biases = [self.biases]

            for _ in range(batch_size):

                batch_weights.append(copy.deepcopy(self.weights))
                batch_biases.append(copy.deepcopy(self.biases))

                for layerindex in range(len(batch_weights[0])):
                    for neuronindex in range(len(batch_weights[0][layerindex])):
                        batch_biases[0][layerindex][neuronindex] = round(
                            random.uniform(learning_rate, learning_rate*-1) + batch_biases[0][layerindex][neuronindex], 8)

                        for weightindex in range(len(batch_weights[0][layerindex][neuronindex])):
                            batch_weights[0][layerindex][neuronindex][weightindex] = round(
                                random.uniform(learning_rate, learning_rate*-1) + batch_weights[0][layerindex][neuronindex][weightindex], 8)

                for layerindex in range(len(batch_weights[0])):
                    for neuronindex in range(len(batch_weights[0][layerindex])):
                        batch_biases[0][layerindex][neuronindex] = round(
                            random.uniform(learning_rate*0.1, learning_rate*-0.1) + batch_biases[0][layerindex][neuronindex], 8)

                        for weightindex in range(len(batch_weights[0][layerindex][neuronindex])):
                            batch_weights[0][layerindex][neuronindex][weightindex] = round(
                                random.uniform(learning_rate*0.1, learning_rate*-0.1) + batch_weights[0][layerindex][neuronindex][weightindex], 8)
            
            class network_forward_class():
                def __init__(self, weights, biases):
                    self.weights = weights
                    self.biases = biases
                def predict(self, network_input):
                    network_output = network_input
                    for weight_index in range(len(self.weights)):
                        network_output = layer_forward(network_output, self.weights[weight_index], self.biases[weight_index])
                    return network_output

            # Selection
            losses = []
            for i in range(len(batch_weights)):
                if loss_function == None:
                    current_loss = 0
                    for x_index in range(len(x_samples)):
                        network_output = network_forward(x_samples[x_index], batch_weights[i], batch_biases[i])
                        neuron_loss = 0
                        for output_index in range(len(y_samples[x_index])):
                            neuron_loss += abs(network_output[output_index] - y_samples[x_index][output_index])
                        current_loss += neuron_loss
                    losses.append(current_loss)
                else:
                    forward_class = network_forward_class(batch_weights[i], batch_biases[i])
                    losses.append(loss_function(forward_class, x_samples, y_samples))

            if starting_loss == None:
                starting_loss = min(losses)

            self.weights = batch_weights[losses.index(min(losses))]
            self.biases = batch_biases[losses.index(min(losses))]

            if epoch == 1:
                if (time.time() - start_time) * epochs >= 60:
                    if verbose == True: print(f"estimated time: {math.floor(((time.time() - start_time) * epochs) / 60)}m")
                else:
                    if verbose == True: print(f"estimated time: {math.floor((time.time() - start_time) * epochs)}s")
            
            filled_loadingbar = "█"
            unfilled_loadingbar = " "

            bar_filled = round(epoch / epochs * 40)

            if round(epoch % (epochs / 50), 0) == 0 or epoch == epochs:
                if ((time.time() - start_time) / (epoch / epochs)) * (1 - (epoch / epochs)) >= 60:
                    if verbose == True: print(f"loss: {round(min(losses), 8)} - average loss: {round(min(losses)/len(x), 8)} - epoch {epoch}/{epochs} - time remaining: {math.floor((((time.time() - start_time) / (epoch / epochs)) * (1 - (epoch / epochs))) / 60)}m" + " " * 50)
                else:
                    if verbose == True: print(f"loss: {round(min(losses), 8)} - average loss: {round(min(losses)/len(x), 8)} - epoch {epoch}/{epochs} - time remaining: {math.floor(((time.time() - start_time) / (epoch / epochs)) * (1 - (epoch / epochs)))}s" + " " * 50)

                if backup == True:
                    if not os.path.exists("backups/"):
                        os.mkdir("backups")
                    data = {}
                    data['weights'] = self.weights
                    data['biases'] = self.biases
                    data['activation'] = self.activation_function

                    with open(f"backups/backup_model_{round(epoch / (epochs / 50))}_loss_{round(min(losses), 8)}.json", 'w') as backup_file:
                        json.dump(data, backup_file)

            else:
                if verbose == True: print(f"training... |{filled_loadingbar * bar_filled}{unfilled_loadingbar * (40 - bar_filled)}| {round((epoch / epochs) * 100, 1)}% - loss: {round(min(losses), 8)} - average loss: {round(min(losses)/len(x), 8)} - epoch {epoch}/{epochs}" + " " * 50, end="\r")
                else: print(f"training... |{filled_loadingbar * bar_filled}{unfilled_loadingbar * (40 - bar_filled)}| {round((epoch / epochs) * 100, 1)}% - loss: {round(min(losses), 8)}" + " " * 50, end="\r")

        # Post training
        if verbose == True: 
            if (time.time() - start_time) * (epoch / epochs) >= 60:
                print(f"training finished - loss: {round(min(losses), 8)} - average loss: {round(min(losses)/len(x), 8)} - improvement: {round(starting_loss - min(losses), 8)} - improvement percentage: {round((1 - min(losses) / starting_loss) * 100, 8)}% - training time: {math.floor(((time.time() - start_time) / (epoch / epochs)) / 60)}m")
            else:
                print(f"training finished - loss: {round(min(losses), 8)} - average loss: {round(min(losses)/len(x), 8)} - improvement: {round(starting_loss - min(losses), 8)} - improvement percentage: {round((1 - min(losses) / starting_loss) * 100, 8)}% - training time: {math.floor((time.time() - start_time) / (epoch / epochs))}s")
        else:
            if (time.time() - start_time) * (epoch / epochs) >= 60:
                print(f"\ntraining finished - loss: {round(min(losses), 8)} - training time: {math.floor(((time.time() - start_time) / (epoch / epochs)) / 60)}m")
            else:
                print(f"\ntraining finished - loss: {round(min(losses), 8)} - training time: {math.floor((time.time() - start_time) / (epoch / epochs))}s")
        
        return round(min(losses), 8)

    def predict(self, inputs):
        """
        Nait
        
        function for passing a single input array through the network
        
        usage:
        
        predict(input)
        """

        # Layer foward function
        def layer_forward(layer_input, layer_weights, layer_biases):
            layer_output = []

            for neuron_index in range(len(layer_weights)):
                neuron_output = []

                for weight_index in range(len(layer_weights[neuron_index])):
                    neuron_output.append(layer_input[weight_index] * layer_weights[neuron_index][weight_index])

                neuron_output = sum(neuron_output) + layer_biases[neuron_index]
                
                if self.activation_function == 'relu':
                    if neuron_output < 0:
                        neuron_output = 0

                if self.activation_function == 'step':
                    if neuron_output >= 1:
                        neuron_output = 1
                    else:
                        neuron_output = 0

                if self.activation_function == 'sigmoid':
                    sig = 1 / (1 + math.exp(-neuron_output))
                    neuron_output = sig

                if self.activation_function == 'leaky_relu':
                    if neuron_output < 0:
                        neuron_output = neuron_output * 0.1

                layer_output.append(neuron_output)

            return layer_output

        # Forward function
        def network_forward(network_input, weights, biases):
            network_output = network_input
            for weight_index in range(len(weights)):
                network_output = layer_forward(network_output, weights[weight_index], biases[weight_index])
            return network_output

        return network_forward(inputs, self.weights, self.biases)
    
    def save(self, file="model.json"):
        """
        Nait
        
        function for exporting the network into a json file 
        which can late be imported with load()
        
        usage:
        
        save(file="model.json")
        """
        
        data = {}

        data['weights'] = self.weights
        data['biases'] = self.biases
        data['activation'] = self.activation_function

        with open(file, 'w') as file:
            json.dump(data, file)
        
        return True
    
    def load(self, file="model.json"):
        """
        Nait
        
        function for importing a network json file exported with save()
        
        usage:
        
        load(file="model.json")
        """

        with open(file, 'r') as file:
            data = json.load(file)

        self.weights = data['weights']
        self.biases = data['biases']
        self.activation_function = data['activation']
    
        return True
    
    def evaluate(self,
                 x,
                 y=None, 
                 loss_function=None, 
                 output_to_screen=True):
        """
        Nait
        
        function to get a loss and average loss of a network
        with completely new inputs and outputs without changing the network
        
        usage:
        
        evaluate(x,
                 y=None, 
                 loss_function=None, 
                 output_to_screen=True)
        """

        # Layer foward function
        def layer_forward(layer_input, layer_weights, layer_biases):
            layer_output = []

            for neuron_index in range(len(layer_weights)):
                neuron_output = []

                for weight_index in range(len(layer_weights[neuron_index])):
                    neuron_output.append(layer_input[weight_index] * layer_weights[neuron_index][weight_index])

                layer_output.append(sum(neuron_output) + layer_biases[neuron_index])

            return layer_output

        # Forward function
        def network_forward(network_input, weights, biases):
            network_output = network_input
            for weight_index in range(len(weights)):
                network_output = layer_forward(network_output, weights[weight_index], biases[weight_index])
            return network_output

        class network_forward_class():
            def __init__(self, weights, biases):
                self.weights = weights
                self.biases = biases
            def predict(self, network_input):
                network_output = network_input
                for weight_index in range(len(self.weights)):
                    network_output = layer_forward(network_output, self.weights[weight_index], self.biases[weight_index])
                return network_output

        # Evaluation
        if loss_function == None:
            current_loss = 0
            for x_index in range(len(x)):
                network_output = network_forward(x[x_index], self.weights, self.biases)
                neuron_loss = 0
                for output_index in range(len(y[x_index])):
                    neuron_loss += abs(network_output[output_index] - y[x_index][output_index])
                current_loss += neuron_loss
            loss = current_loss
        else:
            forward_class = network_forward_class(self.weights, self.biases)
            loss = loss_function(forward_class, x, y)

        if output_to_screen == True: print(f"evaluation - loss: {round(loss, 8)} - average loss: {round(loss/len(x), 8)}")

        return (round(loss, 8), round(loss/len(x), 8))
    
    def values(self):
        """
        Nait
        
        function for printing the network values
        in a readable format
        
        usage:
        
        values()
        """
        
        for weight_layer, biases_layer, i in list(zip(self.weights, self.biases, range(len(self.weights)))):
            
            print(f"\nlayer {i}\n")
            
            for neuron, bias, i2 in list(zip(weight_layer, biases_layer, range(len(weight_layer)))):
                print(f"    {' '.join([str(weight) for weight in neuron])} > {bias}")
                
        print(f"\nactivation: {self.activation_function}")

        value_count = sum([len(x[0]) * len(x) for x in self.weights]) + sum([len(x) for x in self.biases])

        print(f"\ntotal number of values: {value_count}\n")

        return True

if __name__ == "__main__":
    print("Nait v2.0.2")