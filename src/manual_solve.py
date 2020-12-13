#!/usr/bin/python

"""
NUI Galway CT5132 Programming and Tools for AI (James McDermott)

Solution for Assignment 3

By writing my name below and submitting this file, I/we declare that
all additions to the provided skeleton file are my/our own work, and that
I/we have not seen any work on this assignment by another student/group.

Student name(s):Yashitha Agarwal
Student ID(s): 20230091

GitHub Repository Link: https://github.com/yagarwal1/ARC

Please find the updated README.md in the above repository link

Contents added in README.md: Purpose of repository, Task description, Summary

NB: The summary has been added at the end of this file as well

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
    
    On analysing this task using the manual ARC testing interface, it can be seen that each input grid has a sub-set of
    n-dimensional grids, having 4 colour values each, that need to be superimposed together to generate the required 
    (n x n) output grid. To achieve this, first the unique colours are obtained by fetching the counts of all the unique
    numbers (colours) in the numpy array, and selecting the colours with a count of 4. Then, the dimension of the
    output grid needs to be calculated, which can be done as follows:
    
    number of rows (or) columns of unique colours = maximum(colour_index) - minimum(colour_index), 
    for all the above unique colours (i.e count = 4)
    
    output array dimension, n = maximum(number of rows (or) columns of all unique colours)
    
    The maximum of the difference between the maximum and minimum values of the number of rows/columns among all the 
    colours (sub-set matrices) in the given input grid, gives the dimension for the output array. The background colour 
    can be obtained by fetching the unique colour with highest count. With the dimension and the background colour,
    a (n X n) base matrix with values of the background colour can be generated with the np.full() function.  
    
    Now, the np.where() function can be used to modify the output matrix based on the 'if-elif-else' condition. For sub-
    sets that have a shape different from shape of the output matrix, the starting and ending indices where the sub-set 
    should be merged on the output matrix should be specified. This is done using the function 'replace_colour()' with the 
    logic to find the start row index by dividing the number of rows of the output array and the sub-set array. The end row 
    index is calculated by adding the start row index with the number of rows in the sub-set array. For eg., if the output 
    array is a 7 x 7 matrix and the sub-set is 3 x 7, then start row index is (7 // 3) which is 2, and end row is (2 + 3) 
    = 5. If the column value of sub-set is less than the column value of the output matrix, the matrices are transposed 
    before being passed to the 'replace_colour' function to perform the same logic outlined above.

    All the training and test sets have been solved successfully using this algorithm.
        
    '''

    (unique, counts) = np.unique(x, return_counts=True) # Fetch the unique colours and their count as a tuple
    colours = unique[counts == 4] # Unique colours except the background

    res_dim = max([(max(np.where(x == c)[0]) - min(np.where(x == c)[0])) for c in colours]) + 1 # Output array dimension
    x_res = np.full((res_dim, res_dim), unique[np.argmax(counts)]) # Output matrix with the background colour filled

    # Function to modify the output array when the shape of output array is different from the shape of sub-set array
    def replace_colour(original_array, result_array):
        s_row = min(result_array.shape) // min(original_array.shape) # Starting row index to be modified - for output array
        e_row = s_row + min(original_array.shape) # Ending row index to be modified - for output array
        result_array[s_row:e_row,:] = np.where(original_array == c, c, result_array[s_row:e_row,:]) # Modifying output array
        # Note that values are only changed in the output array and the input array remains unchanged

    for c in colours: # For each unique colour
        (rows, cols) = np.where(x == c) # Row and column indices for the colour c
        each_colour = x[min(rows):(max(rows) + 1),min(cols):(max(cols) + 1)] # Slicing the array based on row and col index

        if each_colour.shape[0] < x_res.shape[0]: # No. of 'rows' in colour sub-set < No. of 'rows' in output array
            replace_colour(each_colour, x_res) # Passing the sub-set and output array to 'replace_colour()' function
            
        elif each_colour.shape[1] < x_res.shape[1]: # No. of 'cols' in colour sub-set < No. of 'cols' in output array
            t_each_colour = np.transpose(each_colour) # Transpose of the sub-set array
            t_x_res = np.transpose(x_res) # Transpose of the output array
            replace_colour(t_each_colour, t_x_res) # Passing the transposed arrays to 'replace_colour()' function
            # Note that np.transpose() only passes a transposed view of the matrix. Therefore, the changes made to t_x_res
            # is also applied to x_res, and so there is no need to re-transpose the matrix (t_x_res) to the original form
            
        else:
            x_res = np.where(each_colour == c, c, x_res) # Modifying the output array when both arrays have the same shape
            
    return x_res # Return the transformed array 


def solve_06df4c85(x):

    '''
    Difficulty: Medium-to-difficult
    
    This task has 2 consecutive rows or columns of colour values that need to be filled, if and only if there are 2 other 
    consecutive values of the same colour on the particular row or column. The colour should be filled row-wise and column-
    wise. For doing this, the 'fill_colour()' function is used to first check the row-wise values and then the same function
    is used to check the column-wise values by passing the transposed arrays.
    
    First, the unique colours available in the input grid are fetched using the np.unique() method. The unique colour values,
    along with the input array and the output array are passed to the 'fill_colour()' function. This function traverses each
    row of the input and output arrays, for each unique colour value in the input grid. For each row, if a unique colour value 
    is present exactly 4 times, then ONLY black ('0') values present between the four colour value indices are replaced with the
    'colour's value'. The input array is only used to check the conditions and the modifications are made in the output array. 
    This helps in avoiding filling the vertical column in the third 'training' set.
    
    For eg., in a row [0 0 4 0 0 4 2 2 4 0 0 4 0 0 4 0 0 4 2 2 4 0 0 4 0 0], there are exactly four 2's and only the 0's between
    the 2's need to be filled

    All the training and test sets have been solved successfully using this algorithm.

    '''
    
    x_res = x.copy() # Create a copy of the input array, to retain the original input array
    t_x = np.transpose(x) # Transpose of the input array
    t_x_res = np.transpose(x_res) # Transpose of the output array
    unique = np.unique(x) # Unique colours (numbers) in the input grid
    
    # Function to fill colour by traversing the given input and output matrices row-wise
    def fill_colour(unique, input_array, output_array):
        for row, x_row in zip(input_array, output_array): # For each row in the input and output matrix
            for u in unique: # Iterating over each colour in the input grid
                if np.count_nonzero(row == u) == 4: # If the count of the unique colour is exactly equal to 4
                    u_ind = np.where(row == u)[0] # Indices of the particular colour
                    b_ind = np.where(row == 0)[0] # Indices of black in the particular row
                    # Indices of black which lie between the indices of the given unique colour's indices
                    r_ind = np.array([b_i for b_i in b_ind if b_i > u_ind[1] and b_i < u_ind[2]])
                    np.put(x_row, r_ind, u) # Using np.put() method to modify ONLY the value of 0's to the given colour
                    # Note that values are only changed in the output array and the input array remains unchanged
                    
    fill_colour(unique, x, x_res) # Passing the unique colours, input and output arrays to 'fill_colour()'
    fill_colour(unique, t_x, t_x_res) # Passing the unique colours, transposed input and output arrays to 'fill_colour()'
    # Note that np.transpose() only passes a transposed view of the matrix. Therefore, the changes made to t_x_res
    # is also applied to x_res, and so there is no need to re-transpose the matrix (t_x_res) to the original form
    
    return x_res # Return the transformed array


def solve_ded97339(x):

    '''
    Difficulty: Medium-to-difficult
    
    Similar to the above task, this one also follows almost the same logic with the only difference that, here black
    cells between 2 blue cells on the same row/column needs to be filled. As with the previous task, the colour should be 
    filled row-wise and column-wise. For doing this, a modified version of the 'fill_colour()' function is used to first 
    check the row-wise values and the column-wise values by passing the transposed arrays.
    
    The input array and the output array are passed to the 'fill_colour()' function. This function traverses each row of
    the input and output arrays, to check blue colour (non-zero since the input grid has only 2 colours - blue and black
    ('0')) is present exactly 2 times. In the rows that have exactly 2 blue colour values, the indices of the blue cells  
    are taken as the start and end values and the 0's between those indices are replaced.
    
    For eg., in a row [0 0 8 0 0 0 0 8 0 0 0 0], there are exactly two 8's and all the 0's between the 8's need to be 
    replaced with 8.
    
    All the training and test sets have been solved successfully using this algorithm.
    
    '''

    x_res = x.copy() # Create a copy of the input array, to retain the original input array
    t_x = np.transpose(x) # Transpose of the input array
    t_x_res = np.transpose(x_res) # Transpose of the output array
    
    # Function to fill colour by traversing the given input and output matrices row-wise
    def fill_colour(input_array, output_array):        
        for row, x_row in zip(input_array, output_array): # For each row in the input and output matrix
            # If count of blue colour (i.e non-zero values since black = '0') is exactly equal to 2
            if np.count_nonzero(row) == 2: 
                (start, end) = np.where(row == 8)[0] # Indices of start and end of blue colour ('8')
                # The value of blue colour ('8') is hardcoded as it is the only number in the grid apart from black
                x_row[start: end] = np.where(row[start: end] == 0, 8, x_row[start: end]) 
                # Note that values are only changed in the output array and the input array remains unchanged

    fill_colour(x, x_res) # Passing the input and output arrays to 'fill_colour()'
    fill_colour(t_x, t_x_res) # Passing the unique colours, transposed input and output arrays to 'fill_colour()'
    # Note that np.transpose() only passes a transposed view of the matrix. Therefore, the changes made to t_x_res
    # is also applied to x_res, and so there is no need to re-transpose the matrix (t_x_res) to the original form
    
    return x_res # Return the transformed array 


def solve_3631a71a(x):
    
    '''
    Difficulty: Medium-to-difficult
    
    Using the ARC testing interface, two important observations can be made for this task:
    1. The input grids are symmetrical, except for the first two (indices [0] and [1]) rows and columns
    2. In the input grid, the colour represented by the value '9' needs to be replaced with the correct value to generate 
       the output grid
    
    On further analysis, for all the train and test input grids, it can be seen that any empty values (i.e '9') in the 
    first two rows/columns can be replaced by the value in the corresponding column/row. For instance, assuming the value 
    in index x[i, j] is '9', it can be replaced by the value in index x[j, i]. 
    
    The above logic can also be applied to most of the empty values ('9') in the rest of the rows and columns -> x[2:, 2:],
    provided that the value in x[j, i] is not equal to '9'. In case x[j, i] is also '9', then the correct value can be 
    obtained from either the horizontal or vertical mirror value (as they are symmetrical), by taking the row or column 
    index value in reverse.    
    
    The horizontal and vertical mirror values for any index is obtained by subtracting 1 from the original row or column 
    index respectively, as this fetches the index in reverse. For eg. the mirror value for x[5, 14] would be x[5, 17] which
    is the same as x[5, -13].
    
    All the training and test sets have been solved successfully using this algorithm.
    
    '''
    
    x_res = x.copy() # Create a copy of the input array, to retain the original input array
    rows, cols = np.where(x == 9) # Get the list of indices whose values need to be replaced (i.e) x == 9

    for i, j in zip(rows, cols):
        # If x[j, i] is not 9, replace x_res[i, j] with x[j, i]
        # Else if the vertical mirror value is not 9, replace x_res[i, j] with x[i, 1 - j]
        # Else replace x_res[i, j] with the horizontal mirror value, which is x[1 - i, j]
        x_res[i, j] = x[j, i] if x[j, i] != 9 else (x[i, 1 - j] if x[i, 1 - j] != 9 else x[1 - i, j])  
    
    return x_res # Return the transformed array 


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
    
    All the training and test sets have been solved successfully using this algorithm.
    
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

"""
SUMMARY:

All the tasks have been solved using the hand-coded python functions, which are task specific. Each function has a single 
task-specific logic which has been used to successfully solve all the training and test grids. NumPy library has been used 
in the code as it makes working with arrays much easier and simpler. The functions for all the tasks make use of various 
numpy functions, such as numpy.where(), numpy.transpose() and numpy.unique(). Among the many numpy functions used, I 
believe numpy.where() has been used the most throughout the entire program. Also, numpy.transpose() was a highly useful 
function as it outputs a view of the original array. This makes it extremely easy to work with transposed matrices without 
the hassles of re-transposing the matrix as all the changes made to the transposed matrix are duplicated to the original 
matrix. Apart from the NumPy functions, Python features like list comprehensions and single-line 'for', 'if' loops have 
also been used throughout the program. 

The Abstraction and Reasoning Corpus has a vast variety of tasks with varied levels of difficulty. Most of the tasks work 
by finding and replacing certain cells of the grid or certain indices of the cells. Also, there are a few tasks which 
follow the same logic, with a slight difference. For instance, tasks 2 and 3 explained above share the same high-level 
logic, which means that if an AI agent is trained on a set of high-level logics and also on techniques of tweaking the 
code to try different combinations, to use ARC as a benchmark for comparing general intelligence betwen AI systems and 
humans.

"""

if __name__ == "__main__": main()