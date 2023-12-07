# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:04:14 2023

@author: Fergut4
"""
import time
import chess
import random

def legal_moves(board):
    legal_moves = board.legal_moves
    legal_moves = str(legal_moves)
    legal_moves = legal_moves.split('(')
    legal_moves.pop(0)
    legal_moves = legal_moves[0].split(',')
    legal_moves[-1] = legal_moves[-1].replace(')>','')
    numbs = []
    for x in range(len(legal_moves)):
        legal_moves[x] = legal_moves[x].strip()
        if legal_moves[x] == '':
            numbs.append(x)
    for x in numbs:
        legal_moves.pop(x)
        map(lambda x : x - 1, numbs)
    return legal_moves



def white_rating(board,turn):
    #Below about how close to edge king is
    #Only good in early game
    rating = 0
    piece_points = 0 
    
    #King Safety
    if turn > 4 and turn <= 25:
        if chess.square_manhattan_distance(board.king(chess.Color(True)),chess.B1) < chess.square_manhattan_distance(board.king(chess.Color(True)),chess.G1):
            rating -= chess.square_manhattan_distance(board.king(chess.Color(True)),chess.B1)
        else:
            rating -= chess.square_manhattan_distance(board.king(chess.Color(True)),chess.G1)
    
    #Points for all pieces remaining
    for y in board.pieces(chess.PAWN,chess.WHITE):
        piece_points += 1 
    for y in board.pieces(chess.ROOK,chess.WHITE):
        piece_points += 5
    for y in board.pieces(chess.BISHOP, chess.WHITE):
        piece_points += 3
    for y in board.pieces(chess.KNIGHT, chess.WHITE):
        piece_points += 2.9
    for y in board.pieces(chess.QUEEN, chess.WHITE):
        piece_points += 9
    rating += piece_points
    if (chess.square_knight_distance(chess.KNIGHT, chess.E4) < 2 or chess.square_knight_distance(chess.KNIGHT, chess.D4) < 2) and board.attackers(chess.BLACK, chess.E4) < board.attackers(chess.WHITE, chess.E4):
        rating += 3
    
    if board.is_check():
        rating -= 0.5
    
    #print(board.piece_type_at(chess.E4))
    #checks for center control via any pieces
    if board.color_at(chess.E4) == chess.WHITE:
        rating+=2
    if board.color_at(chess.D4) == chess.WHITE:
        rating += 2
        
    #center control
    if board.is_attacked_by(chess.WHITE,chess.E5):
        rating += .5
    if board.is_attacked_by(chess.WHITE,chess.D5):
        rating += .5
    
    if board.is_attacked_by(chess.BLACK,chess.E4):
        rating -= .5
    if board.is_attacked_by(chess.BLACK,chess.D4):
        rating -= .5
        
    if board.is_attacked_by(chess.WHITE, chess.E5):
            rating += 0.5
        
    if board.is_attacked_by(chess.WHITE, chess.D5):
            rating += 0.5
            
    if int(board.attackers(chess.WHITE, chess.E5)) > 0:
        rating += 1 
        if int(board.attacks(chess.E5)) > 0:
            rating -= 1 
    if int(board.attackers(chess.WHITE, chess.D5)) > 0:
        rating += 1 
        if int(board.attacks(chess.D5)) > 0:
            rating -= 1 
        
        
    return rating

def black_rating(board,turn):
    #Below about how close to edge king is
    #Only good in early game
    rating = 0
    piece_points = 0 
    
    #King Safety
    if turn > 4 and turn <= 25:
        if chess.square_manhattan_distance(board.king(chess.Color(False)),chess.B8) < chess.square_manhattan_distance(board.king(chess.Color(False)),chess.G8):
            rating -= chess.square_manhattan_distance(board.king(chess.Color(False)),chess.B8)
        else:
            rating -= chess.square_manhattan_distance(board.king(chess.Color(False)),chess.G8)
    
    #Points for all pieces remaining
    for y in board.pieces(chess.PAWN,chess.BLACK):
        piece_points += 1 
    for y in board.pieces(chess.ROOK,chess.BLACK):
        piece_points += 5
    for y in board.pieces(chess.BISHOP, chess.BLACK):
        piece_points += 3
    for y in board.pieces(chess.KNIGHT, chess.BLACK):
        piece_points += 2.9
    for y in board.pieces(chess.QUEEN, chess.BLACK):
        piece_points += 9
    rating += piece_points
    
    if board.is_check():
        rating -= 0.5
    if (chess.square_knight_distance(chess.KNIGHT, chess.E4) < 1 or chess.square_knight_distance(chess.KNIGHT, chess.D4) < 1) and board.attackers(chess.WHITE, chess.E4) < board.attackers(chess.BLACK, chess.E4):
        rating += 3
    
    if board.color_at(chess.E5) == chess.BLACK:
        rating+=2
    if board.color_at(chess.D5) == chess.BLACK:
        rating += 2
    
    #center control
    if board.is_attacked_by(chess.WHITE,chess.E5):
        rating -= .5
    if board.is_attacked_by(chess.WHITE,chess.D5):
        rating -= .5
    
    if board.is_attacked_by(chess.BLACK,chess.E4):
        rating += .5
    if board.is_attacked_by(chess.BLACK,chess.D4):
        rating += .5
  
    if board.is_attacked_by(chess.BLACK, chess.E5):
        rating += 0.5
    
    if board.is_attacked_by(chess.BLACK, chess.D5):
        rating += 0.5

    if int(board.attackers(chess.BLACK, chess.E5)) > 0:
        rating += 1 
        if int(board.attacks(chess.E4)) > 0:
            rating -= 1 
    if int(board.attackers(chess.BLACK, chess.D5)) > 0:
        rating += 1 
        if int(board.attacks(chess.D4)) > 0:
            rating -= 1

    return rating    


def best_move(board, legal, color, turn):
    best_score = (0,float('-inf'))
    if '' in legal:
        legal.remove('')
    for x in legal:
        if x == '':
            break
        a = 0
        z = board.copy()
        z.push_san(x)
        a+= 1 
        color = not color
        if color == True:
            if z.attackers(not color, chess.E4) == 0 and x == 'e4':
                best_score = x
            elif z.attackers(not color, chess.D4) == 0 and x == 'd4':
                best_score = x
            elif (white_rating(board, turn) < white_rating(z, turn+a)) or black_rating(board, turn) < black_rating(z, turn+a):
                best_score = x
        if color == False:
            if z.attackers(not color, chess.E5) == 0 and x == 'e5':
                best_score = x
            elif z.attackers(not color, chess.D5) == 0 and x == 'd5':
                best_score = x
            elif black_rating(board, turn) < black_rating(z, turn+a) or white_rating(board, turn) > white_rating(z, turn+a):
                best_score = x
    if best_score == (0, float('-inf')):
        best_score = random.shuffle(legal)
        best_score = legal[0]
    return best_score
    
def depth(board, depth_amount):
    if depth_amount > 0:
        best = (float('-inf'), 'e4')
        for x in legal_moves(board):

            z = board.copy()
            z.push_san(x)
            if board.turn == True and (white_rating(z, turn) - black_rating(z, turn)) > best[0]:
                best = (white_rating(z, turn) - black_rating(z, turn), x)
            elif board.turn == False and (black_rating(z, turn) - white_rating(z, turn)) > best[0]:
                best = (black_rating(z,turn) - white_rating(z, turn), x)
                
            depth(z, depth_amount-1)

    else:
        best = best_move(board, legal_moves(board), board.turn, board.fullmove_number)
    return best

board = chess.Board()
print(board)
color = True
turn = 1
while not board.is_checkmate() and not board.is_insufficient_material() and len(legal_moves(board)) > 0:
    if color == True:
        print("Turn",turn)
        print("White's turn: ")
        turn = turn + 1
    else:
        print("Black's turn: ")
    legal = legal_moves(board)
    for x in range(len(legal_moves(board))):
        legal[x] = legal[x].strip()
    print((legal))
    if color == False:
        start = time.time()
        ran_move = depth(board, 1)
        move = ran_move[1]
        end = time.time() - start
        print(ran_move)
        print(end)
    else:
        move = input("enter the move you want to make => ").strip()
    while move not in legal:
        print('Illegal Move')
        move = input("Enter a legal move you wish to make => ").strip()
    else:
        board.push_san(move)
        print(board)
        color = not color
    print(int(board.attackers((not color), chess.D5)))

    print(white_rating(board,turn) - black_rating(board,turn))
    
print("GOOD GAME!!!")