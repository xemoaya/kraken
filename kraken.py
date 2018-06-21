import pyglet  
import random  
import math
  
from pyglet.window import key   
from pyglet.window import mouse  

from pyglet.gl import *

from board import *
from global_cfg import *

from chess import *
from stratagy import *

window=pyglet.window.Window(window_width,window_height)  

board = None
snake = None
ship = None
king = None
user_chess = None
selected_index = -1
game_end = False
game_label = None

#for mouse picking animation
shake_list = []
stand_shake_clock = 10
shake_clock = stand_shake_clock

#for chess movement animation
movement_list = []
stand_movement_clock = 10
movement_clock = stand_movement_clock

#for disapear animation
disapear_list = []
stand_disapear_clock = 10
disapear_clock = stand_disapear_clock

board_grid = None

turn_flag = "user"

@window.event
def on_draw():
    window.clear()
    board.draw()
    for s in snake :
        s.draw()
    
    for s in user_chess :
        s.draw()
    game_label.draw()

def  select_chess(x,y):
    global user_chess
    for i in range(len(user_chess) ):
        chess = user_chess[i]
        nx, ny = chess.x, chess.y
        #print (nx, ny, x, y)
        if judge_same_grid(nx, x, ny, y) : 
            return i
        #if abs(nx - x) < chess_width / 2 and abs(ny - y) < chess_width / 2 :
        #    return i
    return -1 #invisible  coordinate




def center_image(image):
    """Sets an image's anchor point to its center"""
    global zoom_rate
    image.width = chess_width
    image.height = chess_width
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2


def check_movement(chess, next_x, next_y) :
    global board_grid
    if not judge_next_grid(chess.x, next_x, chess.y, next_y) :
        print("not next grid")
        return False
    if board_grid.check_occupy(next_x, next_y) :
        print("occupy")
        return False
    
    if chess.type == "ship" and board_grid.get_grid_type(next_x, next_y) != "normal" :
        return False
    return True

@window.event
def on_key_press(symbol, modifiers):
    global game_end, game_label
    if symbol == pyglet.window.key.SPACE and game_end:
        init()
        game_end = False
        game_label.text = ""

@window.event  
def on_mouse_press(x, y, button, modif):  
    if game_end :
        return
    global selected_index, movement_list, board_grid, user_chess, snake, disapear_list, game_label
    if button==mouse.LEFT:  
        if game_label.text != "":
            game_label.text = ""

        idx = select_chess(x, y)
        if idx > -1 : #selected one chess
            selected_index = idx
            shake_list.append(selected_index)
        elif selected_index > -1 :
            nx, ny = board_grid.get_grid(x, y)
            #print (nx, ny)
            chess = user_chess[selected_index]
            if check_movement(chess, nx, ny) :
                movement_list.append((chess, (nx, ny)))
                board_grid.unoccupy(chess.x, chess.y)
            else :
                shake_list.append(selected_index)
            selected_index = -1
            
    

def build_map_v1() :
    snake_xy = [(basic_x + 2*grid_width, basic_y),
                (basic_x + 4*grid_width, basic_y),
                (basic_x, basic_y + 2*grid_width),
                (basic_x, basic_y + 4*grid_width),
                (basic_x + 6*grid_width, basic_y + 2*grid_width),
                (basic_x + 6*grid_width, basic_y + 4*grid_width),
                (basic_x + 2*grid_width, basic_y + 6*grid_width),
                (basic_x + 4*grid_width, basic_y + 6*grid_width)]
    king_xy = (basic_x + 3*grid_width, basic_y + 3*grid_width)

    ship_xy = [(basic_x + 2*grid_width, basic_y + 3*grid_width),
               (basic_x + 4*grid_width, basic_y + 3*grid_width),
               (basic_x + 3*grid_width, basic_y + 2*grid_width),
               (basic_x + 3*grid_width, basic_y + 4*grid_width)]

    return snake_xy, king_xy, ship_xy

def init():
    global board,window_width,window_height,zoom_rate, user_chess
    #global ship,king,snake
    global ship, snake
    global board_grid,game_end, game_label

    global shake_list, movement_list, disapear_list

    pyglet.resource.path = ['./resource']
    
    pyglet.resource.reindex()
    board_image = pyglet.resource.image("board.png")
    snake_image = pyglet.resource.image("snake.png")
    ship_image  = pyglet.resource.image("ship.png")
    king_image  = pyglet.resource.image("king.png")
    
    for img in snake_image,ship_image,king_image :
        center_image(img)

    board_image.width = window_width
    board_image.height = window_height
    board = pyglet.sprite.Sprite(img = board_image)
    
    
    snake_xy,king_xy, ship_xy = build_map_v1()

    snake = []
    for i in range(len(snake_xy)) :
        ns = Chess(img = snake_image, x = snake_xy[i][0], y = snake_xy[i][1], type = "snake")
        snake.append(ns)

    king = Chess(img = king_image, x = king_xy[0], y = king_xy[1], type = "king")

    ship = []
    for i in range(len(ship_xy) ) :
        sp = Chess(img = ship_image, x = ship_xy[i][0], y = ship_xy[i][1], type = "ship")
        ship.append(sp)
    user_chess = ship + [king]
    #snake = pyglet.sprite.Sprite(img=snake_image,x=45, y=62)

    board_grid = BoardGrid()

    for c in snake + user_chess :
        board_grid.occupy(c.x, c.y)

    global exit_grid, center_grid
    for g in exit_grid : 
        board_grid.set_grid_type(g[0], g[1], "exit")
    board_grid.set_grid_type(center_grid[0], center_grid[1], "block")

    game_end = False
    game_label = pyglet.text.Label("press to start", font_size=36,x=window.width//2, y=window.height//2 + 100,anchor_x='center', anchor_y='center')
    game_label.color = (0, 0, 0, 200)
    game_label.font_name = 'Times New Roman'

    movement_list = []
    shake_list = []
    disapear_list = []

def update(dt) :
    #deal with chess shake
    global shake_list, shake_clock, user_chess,stand_shake_clock
    if len(shake_list) > 0 :
        #print (shake_list)
        if shake_clock == -1 :
            shake_clock = stand_shake_clock
            shake_list.pop(0)
        else :
            idx = shake_list[0]
            user_chess[idx].scale =1 + 0.02 * (stand_shake_clock//2 - abs(stand_shake_clock//2 - shake_clock) )
            shake_clock -= 1

    global movement_list, stand_movement_clock, movement_clock, grid_width,disapear_list, game_label, game_end
    if len(movement_list) > 0 :
        chess = movement_list[0][0]
        nx, ny = movement_list[0][1]
        if movement_clock == -1 :#the last step
            chess.x = nx 
            chess.y = ny
            board_grid.occupy(nx, ny)
            if judge_game_win(user_chess, board_grid) :
                game_end = True
                game_label.text = "You Win!"
                return
            #judge defeat snake
            if chess.type == "snake" :
                slist = judge_defeat_chess(snake, user_chess)
            else :
                slist = judge_defeat_chess(user_chess, snake)
                #it is snake's turn now
                chess, (nx, ny) = snake_move(snake, user_chess, board_grid)
                #print(chess.x, chess.y, nx, ny)
                movement_list.append( (chess, (nx, ny)) )
                board_grid.unoccupy(chess.x, chess.y)

            #print (slist)
            for s in slist:#remove
                s.isalive = False
                if s.type == "king" :
                    game_end = True
                    game_label.text = "You lose.."
                board_grid.unoccupy(s.x, s.y)
                disapear_list.append(s)
            movement_clock = stand_movement_clock
            movement_list.pop(0)
        else :
            step = grid_width / stand_movement_clock
            if abs(nx - chess.x) > 1 :
                chess.x += step * (nx - chess.x)/abs(nx - chess.x)
            if abs(ny - chess.y) > 1 :
                chess.y += step * (ny - chess.y)/abs(ny - chess.y)
            movement_clock -= 1
            
    global disapear_clock, stand_disapear_clock
    if len(disapear_list) > 0 : 
        if disapear_clock == -1 :
            disapear_clock = stand_disapear_clock
            disapear_list.pop(0)
        else :
            chess = disapear_list[0]
            chess.scale = 1 + 0.02 * (stand_disapear_clock - disapear_clock)
            chess.opacity = 255 * disapear_clock * 0.1
            disapear_clock -= 1

if __name__ == '__main__':
    init()
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()





