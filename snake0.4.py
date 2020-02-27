from pynput.keyboard import Key, Listener
import threading,sys
from os import system
from random import randrange
from time import sleep
class Player:
    def __init__(self):
        self.score = 0
        self.snake_coords = [[randrange(y),randrange(x)]]
        self.head,self.tail = '☻','●'
        self.need_to_grow = None
        self.taill = None
        self.speed = [0,1] #x=second y=first
        
    def snake_move(self):
        if len(self.snake_coords) > 1:
            previous = self.snake_coords[0][:]
            previous[0] += self.speed[0]
            previous[1] += self.speed[1]
            self.snake_coords.insert(0,previous[:])
            self.snake_coords.pop()
        else:
            self.snake_coords[0][0]+=self.speed[0]
            self.snake_coords[0][1]+=self.speed[1]

class Food:
    def __init__(self):
        self.coords = [None,None]
        self.food = '♥'
        
    def find_new_pos(self):
        finded = False
        while not finded:
            self.coords[0] = randrange(len(init_field))
            self.coords[1] = randrange(len(init_field[0]))
            if self.coords not in player.snake_coords:
                finded = True
        

def key_pressed(): # обработка событий клавитуры
    def keypress(Key):
        global key_event
        key_event = str(Key)
    with Listener(on_press = keypress) as listener:# неведомая хрень
        listener.join()


def animate():
    system('cls')
    field = [i[:] for i in init_field[:]]# очищаем поле
    #перенос хвоста начало
    for frame in player.snake_coords: 
        field[frame[0]][frame[1]] = player.tail
    #перенос хвоста конец
    field[food.coords[0]][food.coords[1]]= food.food
    field[player.snake_coords[0][0]][player.snake_coords[0][1]] = player.head #переносим на новое поле игрока
    #отрисовка поля начало
    sys.stdout.write('╔══════SCORE: {: >2}═════╗\n'.format(player.score))
    for line in field:
        sys.stdout.write('║')
        for cell in line:
            sys.stdout.write(cell)
        sys.stdout.write('║\n')
    sys.stdout.write(lower_string)
    #отрисовка поля конец


lower_string = '╚════════════════════╝\n'
x,y = 20,10
init_field = init_field = [[' ' for i in range(x)] for j in range(y)]#инициализируем поле          
key_event = None # сюда записывается событие клавиутуры
game = True
left,right,up,down = True,True,True,True
my_thrd = threading.Thread(target=key_pressed,args = ()) #обрабатываем нажатия клавиш в отдельном потоке
my_thrd.start() #начать поток захвата событий клавы
player = Player()# инициализируем игрока
food = Food() #инициализируем еду
food.find_new_pos()# инициализируем позицию еды

while game:
    sleep(0.1)
    #перенос сквозной перенос при выходе за границы начало
    if player.snake_coords[0][1] > x-1:
        player.snake_coords[0] = [player.snake_coords[0][0],0]
    elif player.snake_coords[0][0] > y-1:
        player.snake_coords[0] = [0,player.snake_coords[0][1]]
    elif player.snake_coords[0][1] < 0:
        player.snake_coords[0] = [player.snake_coords[0][0],x-1]
    elif player.snake_coords[0][0] < 0:
        player.snake_coords[0] = [y-1,player.snake_coords[0][1]] 
    #перенос сквозной при выхоже за границы конец
    #обработка "поедания" начало
    if player.snake_coords[0] == food.coords:
        player.need_to_grow = food.coords
        player.taill = player.snake_coords[-1]
        food.find_new_pos()
        player.score +=1
    #обработка "поедания" конец
    if player.need_to_grow:
        if player.snake_coords[0] != player.need_to_grow:
            player.snake_coords.append(player.taill)
            player.need_to_grow = None

    if player.snake_coords[0] in player.snake_coords[1:] and len(player.snake_coords)>2:
        lower_string = '╚══════YOU LOSE══════╝\n'
        game = False
    animate()
    if (key_event == "'d'" or key_event == 'Key.right') and right:
        player.speed = [0,1]
        key_event = None #После обраротки события устанавливается исх. значение
        up,down = True,True
        left = False
    elif (key_event == "'a'" or key_event == 'Key.left') and left:
        player.speed = [0,-1]
        key_event = None
        up,down = True,True
        right = False
    elif (key_event == "'w'" or key_event == 'Key.up') and up:
        player.speed = [-1,0]
        key_event = None
        left,right = True,True
        down = False
    elif (key_event == "'s'" or key_event == 'Key.down') and down:
        player.speed = [1,0]
        key_event = None
        left,right = True,True
        up = False
    player.snake_move()
