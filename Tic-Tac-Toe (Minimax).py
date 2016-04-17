"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    status = board.check_win()
    if status != None:
        return SCORES[status], (-1, -1)
    else:
        empty_squares = board.get_empty_squares()
        min_rival_score = 1
        min_rival_move = (-1, -1)
        for square in empty_squares:
            board_temp =  board.clone()
            board_temp.move(square[0], square[1], player)
            if player == provided.PLAYERO:
                rival_mm = mm_move(board_temp, provided.switch_player(player))
            else:
                temp = mm_move(board_temp, provided.switch_player(player))
                rival_mm = (-temp[0], temp[1])    
            if rival_mm[0] == -1:
                return (-1, square) if player == provided.PLAYERO else (1, square)
            elif rival_mm[0] <= min_rival_score:
                min_rival_score = rival_mm[0]
                min_rival_move = square
        return (-min_rival_score, min_rival_move) if player == provided.PLAYERO else (min_rival_score, min_rival_move)


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#
#board = provided.TTTBoard(2, False, 
#                          [[provided.EMPTY, provided.EMPTY], 
#                           [provided.EMPTY, provided.EMPTY]])
#board_u = provided.TTTBoard(2, False, 
#                              [[provided.PLAYERX, provided.EMPTY], 
#                               [provided.PLAYERO, provided.EMPTY]])
#board_x = provided.TTTBoard(2, False, 
#                              [[provided.PLAYERX, provided.EMPTY], 
#                               [provided.PLAYERO, provided.PLAYERX]])
#board_3 = provided.TTTBoard(3, False, 
#                  [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], 
#                   [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], 
#                   [provided.EMPTY, provided.PLAYERX, provided.EMPTY]])

#print board
#print board.move(0, 0, provided.PLAYERX)
#print SCORES
#print board_u.check_win()
#print board_x.check_win()
#print board_u.get_empty_squares()


#import poc_simpletest
#
#def run_suite(function):
#    """
#    test the functions
#    """
#    board_e = provided.TTTBoard(2, False, 
#                          [[provided.EMPTY, provided.EMPTY], 
#                           [provided.EMPTY, provided.EMPTY]])
#    board_x = provided.TTTBoard(2, False, 
#                              [[provided.PLAYERX, provided.EMPTY], 
#                               [provided.PLAYERO, provided.PLAYERX]])
#    board_u = provided.TTTBoard(2, False, 
#                              [[provided.PLAYERX, provided.EMPTY], 
#                               [provided.PLAYERO, provided.EMPTY]])
#    board_3 = provided.TTTBoard(3, False, 
#                  [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], 
#                   [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], 
#                   [provided.PLAYERO, provided.PLAYERX, provided.EMPTY]])
#
#    
#    suite = poc_simpletest.TestSuite()
#    
#    suite.run_test(function(board_x, provided.PLAYERX), 
#                   (1, (-1, -1)), 'X wins')
#    suite.run_test(function(board_u, provided.PLAYERX), 
#                   (1, (0, 1)), 'x wins')
#    suite.run_test(function(board_u, provided.PLAYERO), 
#                   (-1, (0, 1)), 'o wins')
#    suite.run_test(function(board_3, provided.PLAYERX), 
#                   (0, (-1, -1)), 'o wins')
#    
#    suite.report_results()
#
#run_suite(mm_move)