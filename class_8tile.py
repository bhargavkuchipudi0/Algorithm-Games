import sys
import random
import copy
import time

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal_board = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

'''
    Class Board takes a board as an Input and its parent as reference and finds the next possible
    boards. For the intial board the parent is "root". This class has built in functions which can
    find the manhatten distance for a board.
'''


class Board:

    '''
        This is a constructor function. When ever a new board class is created this function executes
        and initialize the attributes of the class.
    '''

    def __init__(self, actual_board, parent):
        self.actual_board = actual_board
        self.parent = parent
        self.child = []

    '''
    This function will find the all possible moves in the current board and stores the moves in
    a dictionary with key as direction of the move. Iterated the possible moves and calls the
    moveBoard() function to move the tile returns the updated board. Prints the board to output
    and calls the fitness function to find the manhatten distance from current board to the goal
    board.
    board: actual board
    returns: new boards <Array>
    '''

    def nextBoards(self):
        current_position = self.getEmptySpacePosition(self.actual_board, 0)
        valid_moves = {}
        move_up = [current_position[0]-1, current_position[1]]
        if (self.checkForValidMove(move_up)):
            valid_moves['U'] = move_up
        move_down = [current_position[0]+1, current_position[1]]
        if (self.checkForValidMove(move_down)):
            valid_moves['D'] = move_down
        move_left = [current_position[0], current_position[1]-1]
        if (self.checkForValidMove(move_left)):
            valid_moves['L'] = move_left
        move_right = [current_position[0], current_position[1]+1]
        if (self.checkForValidMove(move_right)):
            valid_moves['R'] = move_right
        new_boards = []
        for key in valid_moves.keys():
            board_copy = copy.deepcopy(self.actual_board)
            tile = self.actual_board[valid_moves[key][0]][valid_moves[key][1]]
            newBoard = self.moveBoard(board_copy, tile, valid_moves[key])
            new_boards.append(newBoard)
        return new_boards

    '''
    This function finds the position of a tile or an empty space and returns the position
    back to the called function.
    board: current board
    spec_tile: tile for which position has to be find
    return: position of the given tile <Array>
    '''

    def getEmptySpacePosition(self, board, spec_tile):
        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                if tile == spec_tile:
                    return [i, j]

    '''
    This function will move the tile to the specified position and returns the updatd board to
    the called function.
    board: current board
    tile: tile to be moved
    direction: tile position
    return: board <Array<Array>>
    '''

    def moveBoard(self, board, tile, direction):
        spacePosition = self.getEmptySpacePosition(board, 0)
        board[direction[0]][direction[1]] = 0
        board[spacePosition[0]][spacePosition[1]] = tile
        return board

    '''
    This function checks weather the move is valid or not
    move: tile position
    return: Boolean
    '''

    def checkForValidMove(self, move):
        if 0 <= move[0] <= 2 and 0 <= move[1] <= 2:
            return True
        else:
            return False


'''
    This funtion prints the board with a message
    board: board(actual/goal)
    message: print message
'''


def print_board(board, message=None):
    if message:
        print(message)
    for i in board:
        print(i)


'''
    fitness function calculates the manhatten distance from the current board to the goal board.
    This function takes current board as input argument.
    '0' is the empty space in the board for which we don't calculate the distance.
    Args:    
        board: board(actual/goal)
    Returns:
        manhatten distnace
'''


def fitness(board):
    actual = {}
    goal = {}
    for i in range(len(board)):
        for j in range(len(board[0])):
            actual[board[i][j]] = [i, j]
            goal[goal_board[i][j]] = [i, j]
    md = 0
    for i in range(0, 9):
        if i != 0:
            md = md + (abs(actual[i][0] - goal[i][0]) +
                       abs(actual[i][1] - goal[i][1]))
    return md


'''
    This is a recursive function which calls its self with out exceeding the system maximum recursive calls.
    Calls the restart_hill_climbing() function. If it returns None, this function calls itself untill the solution
    is found. If found prints the solution steps, time taken to execute, and the number of recursive calls.
    Args:
        count: 0 (default) used to calculate the number of recursive calls
'''


def init_board(count=0):
    start_time = time.time()
    end_time = 0
    random.shuffle(numbers)
    actual_board = [
        [numbers[0], numbers[1], numbers[2]],
        [numbers[3], numbers[4], numbers[5]],
        [numbers[6], numbers[7], numbers[8]]
    ]
    board = Board(actual_board, "root")
    res = restart_hill_climbing(board)
    end_time = time.time()
    if not res:
        if (count < sys.getrecursionlimit() - 11):
            init_board(count + 1)
        else:
            print("------------------System maximum recursion reached------------------")
            print("Time taken for execution: {0} seconds".format(
                end_time - start_time))
            print("Number of random restarts: {0}".format(count))
            sys.exit(1)
    else:
        print("------------------Solution found------------------")
        print_board(board.actual_board, "Actual Board")
        print("Time taken for execution: {0} seconds".format(
            end_time - start_time))
        print("Number of random restarts: {0}".format(count))
        response = input("Do you want to see  the solution? (Y/N)")
        if response.lower() == 'y':
            child = board.child[0]
            move_count = 1
            print_board(child.actual_board,
                        "Next move: {0}".format(move_count))
            while child:
                move_count += 1
                time.sleep(1)
                if len(child.child) > 0:
                    child = child.child[0]
                else:
                    print("------------------Done------------------")
                    break
                print_board(child.actual_board,
                            "Next move: {0}".format(move_count))
        else:
            sys.exit(0)


'''
    This function calls the built in function of a board class to get the next possible boards and
    takes least manhatten distance from the boards and returns to the caller. If the manhatten distance
    for next boards are all greater than the current board it reutrns the current board.
    Args: 
        board: board
    Returns:
        Board <Array>
'''


def hill_climbing(board):
    min_md = 0
    cur_md = fitness(board.actual_board)
    boards = board.nextBoards()
    for i, b in enumerate(boards):
        md = fitness(b)
        if i == 0:
            min_md = md
            min_board = b
        else:
            if min_md > md:
                min_md = md
                min_board = b

    if min_md < cur_md:
        nxt_child = Board(min_board, board.actual_board)
        board.child.append(nxt_child)
        return nxt_child
    else:
        print("Solution not found!")


'''
    This function calls the hill_climbing function untill the solution board is found
    Args:
        board: board
    Returns: 
        board <Array>
'''


def restart_hill_climbing(board):
    while board.actual_board != goal_board:
        board = hill_climbing(board)
        if not board:
            return None
    else:
        return board


init_board()
