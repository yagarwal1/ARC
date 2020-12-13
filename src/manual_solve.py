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
    '''
    Difficulty: Difficult
    
    On analysing this task using the manual ARC testing interface, it can be seen that each input grid has a sub set of
    n-dimensional grids, having 4 colour values each, that need to be superimposed together to generate the required 
    (n x n) output grid. To achieve this, first the unique colours are obtained by fetching the counts of all the unique
    numbers (colours) in the numpy array, and selecting the colours with the count of 4. Then, the dimension of the
    output grid needs to be calculated, which can be done as follows:
    
    number of rows (or) columns of unique colours = maximum(colour_index) - minimum(colour_index), 
    for all the above unique colours (i.e count = 4)
    
    output array dimension, n = maximum(number of rows (or) columns of unique colours)
    
    The maximum of the difference between the maximum and minimum values of the number of rows/columns among all the 
    colours (sub set matrices) in the given input grid, gives the dimension for the output array. The background colour 
    can be obtained by fetching the unique colour with highest count. With the dimension and the background colour,
    a n X n base matrix with values of the background colour can be generated with the np.full() function.  
    
    Now, the np.where() function can be used to modify the output matrix based on the if-elif-else condition. For sub
    sets that have a shape different from shape of the output matrix, the start and end rows where the sub set should be
    merged on the output matrix should be specified. This is done using the function 'replace_colour' with the logic to 
    find the start row index by dividing the number of rows of the output array and the sub set array. The end row index
    is calculated by adding the start row index with the number of rows in the sub set array. For eg., if the output array 
    is a 7 x 7 matrix and the subset is 3 x 7, then start row is (7 // 3) which is 2, and end row is (2 + 3) = 5. If the 
    column value of sub set is less than the column value of the output matrix, the matrices are transposed before being 
    passed to the 'replace_colour' function to perform the same logic outlined above.
        
    '''

    (unique, counts) = np.unique(x, return_counts=True) # Fetch the unique colours and their count as a tuple
    colours = unique[counts == 4] # Unique colours except the background

    res_dim = max([(max(np.where(x == c)[0]) - min(np.where(x == c)[0])) for c in colours]) + 1 # Output array dimension
    x_res = np.full((res_dim, res_dim), unique[np.argmax(counts)]) # Output matrix with the background colour filled

    # Function to modify the output array when the shape of output array is different from the shape of subset array
    def replace_colour(original_array, result_array):
        s_row = min(result_array.shape) // min(original_array.shape) # Starting row index to be modified - for output array
        e_row = s_row + min(original_array.shape) # Ending row index to be modified - for output array
        result_array[s_row:e_row,:] = np.where(original_array == c, c, result_array[s_row:e_row,:]) # Modifying the output array
        # Note that values are only changed in the output array and the input array remains unchangedS

    for c in colours: # For each unique colour
        (rows, cols) = np.where(x == c) # Row and column indices for the colour c
        each_colour = x[min(rows):(max(rows) + 1),min(cols):(max(cols) + 1)] # Slicing the array based on row and col index

        if each_colour.shape[0] < x_res.shape[0]: # No. of rows in colour subset < No. of rows in output array
            replace_colour(each_colour, x_res) # Passing the subset and output array to 'replace_colour' function
        elif each_colour.shape[1] < x_res.shape[1]: # No. of cols in colour subset < No. of cols in output array
            t_each_colour = np.transpose(each_colour) # Transpose of the subset array
            t_x_res = np.transpose(x_res) # Transpose of the output array
            replace_colour(t_each_colour, t_x_res) # Passing the transposed arrays to 'replace_colour' function
        else:
            x_res = np.where(each_colour == c, c, x_res) # Modifying the output array when both arrays have the same shape
            
    return x_res # Return the transformed array 


def solve_06df4c85(x):
    return x


def solve_3631a71a(x):
    '''
    Difficulty: Medium-to-difficult
    
    Using the ARC testing interface, two important observations can be made for this task:
    1. The input grids are symmetrical, except for the first two ([0] and [1]) rows and columns
    2. In the input grid, the colour represented by the value '9' needs to be replaced with the correct value to generate 
       the output grid
    
    On further analysis, for all the train and test input grids, it can be seen that any empty values (i.e '9') in the 
    first two rows/columns can be replaced by the value in the corresponding column/row. For instance, assuming the value 
    in index x[i, j] is '9', it can be replaced by the value in index x[j, i]. 
    
    The above logic can also be applied to most of the empty values ('9') in the rest of the rows and columns -> x[2:, 2:],
    provided that the value in x[j, i] is not equal to '9'. In case x[j, i] is also '9', then the correct value can be 
    obtained from either the horrizontal or vertical mirror value (as they are symmetrical), by taking the row or column 
    index value in reverse.
    
    The horizontal and vertical mirror values for any index is obtained by subtracting 1 from the original row or column 
    index respectively, as this fetches the index in reverse. For eg. the mirror value for x[5, 14] would be x[5, 17] which
    is the same as x[5, -13].
    
    '''
    
    x_res = x.copy() # Create a copy of the input array, to retain the original input array
    rows, cols = np.where(x == 9) # Get the list of indices whose values need to be replaced (i.e) x == 9
    for i, j in zip(rows, cols):
        # If x[j, i] is not 9, replace x_res[i, j] with x[j, i]
        # Else if the horizontal mirror value is not 9, replace x_res[i, j] with x[i, 1 - j]
        # Else replace x_res[i, j] with the vertical mirror value, which is x[1 - i, j]
        x_res[i, j] = x[j, i] if x[j, i] != 9 else (x[i, 1 - j] if x[i, 1 - j] != 9 else x[1 - i, j])  
    
    return x_res


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

