import random


class boardSpot(object):
    def __init__(self):
        self.is_selected = False
        self.is_mine = False
        self.count = 0

    def __str__(self):
        if self.is_mine and self.is_selected:
            return "*"
        elif self.is_selected:
            return str(self.count)
        else:
            return " "

    def isMine(self):
        return self.is_mine


class boardClass(object):
    def __init__(self, boardSize, numMines):
        self.board = [[boardSpot() for i in range(boardSize)] for j in range(boardSize)]
        self.boardSize = boardSize
        self.numMines = numMines
        self.selectableSpots = boardSize * boardSize - numMines

        i = 0
        while i < numMines:
            x = random.randint(0, self.boardSize - 1)
            y = random.randint(0, self.boardSize - 1)

            if not self.board[x][y].is_mine:
                self.addMine(x, y)
                i += 1

    def __str__(self):
        returnString = " "
        divider = "\n---"

        for i in range(0, self.boardSize):
            returnString += " | " + str(i)
            divider += "----"

        divider += "\n"
        returnString += divider

        for y in range(0, self.boardSize):
            returnString += str(y)

            for x in range(0, self.boardSize):
                returnString += "|" + str(self.board[x][y])

            returnString += " |"
            returnString += divider

        return returnString

    def addMine(self, x, y):
        self.board[x][y].count = -1
        self.board[x][y].is_mine = True

        for coord_x, coord_y in self.get_neighbouring_coords_of(x, y):
            if not self.board[coord_x][coord_y].is_mine:
                self.board[coord_x][coord_y].count += 1

    def makeMove(self, x, y):
        if self.board[x][y].is_selected:
            return True

        self.board[x][y].is_selected = True
        self.selectableSpots -= 1

        if self.board[x][y].is_mine:
            return False

        if self.board[x][y].count == 0:
            for coord_x, coord_y in self.get_neighbouring_coords_of(x, y):
                if not self.board[coord_x][coord_y].is_selected:
                    self.makeMove(coord_x, coord_y)

        return True

    def hitMine(self, x, y):
        return self.board[x][y].is_mine

    def isWinner(self):
        return self.selectableSpots == 0

    def get_neighbouring_coords_of(self, x, y):
        coords = []

        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                in_range = 0 <= i < self.boardSize and 0 <= j < self.boardSize
                is_cell_itself = i == x and j == y

                if not is_cell_itself and in_range:
                    coords.append((i, j))

        return coords


def get_valid_board_size():
    while True:
        boardSize = int(input("Choose width of the board: "))

        if boardSize >= 2:
            return boardSize
        else:
            print("Board width has to be at least 2")


def get_valid_num(boardSize):
    while True:
        numMines = int(input("Choose the number of mines: "))

        if 1 <= numMines < boardSize * boardSize:
            return numMines
        else:
            print("Number has to be at least 1 and less than the space number")


def get_validMove(wholeBoard):
    while True:
        x = int(input("x: "))
        y = int(input("y: "))

        if x < 0 or x >= wholeBoard.boardSize or y < 0 or y >= wholeBoard.boardSize:
            print("Coordinates must be on the board")
        elif wholeBoard.board[x][y].is_selected:
            print("The location has previously been selected")
        else:
            return x, y


def playGame():
    boardSize = get_valid_board_size()
    numMines = get_valid_num(boardSize)

    gameOver = False
    winner = False

    wholeBoard = boardClass(boardSize, numMines)

    while not gameOver:
        print(wholeBoard)
        print("Make your move:")

        x, y = get_validMove(wholeBoard)

        wholeBoard.makeMove(x, y)
        gameOver = wholeBoard.hitMine(x, y)

        if wholeBoard.isWinner() and not gameOver:
            gameOver = True
            winner = True

    print(wholeBoard)

    if winner:
        print("Congratulations, You Win!")
    else:
        print("You hit a mine, Game Over!")


if __name__ == "__main__":
    playGame()