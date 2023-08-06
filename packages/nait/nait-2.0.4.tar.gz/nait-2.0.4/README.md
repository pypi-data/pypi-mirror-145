---

# Nait

---

**Neural network module**
**Simple but powerful**




## Network - *class*

---

### Description

class for creating a neural network
containing everything needed for training, using and testing a neural network

### Syntax

**`network()`**

### Values

- weights
- biases
- activation_function

### Methods

- train
- predict
- save
- load
- evaluate
- values




## train - *method*

---

### Description

function for training a network to improve at a given task
comes with a large variety of customization options for the training process

### Syntax

**`train(x=[[1, 1, 1, 1]], y=None, structure=(4, 4, 4), activation_function="linear", generate_network=True, learning_rate=0.01, batch_size=10, sample_size=None, loss_function=None, epochs=100, backup=False, verbose=True)`**

### Arguments

- x - training inputs
- y - training outputs
- structure - array of layer sizes
- activation_function - function applied to the output of each layer (linear / relu / step / sigmoid / leaky_relu)
- generate_network - if the program should generate a new structure or try to train the existing one
- learning_rate - how drastically the network will try to improve
- batch_size - how many variations the network will try each epoch
- sample_size - how much of the dataset the network will train on each epoch - if set to none the network will use the whole dataset
- loss_function - the function used for calculating loss - if set to none the program will use output to y difference - more information lower on the page
- epochs - number of epochs the network should train for
- backup - if the network should backup itself while it trains
- verbose - if the network should output additional information to the screen while training




## predict - *method*

---

### Description

function for passing a single input array through the network

### Syntax

**`predict(input)`**

### Arguments

- input - input array




## save - *method*

---

### Description

function for exporting the network into a json file 
which can late be imported with load()

### Syntax

**`save(file="model.json")`**

### Arguments

- file - where to save




## load - *method*

---

### Description

function for importing a network json file exported with save()

### Syntax

**`save(file="model.json")`**

### Arguments

- file - where to save




## evaluate - *method*

---

### Description

function to get a loss and average loss of a network
with completely new inputs and outputs without changing the network

### Syntax

**`evaluate(x=[[1, 1, 1, 1]], y=None, loss_function=None, output_to_screen=True)`**

### Arguments

- x - testing inputs
- y - testing outputs
- loss_function - the function used for calculating loss - if set to none the program will use output to y difference - more information lower on the page
- output_to_screen - if the network should output the result of the evaulation to the console




## values - *method*

---

### Description

function for printing the network values
in a readable format

### Syntax

**`values()`**




# Additional information

## Creating a loss function

---

to create a loss function for the 'train' and 'evaluate' function
you create a function which takes three arguments: forward, x, y

- forward - a class that can be used pass an input through the network - usage: forward.predict(input)
- x - the wanted inputs
- y - the wanted outputs

## Network structure

---

you can create a network structure with the 'train' function in the 'structure' argument
you then pass in a tuple with the layer sizes that you want, example: (2, 6, 3)
the first and last values are the input and output size, so they have to mach the size of x and y




# Nait v2.0.4 - Change Log

---

- Added more structure control
- Added 'values' function
- Added 'sample_size' argument to the train function
- Added 'verbose' argument to the train function
- Added function documentation
- Changed display
- Removed 'layer_size' and 'layers' from the train function

---