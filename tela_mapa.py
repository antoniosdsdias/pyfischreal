"Mapa: escolher onde pescar (lago, rio, mar ou o lixão secreto)."
import pygame

from config import (AMARELO, BRANCO, FPS, HEIGHT, LUGAR, LUGARES, PEIXES_PARA_LIXAO, SAIR, SINGLE,
                    VERMELHO, WIDTH)
from dados import salvar, total_pescado
from desenhos import escrever, painel

ALTURA_LINHA = 90


def motivo_bloqueio(progresso, lugar):
    """funcao que retorna o motivo pelo qual não se pode pescar no lugar. Texto vazio quer dizer que dá."""
    if lugar == 'lixao' and total_pescado(progresso) < PEIXES_PARA_LIXAO:
        faltam = PEIXES_PARA_LIXAO - total_pescado(progresso)
        return f'Pesque mais {faltam} peixes para descobrir'
    if lugar == 'mar' and progresso['vara'] == 'comum':
        return 'Precisa de uma vara melhor que a Comum'
    return ''
