#!/usr/bin/python

"""NUI Galway CT5132/CT5148 Programming and Tools for AI (James McDermott)

Solution for Assignment 3

By writing my name below and submitting this file, I/we declare that
all additions to the provided skeleton file are my/our own work, and that
I/we have not seen any work on this assignment by another student/group.

Student name(s):Yashitha Agarwal
Student ID(s): 20230091

GitHub Repository Link: https://github.com/yagarwal1/ARC

"""

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

def solve_c8cbb738(x):
    return x


def solve_06df4c85(x):
    return x


def solve_3631a71a(x):
    return x

def solve_0d3d703e(x):
    '''
    Difficulty: Easy
    
    [3 1 2]  =>  [4 5 6]
    [3 1 2]  =>  [4 5 6]
    [3 1 2]  =>  [4 5 6]
    
    On analysing this task manually, it is clear that the colours are mapped to each other in a straight-forward manner.
    For eg., the colour 'green (3)' always maps to 'yellow (4)' and vice-versa. Similarly, 'red (2)' and 'pink (6)' are
    mapped with each other and so on.
    
    The below program solves this task by creating a dictionary of the colours that are mapped to each other as key-value 
    pairs. Using this dictionary, the 'if-else' condition is used to check if the values of the numpy array contains the 
    elements in 'keys' (eg. green) and replaces it with its corresponding 'value' (eg. yellow) using the numpy.where() 
    function. Alternatively, if the array values are present in 'values' (eg. yellow), it is replaced by the corresponding 
    'key' (eg. green). The input array is used for checking and the replacement is done on the output array only, so that
    there are no changes to the original array.
    
    '''

    x_res = x.copy() # Create a copy of the input array, to retain the original input array
    map_dict = {1 : 5, 2 : 6, 3 : 4, 8 : 9} # Dictionary of colours that are mapped to each other

    for k, v in map_dict.items(): # Iterate over the key-value pairs (i.e 4 times) in the dictionary 
        # If value of "x" is in keys of the dictionary, all values of 'k' in "x_res" are replaced with 'v'
        # Else, all values of 'v' in "x_res" are replaced with 'k' using np.where()
        x_res = np.where(x == k, v, x_res) if np.any(x == k) else np.where(x == v, k, x_res) 

    return x_res # Return the transformed array 


def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

