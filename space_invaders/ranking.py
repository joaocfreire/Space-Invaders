from datetime import date
from functools import cmp_to_key


# Função auxiliar para ordenar os dados do arquivo de ranking com base na maior pontuação
def cmp_score(s1, s2):
    s1 = int(s1.split()[1])
    s2 = int(s2.split()[1])

    if s1 > s2:
        return -1
    elif s1 < s2:
        return 1
    else:
        return 0


# Grava os dados do player em arquivo após ele perder
def save_file(f, score):
    print('—' * 50)
    print(f'\033[0:31m{'GAME OVER':^50}\033[m')
    print('—' * 50)

    player_name = input(f'\033[34m{'Digite seu nome: '}\033[m').upper()

    day = date.today().day
    month = date.today().month
    year = date.today().year

    if day < 10:
        day = f'0{day}'
    if month < 10:
        month = f'0{month}'

    date_gameplay = f'{day}/{month}/{year}'
    datas = f'{player_name} {score} {date_gameplay}'

    file = open(f, 'a')
    file.write(datas)
    file.write('\n')
    file.close()


# Recupera os players armazenados em arquvivo
def recover_file(f):
    rank = []
    # Tenta abrir o arquivo de ranking
    try:
        file = open(f)
        p = file.readline()
        while p != '':
            rank.append(p)
            p = file.readline()
        file.close()

    except FileNotFoundError:
        pass

    return sorted(rank, key=cmp_to_key(cmp_score))
