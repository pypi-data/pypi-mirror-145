from random import randint
from time import sleep


def megasena():
    jogos = list()
    temp = list()
    num = 0
    print('-=' * 30)
    print(f'{"Criador de jogospybr da mega sena!":^60}')
    print('-=' * 30)
    n = int(input('Quantos jogospybr você quer criar?: '))
    for j in range(0, n):
        for s in range(0, 6):
            num = randint(1, 60)
            while True:
                if num in temp:
                    num = randint(1, 60)
                else:
                    break
            temp.append(num)
        jogos.append(temp[:])
        temp.sort()
        print(f'Jogo {j + 1} = {temp}')
        sleep(1)
        temp.clear()
    print('-=' * 30)
