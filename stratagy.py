from global_cfg import *
import pyglet  
from board import *
import random

def judge_defeat_chess(attacker, defender) :
    rlist = []
    for df in defender :
        if df.isalive :
            ct = 0
            for att in attacker :
                if att.isalive and judge_next_grid(df.x, att.x, df.y, att.y) :
                    ct += 1
            if ct >= 2 :
                rlist.append(df)
                    
    return rlist

def judge_game_win(user_chess, board_grid) :
    for chess in user_chess :
        if chess.type == "king" and board_grid.get_grid_type(chess.x, chess.y) == "exit" :
            return True
    return False

def snake_move(snake, user_chess, board_grid) :
    #random move
    global grid_width
    
    dirt = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    able_list = []
    for s in snake :
        dir_list = []
        if s.isalive :
            for i in range(len(dirt)) :
                nx, ny = s.x + dirt[i][0] * grid_width, s.y + dirt[i][1] * grid_width
                if board_grid.get_grid_type(nx, ny) == "normal" and not board_grid.check_occupy(nx, ny) :  
                    #able_list.append( (s, (nx, ny), random.randint(1, 100)) )
                    able_list.append( [s, (nx, ny), 0] )
                    print("xxx", s.x, s.y, nx, ny)
    for i in range(len(able_list)) :#caculate scores for all elements
        chess = able_list[i][0]
        (x, y) = able_list[i][1]
        score = 0
        for uc in user_chess :
            #print(x-uc.x, y-uc.y, judge_next_grid(x, uc.x, y, uc.y), uc.isalive )
            if uc.isalive and judge_next_grid(x, uc.x, y, uc.y) : 
                score += 100
        able_list[i][2] = score
    

    able_list.sort(key=lambda x : x[2], reverse = True)
    print(able_list)

    return able_list[0][0], able_list[0][1] #return chess and next location

    








            