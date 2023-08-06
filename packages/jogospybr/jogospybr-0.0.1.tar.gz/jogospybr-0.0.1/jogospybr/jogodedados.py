from random import randint
from time import sleep
from operator import itemgetter


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
