# Predictioner (Module)
Predictioner (Module) is the module of the program Predictioner, which allows you to predict the next terms of a given sequence.

## Installation
First, you need to install the module:
```python
# For Windows users
pip install predictioner
# For Unix users
sudo pip3 install predictioner
```

## Initialization
Then, you need to import the module:
```python
import predictioner
```

## Predict
Then, you can start to predict sequences:
```python
predictioner.predict([your_sequence], number_of_seps, verbose)
```
Where
 - your_sequence = the array of the sequence (ex. [2, 4, 6])
 - number_of_steps = the number of times you want the program to go forward predicting the sequence (ex. 3)
 - verbose = (boolean) do you want to show all steps or only the last one? (ex. True)