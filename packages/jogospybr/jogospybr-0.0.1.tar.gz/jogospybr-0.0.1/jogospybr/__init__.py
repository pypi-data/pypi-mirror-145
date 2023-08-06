from random import randint
from time import sleep
from operator import itemgetter

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

def jogodedados():
    game = {'Jogador1': randint(1, 6),
            'Jogador2': randint(1, 6),
            'Jogador3': randint(1, 6),
            'Jogador4': randint(1, 6)}
    ranking = {}
    print('Valores sorteados')
    for k, v in game.items():
        print(f'{k} tirou {v} no dado')
        sleep(1)
    ranking = sorted(game.items(), key=itemgetter(1), reverse=True)
    print('Ranking dos jogadores')
    for i, v in enumerate(ranking):
        print(f'O {v[0]} tirou {v[1]} e ficou em {i + 1} lugar')
        sleep(1)

def jokenpo():
    print('\033[33m-=-\033[m' * 15)
    print('JOKENPÔ!!!')
    print('\033[33m-=-\033[m' * 15)
    ve = 0
    vp = 0
    vc = 0
    for c in range(1, 6):
        p = str(input('Vamos jogar? Qual você escolhe?:'))
        pu = p.upper()
        lista = ['Pedra', 'Papel', 'Tesoura']
        pcn = randint(1, 3)
        pc = lista[(pcn - 1)]
        print('Pedra, Papel, Tesooooura!!!')
        sleep(2)
        if pu == 'PEDRA' and pcn == 1:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('Empatou, vamos de jogar de novo?')
            ve = ve + 1
        elif pu == 'PEDRA' and pcn == 2:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('O {} embrulha a {}!!\n\033[31mVocê perdeu!\033[m\nVamos Jogar de novo?'.format(pc, p))
            vc = vc + 1
        elif pu == 'PEDRA' and pcn == 3:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('A {} quebra a {}!!\n\033[32mVocê VENCEU!\033[m\nVamos Jogar de novo?'.format(p, pc))
            vp = vp + 1
        elif pu == 'PAPEL' and pcn == 2:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('Empatou, vamos de jogar de novo?')
            ve = ve + 1
        elif pu == 'PAPEL' and pcn == 1:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('O {} embrulha a {}!!\n\033[32mVocê VENCEU!\033[m\nVamos Jogar de novo?'.format(p, pc))
            vp = vp + 1
        elif pu == 'PAPEL' and pcn == 3:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('A {} corta o {}!!\n\033[31mVocê perdeu!\033[m\nVamos Jogar de novo?'.format(pc, p))
            vc = vc + 1
        elif pu == 'TESOURA' and pcn == 3:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('Empatou, vamos de jogar de novo?')
            ve = ve + 1
        elif pu == 'TESOURA' and pcn == 2:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('A {} corta o {}!!\n\033[32mVocê VENCEU!\033[m\nVamos Jogar de novo?'.format(p, pc))
            vp = vp + 1
        elif pu == 'TESOURA' and pcn == 1:
            print('Eu vou de {}\nvocê foi de {}'.format(pc, p))
            print('A {} quebra a {}!!\n\033[31mVocê perdeu!\033[m\nVamos Jogar de novo?'.format(pc, p))
            vc = vc + 1
        else:
            print('\033[41mVocê não está jogando direito, é pedra, papel ou tesoura!! Tente de novo\033[m')
    print('\033[33m-=-\033[m' * 15)
    print(
        '\033[1;36mPlacar da jogada (Melhor de 5)\033[m\nVitórias do jogador {}\nVitórias do Computador {}\nEmpate {}'.format(
            vp, vc, ve))
    print('\033[33m-=-\033[m' * 15)

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
