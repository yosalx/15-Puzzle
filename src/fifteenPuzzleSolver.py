import numpy as np
from heapq import heappush, heappop

# the target matrix
target_matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
# global variabel to count the number of child node generated
childNodeCount = 0

# function to read matrix from file
def read_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line.split(' ') for line in lines]
    lines = [[int(x) for x in line] for line in lines]
    return np.array(lines)

# function to find the position of a certain value in a matrix
def find_value(matrix, value):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == value: # if the value is found
                return i, j # return the row and column of the value

# function to determine the value of X based on the position of the blank cell
def x_value(matrix):
    null_row, null_col = find_value(matrix, 16) # find the position of the blank cell
    sum = null_row + null_col
    if sum % 2 == 1:
        return 1
    else:
        return 0

# function kurang(i) and the sum of it
def KURANG_I(matrix):
    sum = 0 # sum of kurang(i)
    for value in range(1,17): # for every value from 1 to 16
        row, col = find_value(matrix, value) # position of the value i
        count = 0 # the value of kurang(i)
        # function to find kurang(i) from 1 to 16
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] < value: # for every value smaller than i
                    # check whether the position of it is bigger than the position of value i
                    if row == i: # if the row of it is the same as the row of value i
                        if j > col: # if the column of it is bigger than the column of value i
                            count += 1 # increment the count
                    elif row < i: # if the row of it is smaller than the row of value i
                        count += 1 # increment the count
        sum += count # add the count to the sum
        print("Kurang(",value,") = ", count) # print the value of each kurang(i) from 1 to 16
    return sum

# function to determine whether the puzzle is solvable
def solvable(matrix):
    sum_kurang = KURANG_I(matrix) # sum of kurang(i)
    x = x_value(matrix) # value of x
    total = sum_kurang + x # sum of Sum(kurang(i)) + x
    print("\nValue of X = ", x) # print the value of x
    print("\nSum(Kurang(i)) + X = ", total) # print the sum of Kurang(i) and X
    # if the sum of Sum(Kurang(i)) and X is even, the puzzle is solvable
    if (total) % 2 == 0:
        return True
    else:
        return False

# function to find the cost of moving the blank cell (number 16)
def cost(matrix):
    cost = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # for every non-blank cell different than the supposed value in the target matrix
            if matrix[i][j] != 16:
                if matrix[i][j] != target_matrix[i][j]:
                    cost += 1 # increment the cost
    return cost

class priority_queue: # priority queue class
    def __init__(self): # const
        self.heap = []

    def push(self, value): # push the value into the heap
        heappush(self.heap, value)

    def pop(self): # pop the value from the heap
        return heappop(self.heap)

    def isEmpty(self): # check whether the heap is empty
        if not self.heap:
            return True
        else:
            return False

class Node: # node class
    def __init__(self, root, mat, blank_row, blank_col, cost, depth, prev_move): # const
        self.root = root # node root
        self.mat = mat  # the matrix of the node
        self.blank_row = blank_row # row of the blank cell in the matrix
        self.blank_col = blank_col # column of the blank cell in the matrix
        self.cost = cost # cost of the node (the cost of moving the blank cell)
        self.depth = depth # depth of the node 
        self.prev_move = prev_move # previous move to get to the node from the root

    def __lt__(self, other): # compare the cost of two nodes
        return self.cost < other.cost

def makeChildNode(node): # function to make child node
    childNode =[] # list of child node
    valid_move = [] # list of valid move
    valid_move = nextValidMove(node.blank_row,node.blank_col ,node.prev_move) # find the valid move
    for move in valid_move: # for every valid move
        # find the new position for the blank cell in the matrix
        if move == "Up": # move the blank cell up
            new_row = node.blank_row - 1
            new_col = node.blank_col
        elif move == "Down": # move the blank cell down
            new_row = node.blank_row + 1
            new_col = node.blank_col
        elif move == "Left": # move the blank cell left
            new_row = node.blank_row
            new_col = node.blank_col - 1
        elif move == "Right": # move the blank cell right
            new_row = node.blank_row
            new_col = node.blank_col + 1
        global childNodeCount # global variable to count the number of child node generated
        mat = node.mat 
        blank_row = node.blank_row
        blank_col = node.blank_col
        depth = node.depth
        
        new_mat = np.copy(mat) # copy the matrix
        save = new_mat[blank_row][blank_col] # save the value of the blank cell
        # swap the blank_cell based on the move
        new_mat[blank_row][blank_col] = new_mat[new_row][new_col]
        new_mat[new_row][new_col] = save

        # create a new node
        childNode.append(Node(node, new_mat, new_row, new_col, cost(new_mat) + depth + 1, depth+1, move))
        childNodeCount += 1 # increment the number of child node
    return childNode

def nextValidMove(blank_row, blank_col, prev_move): # function to find the valid move
    validMove = ["Up", "Down", "Left", "Right"] # list of valid move
    if blank_row == 3 or prev_move == "Up": # if the blank cell is in the last row or the previous move is up
        validMove.remove("Down") # remove down from the list of valid move
    if blank_col == 0 or prev_move == "Right": # if the blank cell is in the first column or the previous move is right
        validMove.remove("Left") # remove left from the list of valid move
    if blank_row == 0 or prev_move == "Down": # if the blank cell is in the first row or the previous move is down
        validMove.remove("Up") # remove up from the list of valid move
    if blank_col == 3 or prev_move == "Left": # if the blank cell is in the last column or the previous move is left
        validMove.remove("Right") # remove right from the list of valid move
    return validMove

def print_steps(node): # function to print the steps from the original matrix until the final matrix (same as target matrix)
    if node.root == None: # if the node is the root
        print("")
    else:
        print_steps(node.root) # print the steps from the root
        print("Move : ", node.prev_move) # print the move
        printMatrix(node.mat) # print the matrix

def printMatrix(mat): # function to print the matrix
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 16: # if the value is 16, print blank cell
                print("-", end="\t")
            else: # print the value
                print(mat[i][j], end="\t")
        print("")
    print("\n")

def solvePuzzle(mat): # function to solve the puzzle
    pq = priority_queue() # priority queue
    pq.push(Node(None, mat, find_value(mat, 16)[0], find_value(mat,16)[1], cost(mat), 0, "None")) # push the root node
    while not pq.isEmpty(): # while the priority queue is not empty
        node = pq.pop() # pop the node (the node with the lowest cost)
        if node.cost == 0 or node.cost == node.depth: # if the cost is 0 or the depth is the same as the cost
            # the puzzle is solved
            print_steps(node) # print the steps
            print("Child Node Generated = ", childNodeCount) # print the number of child node generated
            return
        else:
            childNode = makeChildNode(node) # make the child node
            for child in childNode: # for every child node
                pq.push(child) # push the child node into the priority queue
