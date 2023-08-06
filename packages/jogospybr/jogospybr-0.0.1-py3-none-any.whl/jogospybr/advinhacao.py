from random import randint
from time import sleep


def advinhacao():
    print(('\033[33m-=-') * 20)
    print('\033[mJOGO DA ADVINHAÇÃO')
    print(('\033[33m-=-\033[m') * 20)
    acertou = False
    c = 0
    pc = randint(0, 10)
    n = int(input('Pensei em um número de 0 a 10, qual número foi?: '))
    while not acertou:
        if n > pc:
            n = int(input('Menos.. Tente de novo! Qual número foi?: '))
            c += 1
        elif n < pc:
            n = int(input('Mais.. Tente de novo! Qual número foi?: '))
            c += 1
        elif n == pc:
            acertou = True
            c += 1
    sleep(2)
    print('\033[32mParabéns!!! Você acertou com {} tentativas!!'.format(c))
    return
