# Constraint-Satisfaction-Problem

INSTRUCTIONS
In this assignment we will focus on constraint satisfaction problems. We will be implementing the AC-3 and backtracking algorithms to solve Sudoku puzzles. The objective of the game is just to ﬁll a 9 x 9 grid with numerical digits so that each column, each row, and each of the nine 3 x 3 sub-grids (also called boxes) contains one of all of the digits 1 through 9. If you have not played the game before, you may visit sudoku.com to get a sense of how the game works.

Please read all sections of the instructions carefully.

I. Introduction
II. What we Need To build
III. AC-3 Algorithm
IV. Backtracking Algorithm
V. Important Information
VI. Before we startto build



I. Introduction
 There are 81 variables in total, i.e. the tiles to be filled with digits. Each variable is named by its row and its column, and must be assigned a value from 1 to 9, subject to the constraint that no two cells in the same row, column, or box may contain the same value.



In designing classes, you may find it helpful to represent a Sudoku board with a Python dictionary. The keys of the dictionary will be the variable names, each of which corresponds directly to a location on the board. In other words, we use the variable names Al through A9 for the top row (left to right), down to I1 through I9 for the bottom row. For example, in the example board above, we would have sudoku["B1"] = 9, and sudoku["E9"] = 8. This is the highly suggested representation, since it is easiest to frame the problem in terms of variables, domains, and constraints if you start this way. However, you can choose other data structures if you prefer. 

II. What we Need To build
Our job is to write driver.py, which intelligently solves Sudoku puzzles. Your program will be executed as follows:

$ python3 driver.py <input_string>

In the folder, you will find the file sudokus_start.txt, containing hundreds of sample Sudoku puzzles to be solved. Each Sudoku puzzle is represented as a single line of text, which starts from the top-left corner of the board, and enumerates the digits in each tile, row by row. In this assignment, we will use the number zero to indicate tiles that have not yet been filled. For example, the Sudoku board in the diagram shown above is represented as the string:

00302060090030005001001806400... (and so on)

When executed as above, replacing "<input_string>" with any valid string representation of a Sudoku board (for instance, taking any Sudoku board from sudokus_start.txt), your program will generate a file called output.txt, containing a single line of text representing the finished Sudoku board and the algorithm name (AC3 or BTS, explained later) which solved the Sudoku board. You must use a single white space as a delimiter between the board and the algorithm name. For example, output.txt looks like:

167523849984176523325489671798315264642798135531642798476831952213957486859264317 BTS

(single line, separated by a single white space)

Since this board is solved, the string representation will contain no zeros. You may test your program extensively by using sudokus_finish.txt, which contains the solved versions of all of the same puzzles.

III. AC-3 Algorithm (AC3)
First, implement the AC-3 algorithm. Test your code on the provided set of puzzles in sudokus_start.txt. To make things easier, you can write a separate wrapper script (bash, or python) to loop through all the puzzles to see if your program can solve them. As shown in sudokus_finish.txt, there are only 2/400 Sudoku boards which can be solved AC3 alone. Is this expected or unexpected?

IV. Backtracking Algorithm (BTS)
Now, implement backtracking using the minimum remaining value heuristic. The order of values to be attempted for each variable is up to you. When a variable is assigned, apply forward checking to reduce variables domains. Test your code on the provided set of puzzles in sudokus_start.txt. Can you solve all puzzles now?

V. Important Information
Please read the following information carefully. Before you post a clarifying question on the discussion board, make sure that your question is not already answered in the following sections.

1. Precedence over BTS

To check how powerful BTS is compared to AC3, you must execute AC-3 algorithm before Backtracking Search algorithm. That is, your program looks like this:

assignment = AC3(given_sudoku_board)
if (solved(assignment))
          return "<filled sudoku board>" + " AC3"
assignment = BTS(given_sudoku_board)
          return "<filled sudoku board>" + " BTS" 
