# The Abstraction and Reasoning Corpus (ARC)

This repository contains the ARC task data, as well as a browser-based interface for humans to try their hand at solving the tasks manually.

*"ARC can be seen as a general artificial intelligence benchmark, as a program synthesis benchmark, or as a psychometric intelligence test. It is targeted at both humans and artificially intelligent systems that aim at emulating a human-like form of general fluid intelligence."*

A complete description of the dataset, its goals, and its underlying logic, can be found in: [The Measure of Intelligence](https://arxiv.org/abs/1911.01547).

As a reminder, a test-taker is said to solve a task when, upon seeing the task for the first time, they are able to produce the correct output grid for *all* test inputs in the task (this includes picking the dimensions of the output grid). For each test input, the test-taker is allowed 3 trials (this holds for all test-takers, either humans or AI).


## Task file format

The `data` directory contains two subdirectories:

- `data/training`: contains the task files for training (400 tasks). Use these to prototype your algorithm or to train your algorithm to acquire ARC-relevant cognitive priors.
- `data/evaluation`: contains the task files for evaluation (400 tasks). Use these to evaluate your final algorithm. To ensure fair evaluation results, do not leak information from the evaluation set into your algorithm (e.g. by looking at the evaluation tasks yourself during development, or by repeatedly modifying an algorithm while using its evaluation score as feedback).

The tasks are stored in JSON format. Each task JSON file contains a dictionary with two fields:

- `"train"`: demonstration input/output pairs. It is a list of "pairs" (typically 3 pairs).
- `"test"`: test input/output pairs. It is a list of "pairs" (typically 1 pair).

A "pair" is a dictionary with two fields:

- `"input"`: the input "grid" for the pair.
- `"output"`: the output "grid" for the pair.

A "grid" is a rectangular matrix (list of lists) of integers between 0 and 9 (inclusive). The smallest possible grid size is 1x1 and the largest is 30x30.

When looking at a task, a test-taker has access to inputs & outputs of the demonstration pairs, plus the input(s) of the test pair(s). The goal is to construct the output grid(s) corresponding to the test input grid(s), using 3 trials for each test input. "Constructing the output grid" involves picking the height and width of the output grid, then filling each cell in the grid with a symbol (integer between 0 and 9, which are visualized as colors). Only *exact* solutions (all cells match the expected answer) can be said to be correct.


## Usage of the testing interface

The testing interface is located at `apps/testing_interface.html`. Open it in a web browser (Chrome recommended). It will prompt you to select a task JSON file.

After loading a task, you will enter the test space, which looks like this:

![test space](https://arc-benchmark.s3.amazonaws.com/figs/arc_test_space.png)

On the left, you will see the input/output pairs demonstrating the nature of the task. In the middle, you will see the current test input grid. On the right, you will see the controls you can use to construct the corresponding output grid.

You have access to the following tools:

### Grid controls

- Resize: input a grid size (e.g. "10x20" or "4x4") and click "Resize". This preserves existing grid content (in the top left corner).
- Copy from input: copy the input grid to the output grid. This is useful for tasks where the output consists of some modification of the input.
- Reset grid: fill the grid with 0s.

### Symbol controls

- Edit: select a color (symbol) from the color picking bar, then click on a cell to set its color.
- Select: click and drag on either the output grid or the input grid to select cells.
    - After selecting cells on the output grid, you can select a color from the color picking to set the color of the selected cells. This is useful to draw solid rectangles or lines.
    - After selecting cells on either the input grid or the output grid, you can press C to copy their content. After copying, you can select a cell on the output grid and press "V" to paste the copied content. You should select the cell in the top left corner of the zone you want to paste into.
- Floodfill: click on a cell from the output grid to color all connected cells to the selected color. "Connected cells" are contiguous cells with the same color.

### Answer validation

When your output grid is ready, click the green "Submit!" button to check your answer. We do not enforce the 3-trials rule.

After you've obtained the correct answer for the current test input grid, you can switch to the next test input grid for the task using the "Next test input" button (if there is any available; most tasks only have one test input).

When you're done with a task, use the "load task" button to open a new task.

## Purpose of repository

This repository has been primarily used for solving the below tasks using task specific programs that have been hand-coded. In all the solutions, numpy functions have been extremely useful in working with the given data. For the purpose of this assignment, I have chosen 5 tasks of varying difficulty levels. All the solutions are available in `src/manual_solve.py` with one `"solve_<ID>"` function to solve each task.

### Task 1: `solve_c8cbb738`

In this task, the dimensions of the output array depends on the sub-sets of arrays present in the input grid. Based on the different coloured sub-sets, we need to identify the dimension of the output grid. After selecting the correct output grid dimensions, all the different coloured sub-sets have to be superimposed together in the proper order to form the output grid.

![test space](https://github.com/yagarwal1/ARC/blob/Development/apps/img/Task_1.PNG)

### Task 2: `solve_06df4c85`

For this task, the input grids have black squares (2 x 2) and few coloured squares (2 x 2) of different colours with a common border colour (eg. yellow in the below image). The goal is to identify pairs of same colored squares which are present on the same row (or) column, and replace the black squares between those pairs of coloured squares with the same colour. An important point to note in the image below is that, the red square on the top right should not be joined to the horizontal red grids as they are not present in the initial input array.

![test space](https://github.com/yagarwal1/ARC/blob/Development/apps/img/Task_2.PNG)

### Task 3: `solve_ded97339`

This task is almost similar to task 2, in the sense that the code uses the same logic with a few tweaks in the function. As opposed to the previous task, all the grids in this task have only two colours - black and blue. Therefore, it is a little simpler in comparison to the previous task, as the squares are (1 x 1), have no borders and have only two colours. We need to find the pairs of blue squares on any row or column and join the pair of blue squares by replacing the black squares between them. 

![test space](https://github.com/yagarwal1/ARC/blob/Development/apps/img/Task_3.PNG)

### Task 4: `solve_3631a71a`

An interesting task, which involved more thinking to simplify the logic and optimise the code, this essentially requires all the maroon (number 9) coloured squares to be replaced by the correct coloured square. The trick here is that the grid seems to be symmetrical, while it actually has two extra rows and columns on the top and left respectively, which are not present on their opposite side. However, every corresponding row and column has equal values (eg. r[0] == c[0]), making it symmetrical across the diagonal.

![test space](https://github.com/yagarwal1/ARC/blob/Development/apps/img/Task_4.PNG)

### Task 5: `solve_0d3d703e`

The easiest of the five tasks, this one has a pretty straight-forward logic. It has four pairs of colours that are mapped to each other - (green <=> yellow), (indigo <=> grey), (red <=> pink) and (blue <=> maroon). The aim is to map each colour in the input grid to its pair.

![test space](https://github.com/yagarwal1/ARC/blob/Development/apps/img/Task_5.PNG)

## Summary

All the tasks have been solved using the hand-coded python functions, which are task-specific. Each function has a single task-specific logic which has been used to successfully solve all the training and test grids. NumPy library has been used in the code as it makes working with arrays much easier and simpler. The functions for all the tasks make use of various numpy functions, such as numpy.where(), numpy.transpose() and numpy.unique(). Among the many numpy functions used, I believe numpy.where() has been used the most throughout the entire program. Also, numpy.transpose() was a highly useful function as it outputs a view of the original array. This makes it extremely easy to work with transposed matrices without the hassles of re-transposing the matrix as all the changes made to the transposed matrix are duplicated to the original matrix. Apart from the NumPy functions, Python features like list comprehensions and single-line 'for', 'if' loops have also been used throughout the program. 

The Abstraction and Reasoning Corpus has a vast variety of tasks with varied levels of difficulty. Most of the tasks work by finding and replacing certain cells of the grid or certain indices of the cells. Also, there are a few tasks which follow the same logic, with a slight difference. For instance, tasks 2 and 3 explained above share the same high-level logic, which means that if an AI agent is trained on a set of high-level logics and also on techniques of tweaking the code to try different combinations, to use ARC as a benchmark for comparing general intelligence betwen AI systems and humans.
