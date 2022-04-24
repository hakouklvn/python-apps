import time


class SUDOKU:
    def __init__(self, grid):
        self.grid = grid
        self.gridSize = 9

    def drawGameBoard(self):
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                print(f"|_{self.grid[row][col]}_| ", end=" ") if (
                    (col + 1) % 3 == 0
                ) else print(f"|_{self.grid[row][col]}_|", end=" ")
            print("\n") if (row + 1) % 3 == 0 else print(" ")

    def isSafe(self, row, col, num):
        # check if num exists in row
        for column in range(self.gridSize):
            if self.grid[row][column] == num:
                return False

        # # check if num exists in col
        for r in range(self.gridSize):
            if self.grid[r][col] == num:
                return False

        # check if num exists in box
        grid_row = row - (row % 3)
        grid_col = col - (col % 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + grid_row][j + grid_col] == num:
                    return False

        return True

    def solveSudoku(self):
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if self.grid[row][col] == 0:
                    # check if its safe to put the number
                    for num in range(1, self.gridSize + 1):
                        if self.isSafe(row, col, num):
                            self.grid[row][col] = num
                            self.solveSudoku()
                            self.grid[row][col] = 0
                    return
        self.drawGameBoard()
        input("More?")

    def startGame(self):
        print(
            """
            *******************************************************************
            ****************  Welcome to the sudoku slover  *******************
            *******************************************************************
        """
        )
        user_input = input("Do you want to play the game (y/n): ")
        if user_input == "y":
            print("here it is the sudoku board that we are trying to slove")
            self.drawGameBoard()
            print("Loading the answer ...")
            time.sleep(2)
            self.solveSudoku()
            print("Thank you for trying our app")
        else:
            print("Thank you for trying our app")


# init the game
sudokuValues = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0],
]
initialzeTheGame = SUDOKU(sudokuValues)
# initialzeTheGame.isSafe(0, 0, 1)
initialzeTheGame.startGame()
