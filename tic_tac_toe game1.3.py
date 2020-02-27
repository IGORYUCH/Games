from os import system
from random import choice,randint
    
def introducion():
    for string in ('There is positions\' indexes','You\'re ' + player1_side,' 1|2|3 ',
                '--|-|--',' 4|5|6','--|-|--',' 7|8|9 \n'):
        print(string)

def play():
    def find_win(side):
        for i in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
            if positions[i[0]] == side and positions[i[1]] == side and positions[i[2]] == side:
                show_field()
                print('\n'+ side + ' is Winer!')
                input('Press smth to exit')
                return False
        if not '#' in positions:
            show_field()
            print('\nIt\'s a Draw!')
            input('')
            return False
        else:
            return True    
    def bot_mov():
        bot_step = None
        while bot_step == None:
            b = randint(0,8)
            if positions[b] == '#':
                bot_step = b
        return bot_step
    
    def show_field():
        system('CLS')
        introducion()
        print(' '+positions[0]+'|'+positions[1]+'|'+positions[2]+' ')
        print('--|-|--')
        print(' '+positions[3]+'|'+positions[4]+'|'+positions[5]+' ')
        print('--|-|--')
        print(' '+positions[6]+'|'+positions[7]+'|'+positions[8]+' ')
        
    positions = ['#','#','#','#','#','#','#','#','#']
    current_step = 'x'
    game = True
    while game:
        if current_step == player1_side: # Проверка кто сейчас ходит. Изначально это крестики
            show_field()
            step = int(input('\nYer position is: '))  # Ходит человек
            if 9 < step < 1 or positions[step-1] != '#':
                print('\nWrong input. Never try again')
                continue
            else:
                positions[step-1] = current_step
                game = find_win(current_step) # Проверка на победу
                current_step = player2_side  # Меняем игрока для следующей итерации
        else:
            step = bot_mov() #  Ходит бот
            positions[step] = current_step
            game = find_win(current_step) # Проверка на победу
            current_step = player1_side # Меняем игрока для следующей итерации
    return False
        
something = True
while something:
    print('You\'re playing tic-tac-toe game')
    player1_side = input('Enter your side(x/0) or randomize it(r): ')
    if player1_side == '0':
        player2_side = 'x'
    elif player1_side == 'x':
        player2_side = '0'
    elif player1_side == 'r':
        sides = ['x','0']
        player1_side = sides.pop(choice([0,1]))
        player2_side = sides[0]
    else:
        print('\nWrong input. Never try again')
        continue
    something = play()
