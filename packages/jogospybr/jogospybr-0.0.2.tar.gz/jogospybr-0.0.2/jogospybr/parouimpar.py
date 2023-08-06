from random import randint


def parouimpar():
    cont = 0
    while True:
        print('\033[1;36mPar ou ímpar?\033[m')
        j = ' '
        while j not in 'PpIi':
            j = str(input('Qual você escolhe?: [Par ou Ímpar] ')).strip().upper()[0]
        p = int(input('Digite um número para jogar: '))
        pc = randint(0, 10)
        if j == 'P':
            print('Você é PAR e o computador ÍMPAR')
            if (p + pc) % 2 == 0:
                print(f'\033[32mVocê venceu, colocou {p} e o computador colocou {pc}. A soma é {p + pc}\033[m')
                cont += 1
            elif (p + pc) % 2 != 0:
                print(f'\033[31mVocê perdeu!! Seu número foi {p} e o do computador {pc}. A soma é {p + pc}')
                print(f'Sua sequência foi de {cont} vitórias')
                break
        elif j == 'I':
            print('Você é ÍMPAR e o computador PAR')
            if (p + pc) % 2 != 0:
                print(f'\033[32mVocê venceu, colocou {p} e o computador colocou {pc}. A soma é {p + pc}\033[m')
                cont += 1
            elif (p + pc) % 2 == 0:
                print(f'\033[31mVocê perdeu!! Seu número foi {p} e o do computador {pc}. A soma é {p + pc}')
                print(f'Sua sequência foi de {cont} vitórias')
                break
