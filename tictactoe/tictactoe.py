
"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # X always begins the game
    # So in every round O will either have lesser or equal moves as X
    # If O has lesser moves , It is O's turn.
    # If X and O have equal moves, the round is over it is X's turn.

    x_moves = 0
    o_moves = 0

    # checking the number of counts of X and O based on their occurence column by column
    for column in board:

        x_moves += column.count('X')
        o_moves += column.count('O')

    # if equal moves X's chance else O's chance
    if x_moves != o_moves:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    '''A possible action can only be taken if the block is empty
       as there can be no overlapping values'''

    # If all blocks are filled there is no possible actions that may be taken

    # A set prescribed by CS50AI to store probable actions

    future_actions = set()

    # scanning the entire (3 X 3) board to scan empty blocks

    for row in range(0, 3):

        for column in range(0, 3):

            # if the block has no value it is empty hence a possible action
            if board[row][column] == None:

                # added in the form of a tuple
                future_actions.add((row, column))

    # returning the possible actions after scanning the board
    return future_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # incase an action is invalid for the board

    # if the action made is not under the possible actions for that particular board
    # we raise an exception

    if action not in actions(board):

        raise Exception("Not a possible action for current board")

    # making a deepcopy to prevent losing the original board
    updated_board = copy.deepcopy(board)

    # unpacking two variables under action, [ row = action[0] ; column = action[1] ]
    row, column = action

    '''
    above unpacking could also be done in a simpler way
    row = action[0]
    column = action[1]
    '''

    # adding action to board and returning the result to the function
    updated_board[row][column] = player(board)
    return updated_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # checking rows with a three spree

    # checking three rows with the column changing every comparision
    # checking three rows with the row changing each iteration
    for row in range(0, 3):

        if (board[row][0] == board[row][1] == board[row][2] != None):
            return board[row][0]

    # checking columns with a three spree
    # checking three columns with the rows changing every comparision
    # checking three columns with the column changing each iteration

    for column in range(0, 3):

        if (board[0][column] == board[1][column] == board[2][column] != None):
            return board[0][column]

    # checking diagonals with three spree
    # 2 possible diagonals

    # diagonal starting from the left corner
    if (board[0][0] == board[1][1] == board[2][2] != None):
        return board[0][0]

    # diagonal starting from the right corner
    if (board[0][2] == board[1][1] == board[2][0] != None):
        return board[0][2]

    # if no spree in a row, column or diagonal
    # returns None as game might be processing or might be a tie

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # checking if there is a winner to the tic tac toe game
    if winner(board) == None:

        # in case of None , it might be because game is still in progress
        for row in board:

            for i in row:

                # if block is still empty
                # we confirm the game is under progress
                # returns False

                if i == None:

                    return False

    # either winner or a tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # 1 for X winning
    if winner(board) == X:
        return 1

    # -1 for O winning
    elif winner(board) == O:
        return -1

    # 0 for a draw or tie
    else:
        return 0


def u_value(state):
    """
    Returns utility value if an optimal action is played for the current player on the board.
    """
    # if there is a tie or winner
    if terminal(state) == True:
        return utility(state)

    # if game is in progress

    # if it is max players move(X)
    if player(state) == X:

        # setting function to max
        minmax_f = max
        # setting comparision value to negative infinity
        # to always achieve max value
        val = - math.inf

    else:
        # when it is min players move(O)

        # setting comparision value to positive infinity
        # to always achieve min value
        minmax_f = min
        val = math.inf

    for action in actions(state):
        val = minmax_f(val, u_value(result(state, action)))
    return val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if there is a winner or tie
    # when the game ends, no more possible moves
    # Hence return none after winning or tie
    if terminal(board) == True:
        return None

    # when terminal board is False
    # when game is in progress
    # analyse every action on board
    for action in actions(board):

        # if the move to be returned is an optimal function
        # and if the move is possible on the current state of board
        # return move

        '''
        u_value(result(board, action) - checking the optimal value
        returned by the updated board when the action is executed
        '''
        # checking if that is the most optimal move for current board too
        if u_value(board) == u_value(result(board, action)):
            return action
