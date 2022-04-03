from fifteenPuzzleSolver import *
import time

print("/////////////////////////////////////")
print("\nPuzzle Solver for 15-Puzzle Game\n")
print("Implemented with Branch and Bound Algorithm\n")
print("Enter the initial state of the puzzle with the chosen method")
print("1. Enter the puzzle from txt file")
print("2. Enter the puzzle randomly")
print("p.s. The second method may make a really complicated puzzle")
print("p.s. If it does not work, try again or try the first method")
method = int(input("\nChosen Method : "))

if method == 1:
    print("\nEnter the name of txt file from the test folder (with extension .txt)")
    try:
        filename = input("Filename : ")
        location = "../test/" + filename
        matrix = read_matrix(location)
        print("\nPuzzle Matrix : \n")
        printMatrix(matrix)
        print("\nValue of the function Kurang(i) on each non-empty cell:\n")
        solvable = solvable(matrix)
        if solvable:
            print("\nThe puzzle is solvable")
            print("\nSteps to solve the puzzle : ")
            print("\nInitial State : ")
            printMatrix(matrix)
            start = time.time()
            solvePuzzle(matrix)
            stop = time.time()
            print("\nExecution Time = ", stop - start, "second")
            print("/////////////////////////////////////")
        else:
            print("\nSorry... The puzzle is not solvable")
            print("/////////////////////////////////////")
    except:
        print("\nSorry... The file is not found")
        print("/////////////////////////////////////")
elif method == 2:
    mat = np.arange(1,17).reshape(4,4)
    mat = np.random.permutation(mat)
    print("\nPuzzle Matrix : \n")
    printMatrix(mat)
    print("\nValue of the function Kurang(i) on each non-empty cell:\n")
    solvable = solvable(mat)
    if solvable:
        print("\nThe puzzle is solvable")
        print("\nSteps to solve the puzzle : ")
        print("\nInitial State : ")
        printMatrix(mat)
        start = time.time()
        solvePuzzle(mat)
        stop = time.time()
        print("\nExecution Time = ", stop - start, "second")
        print("/////////////////////////////////////")

    else:
        print("\nSorry... The puzzle is not solvable")
        print("/////////////////////////////////////")
else:
    print("Sorry... Wrong Input")
    print("/////////////////////////////////////")