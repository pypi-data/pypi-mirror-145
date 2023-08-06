from random import randint
from time import sleep


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
