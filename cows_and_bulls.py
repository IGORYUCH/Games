import random
chisl  = str(random.randint(1000,10000))
attempts = 6
right = False
cows,bulls = 0,0
print('Число загадано')
print(f'У вас {attempts} попыток!')
while attempts >= 1 or right:
    user = input('ВВеди число: ')
    if len(user) != 5:
        print('Число должно быть 5 знаков!')
        continue
    for char in user:
        if char not in '0123456789':
            not_int = True
            break
    if not_int:
        print('Число должно быть целым десятичным!')
        continue
    if user == chisl:
        right = True
        print (f'Вы угадали. Это число {chisl} ')
        break
    else:
        stuff = list(chisl)
        for index in range(len(chisl)):
            for i in range(index, len(chisl)):
                if user[i] == chisl[i]:
                    if user[index] == user[i]:
                        sov = True
                        break
                    else:
                        sov = False
                else:
                    sov = False
            if user[index] == chisl[index]:
                bulls +=1
            elif user[index] in stuff and not sov:
                cows +=1
                stuff.remove(user[index])
        print(f'Неверно. Коров {cows},быков {bulls}')
    attempts -= 1
    cows,bulls = 0,0
    if attempts ==0:
        print('Попытки кончились')
        print(f'Игра окончена. Это было число {chisl}')
input()#hold window
