import pygame
from copy import deepcopy # нужен для "глубокого" копирования списков
from random import choice
class Figure:
    def __init__(self,coords,clr):
        self.rects_coords = coords #список коордитат квадратов, относящихся к финуре в данный момент
        self.figure_index = random_figures.index(coords)
        self.color = clr # цвет используемый для закраски квадратов
        self.orig_figure = deepcopy(coords)
        self.rotate_status = 0 
        self.was_swapped = False

    def fall(self): # перемещает фигуру вниз
        field.change_color(self.rects_coords,field.color)#затираем стандартным цветом предыдущие квадраты, занятые фигурой
        for rect in self.rects_coords:
            rect[1]+=1# меняем координату Y каждого квадрата фигуры
        field.change_color(self.rects_coords,self.color)#закрашиваем в цвет фигуры новые ее квадраты
       
    def is_overlayed(self,rect_list):#Метод, необходимый для проверки наложения новой фигуры на непустые квадраты
        for rect in rect_list:
            # Если в указанных координатах находится пустота или указанные координаты в списке координат квадратов фигуры...
            if not ((field.rects[rect[1]][rect[0]] == field.color) or ([rect[0],rect[1]] in self.rects_coords)):
                break
        else: return False

    def is_overlayed2(self,rect_list):
        for rect in rect_list:
            if not (field.rects[rect[1]][rect[0]] == field.color):
                return True
        else:
            return False
            

    def move(self,direction):# перемещает фигуру влево - вправо
        x_cords = [i[0] for i in self.rects_coords]
        figure_max_x, figure_min_x = max(x_cords), min(x_cords)
        if (figure_max_x+direction <= len(field.rects[0])-1) and (figure_min_x-1>=0 or direction > 0):# если максимальный х квадрата фигуры больше длины строки х-1...
            rects_plus_d = [[rect[0]+direction,rect[1]] for rect in deepcopy(self.rects_coords)] # Создаем копию исходного массива и увеличиваем каждый x на ведичину direction
            if self.is_overlayed(rects_plus_d) == False:#Если перемещенная фигура не накладывается на непустые квадраты...
                field.change_color(self.rects_coords,field.color)
                self.rects_coords = rects_plus_d
                field.change_color(self.rects_coords,self.color)
            
    def rotate(self):# Метод поворота фигуры
        rotated_fig = deepcopy(self.rects_coords)# Сначала сделаем копию фигуры, повернем ее и проверим, не вылезает ли она за границы поля...
        for index in range(len(self.rects_coords)):
            rotated_fig[index][0]+= figure_rotate[self.figure_index][self.rotate_status][index][0]# Применяем правило поворота для x
            rotated_fig[index][1]+= figure_rotate[self.figure_index][self.rotate_status][index][1]# Применяем правило поворота для y
        x_coords = [i[0] for i in rotated_fig]
        y_coords = [j[1] for j in rotated_fig]
        max_x,max_y = max(x_coords),max(y_coords)
        min_x,min_y = min(x_coords),min(y_coords)
        if (min_y >= 0) and (min_x >= 0) and (max_x <= len(field.rects[0])-1) and (max_y <= len(field.rects)-1):# Если
            if self.is_overlayed(rotated_fig) == False:#Если повернутая фигура не накладывается на непустые квадраты...
                field.change_color(self.rects_coords,field.color)
                self.rects_coords = deepcopy(rotated_fig)# Если все условия соблюдены, Делаем копию основной фигурой
                self.rotate_status+=1# После успешного поворота увеличиваем статус поворота
                if self.rotate_status == len(figure_rotate[self.figure_index]):# если было было применено последнее правило поворота, то фигура в исходнои положении
                    self.rotate_status = 0
                field.change_color(self.rects_coords,self.color)
                
    def update_figure(self):#Замена фигуры на новую с новым цветомF
        self.rects_coords = deepcopy(next_fig.figure)# Выбыр новой фигуры
        self.orig_figure = deepcopy(next_fig.figure)
        self.color = next_fig.color# Новый цвет
        self.figure_index = random_figures.index(self.rects_coords)# новый индекс правила вращения, в сответствии с выбранной фигурой
        self.rotate_status = 0 # Обнуляем статус вращения
        self.was_swapped = False
        if self.is_overlayed2(self.rects_coords) == True:
            return 1#Если при обновлении фигура накладывается, возвращаем 1
        
    def get_collision(self):#Метод проверки состояния под фигурой и если нужно выбор новой фигуры
        y_coords = [i[1] for i in self.rects_coords]
        y_max = max(y_coords)
        bottom_rects =[]
        for rect in self.rects_coords:
            if rect[1]==y_max:
                bottom_rects.append(rect[:])
        for bottom_rect in bottom_rects:
            if bottom_rect[1]==len(field.rects)-1:#Проверка на достижения ДНА. Иначе проверка состояния квадрата внизу
                field.strip_completed_lines()
                if self.update_figure() == 1: return 1
                next_fig.update_figure()
                break
            else:
                for rect in self.rects_coords:
                    # Если клетка под квадратом не пустая и не входит в число клеток фигуры...
                    if field.rects[rect[1]+1][rect[0]] != field.color and ([rect[0],rect[1]+1] not in self.rects_coords):
                        field.strip_completed_lines()
                        if self.update_figure() == 1: return 1#Если фигура наложилась при обновлении, возвращаем 1
                        next_fig.update_figure()
                        break

    def swap(self):#Меняет фигуру на удерживаемую
        if self.was_swapped == False:
            swap_sound.play()
            if swap_fig.printed_figure == [[0,0],]:#Если фигура в свапе изначально пустая...
                swap_fig.figure = deepcopy(self.orig_figure)
                swap_fig.color = self.color
                swap_fig.printed_figure = [[printed_crds[0]-5,printed_crds[1]+1] for printed_crds in deepcopy(self.orig_figure)] 
                swap_fig.change_color(swap_fig.printed_figure,swap_fig.color)
                field.change_color(self.rects_coords,air_color)
                self.update_figure()
            else:
                field.change_color(self.rects_coords,air_color)
                swap_fig.change_color(swap_fig.printed_figure,air_color)
                new_fig = deepcopy(swap_fig.figure)#Сохраняем в промежуточную переменную координаты квадратов свап фигуры
                new_color = swap_fig.color#Сохраняем в промежуточную переменную цвет свап фигуры
                swap_fig.figure = deepcopy(self.orig_figure)
                swap_fig.color = self.color
                swap_fig.printed_figure = [[printed_crds[0]-5,printed_crds[1]+1] for printed_crds in deepcopy(swap_fig.figure)]
                swap_fig.change_color(swap_fig.printed_figure,swap_fig.color)
                self.orig_figure = deepcopy(new_fig)
                self.rects_coords = deepcopy(new_fig)
                self.color = new_color
                self.rotate_status = 0
                self.figure_index = random_figures.index(new_fig)
                field.change_color(self.rects_coords,self.color)
            self.was_swapped = True
            
             
class Field:
    def __init__(self,air_color):
         self.color = air_color
         self.rects = [[self.color for j in range(t_cells_x)] for i in range(t_cells_y)] #генератор двухмерного массива

    def change_color(self,rect_list,color):# своеобразный сеттер для изменения цвета квадратов
        for rect in rect_list:
            self.rects[rect[1]][rect[0]] = color

    def strip_completed_lines(self):#Метод отвечающий за очиску заполненных линий и перемещение вниз квадратов, находившихся над этой линией
        global score
        line_length = len(self.rects[0])
        for line in range(len(self.rects)):
            for rect in range(line_length):# Цикл проверяющий очередную линию поля на завершенность
                if self.rects[line][rect] == self.color:
                    break
            else:
                strip_line_sound.play()
                self.rects[line] = deepcopy([self.color for i in range(line_length)])#Заполняем завершенную линию пустыми квадратами
                for new_line in range(line-1,-1,-1):#Цикл по всем линиям выше текущей завершенной линии
                    for new_rect in range(line_length):
                        if self.rects[new_line][new_rect] != self.color:
                            self.rects[new_line+1][new_rect] = self.rects[new_line][new_rect]
                            self.rects[new_line][new_rect]= self.color
                score+=t_cells_x*10

    def reset(self):# Закрашивает в стандартный цвет все поле
        for line in range(len(self.rects)):
            for rect in range(len(self.rects[0])):
                self.rects[line][rect] = self.color


class Next_fig:  # класс новой фигуры и класс удерживаемой фигуры
    def __init__(self,new_coords,new_clr):
        self.field = [[field.color for j in range(4)] for i in range(3)]
        self.figure = new_coords
        self.printed_figure = [[printed_crds[0]-5,printed_crds[1]+1] for printed_crds in deepcopy(self.figure)]
        self.color = new_clr
        
    def change_color(self,rect_list,color):# своеобразный сеттер для изменения цвета квадратов
        for rect in rect_list:
            self.field[rect[1]][rect[0]] = color

    def update_figure(self):
        self.change_color(self.printed_figure,air_color)
        self.figure = deepcopy(choice(random_figures))
        self.printed_figure = [[printed_crds[0]-5,printed_crds[1]+1] for printed_crds in deepcopy(self.figure)]
        self.color = choice(random_colors)
        self.change_color(self.printed_figure,self.color)


class Swap_fig:  # класс новой фигуры и класс удерживаемой фигуры
    def __init__(self):
        self.field = [[field.color for j in range(4)] for i in range(3)]
        self.figure = [[5,-1],]
        self.printed_figure = [[printed_crds[0]-5,printed_crds[1]+1] for printed_crds in deepcopy(self.figure)]
        self.color = air_color
        
    def change_color(self,rect_list,color):# своеобразный сеттер для изменения цвета квадратов
        for rect in rect_list:
            self.field[rect[1]][rect[0]] = color

def animate():# функция, отвечающая за отрисовку поля
    for y in range(len(field.rects)):# цикл по всем квадратом поля.Каждый элемент этого списка содержит цвет квадрата
        for x in range(len(field.rects[y])):
            pygame.draw.rect(tetris,field.rects[y][x],(cube_side*x,cube_side*y,cube_side,cube_side),0)
            pygame.draw.rect(tetris,air_color,(cube_side*x,cube_side*y,cube_side,cube_side),1)
    for y in range(len(next_fig.field)):#Отрисовываем квадраты следующей фигуры на ее области
        for x in range(len(next_fig.field[y])):
            pygame.draw.rect(next_figure,next_fig.field[y][x],(cube_side*x,cube_side*y,cube_side,cube_side),0)
            pygame.draw.rect(next_figure,air_color,(cube_side*x,cube_side*y,cube_side,cube_side),1)
    for y in range(len(swap_fig.field)):#Отрисовываем квадраты удерживаемой фигуры на ее области
        for x in range(len(swap_fig.field[y])):
            pygame.draw.rect(swap_figure,swap_fig.field[y][x],(cube_side*x,cube_side*y,cube_side,cube_side),0)
            pygame.draw.rect(swap_figure,air_color,(cube_side*x,cube_side*y,cube_side,cube_side),1)

    score_text  = text_font.render('score:{: >6}'.format(int(score)),0,(0,0,0))
    screen.blit(tetris,(5,5))# Отрисовываем поле тетриса
    screen.blit(next_text,(tetris_len_x+10,5))#Отрисовываем Надпись next
    screen.blit(next_figure,(tetris_len_x+10,25))#Отрисовываем поле следующей фигуры
    screen.blit(swap_text,(tetris_len_x+10,120))# Отрисовываем надпись hold
    screen.blit(swap_figure,(tetris_len_x+10,140))# Отрисовываем поле удерживаемой фигуры
    pygame.draw.rect(screen,air_color,[tetris_len_x+10,240,150,40],0)#Зарисовываем белым место отрисовки счета
    pygame.draw.rect(screen,(0,0,0),[1,1,365,605],1)
    pygame.draw.rect(screen,(0,0,0),[369,25,122,91],1)
    pygame.draw.rect(screen,(0,0,0),[369,140,122,91],1)
    screen.blit(score_text,(tetris_len_x+10,240))#Отрисовываем надпись счета
    screen.blit(hint_text,(5,605))
    pygame.display.flip()

def reset_game():#Функция, начинающая новую игру
    global score,down_pressed
    down_pressed = False
    score = 0
    field.reset()
    next_fig.update_figure()
    figure.update_figure()
    next_fig.update_figure()


pygame.init()
pygame.display.set_caption('Tetris')
size = sizeX,sizeY = 500,620
cube_side = 30# размер квадрата из которых состоит поле тетриса
air_color = (255,255,255)# Стандартный цвет пустого квадата
screen = pygame.display.set_mode(size)# Основной экран, на котором рисуются поверхности и счет игрока
screen.fill(air_color)
next_figure = pygame.Surface((cube_side*4,cube_side*3))#Поверхность, на которой рисуется следующая фигура
swap_figure = pygame.Surface((cube_side*4,cube_side*3))
text_font = pygame.font.Font(None,28)
next_text = text_font.render('Next',0,(0,0,0))
swap_text = text_font.render('Hold',0,(0,0,0))
tetris_len_x,tetris_len_y = 360,600#Размер поверхости тетриса в пикселах
t_cells_x = int(tetris_len_x/cube_side)#Количество ячеек по x при заданной длине поля
t_cells_y = int(tetris_len_y/cube_side)
tetris = pygame.Surface((tetris_len_x,tetris_len_y))#Поверхость на которой рисуется тетрис

random_figures = (
    [[5,1],[6,1],[6,0],[7,0]],
    [[6,1],[7,1],[5,0],[6,0]],
    [[5,1],[6,1],[7,1],[6,0]],
    [[6,0],[7,0],[6,1],[7,1]],
    [[5,0],[6,0],[7,0],[7,1]],
    [[5,0],[6,0],[7,0],[5,1]],
    [[5,0],[6,0],[7,0],[8,0]]
                  )

random_colors = (
    (120,180,0),(240,120,120),(180,0,0),(140,0,140),(0,140,140),
    (240,120,0),(0,0,200),(0,140,0),(190,190,0),(255,128,0)
                )

# Правила вращения для каждой фигуры. У каждой фигуры есть собсвенные этапы вращения, каждый этап содержит 4 кортежа - правила перемещения для каждого квадрата фигуры
# Правило перемещения это просто 2 числа, которые прибавляются к x и y соответственно. Стоит обратить внимание, что не у всех фигур по 4 этапа, а у фигуры, представляющей
# собой квадрат, этап состоит из нолей,такую фигуру вращать бессмысленно
figure_rotate = (
    (((0,0),(0,0),(-1,0),(-1,2) ),((0,0),(0,0),(1,0),(1,-2))),
    (((0,0),(0,0),(1,2),(1,0)),((0,0),(0,0),(-1,-2),(-1,0))),
    (((1,-1),(0,0),(-1,1),(1,1)),((1,1),(0,0),(-1,-1),(-1,1)),((-1,1),(0,0),(1,-1),(-1,-1)),((-1,-1),(0,0),(1,1),(1,-1))),
    (((0,0),(0,0),(0,0),(0,0)),),
    (((1,-1),(0,0),(-1,1),(-2,0)),((1,1),(0,0),(-1,-1),(0,-2)),((-1,1),(0,0),(1,-1),(2,0)),((-1,-1),(0,0),(1,1),(0,2))),
    (((1,-1),(0,0),(-1,1),(0,-2)),((1,1),(0,0),(-1,-1),(2,0)),((-1,1),(0,0),(1,-1),(0,2)),((-1,-1),(0,0),(1,1),(-2,0))),
    (((1,-1),(0,0),(-1,1),(-2,2)),((-1,1),(0,0),(1,-1),(2,-2)))
                )

strip_line_sound = pygame.mixer.Sound('blop.wav')
swap_sound = pygame.mixer.Sound('pop.wav')
field = Field(air_color)
#Выбор случайной фигуры и случайного цвета из списков выше
figure = Figure(deepcopy(choice(random_figures)),choice(random_colors))# используем deepcopy так как нужна полная копия массива, а не еще одна ссылка на него
field.change_color(figure.rects_coords,figure.color)
next_fig = Next_fig(deepcopy(choice(random_figures)),choice(random_colors))
next_fig.change_color(next_fig.printed_figure, next_fig.color)
swap_fig = Swap_fig()
swap_fig.change_color(swap_fig.printed_figure,swap_fig.color)
game_alive,down_pressed,losed = True,False,False
score,speed,need_to_fall = 0,1,0
background = pygame.Surface((sizeX,sizeY))
background.fill(air_color)
background.set_alpha(5)
lose_font = pygame.font.Font(None,55)
lose_text = lose_font.render('YOU LOSE',0,(0,0,0))
hint_font = pygame.font.Font(None,20)
hint_text = hint_font.render('right/left - move  up - rotate  down - boost speed  r_ctrl - swap figure  r - restart',0,(0,0,0))
while game_alive:
    if not losed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_alive = False
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_DOWN]:
                    down_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    figure.move(1)
                elif event.key == pygame.K_LEFT:
                    figure.move(-1)
                elif event.key == pygame.K_UP:
                    figure.rotate()
                elif event.key == pygame.K_DOWN:
                    down_pressed = False
                elif event.key == pygame.K_RCTRL:
                    figure.swap()
                elif event.key == pygame.K_r:
                    reset_game()
        if down_pressed:# Если зажата стрелка вниз то перемещаем в 6 раз быстрее
            speed = 6
            score+=0.05
        else:
            speed = 1
        if need_to_fall >100:
            if figure.get_collision() == None:#Если возвращает ноль, фигура не наложилась
                figure.fall()
                need_to_fall = 0
            else:
                losed = True
                
        else:
            need_to_fall +=speed
        animate()
    else:
        screen.blit(background,(0,0))
        screen.blit(lose_text,(180,180))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_alive = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    losed = False
                    reset_game()
pygame.quit()
