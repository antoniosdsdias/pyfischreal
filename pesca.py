"""Regras da pesca: sortear raridade e peixe, e avaliar o timing."""
import random

from config import BARRA_LARGURA, CHANCES, NIVEL_RARIDADE, PEIXES, PERFEITO_LARGURA, RARIDADES, ZONA_LARGURA


def sortear_raridade(vara):
    """Sorteia uma raridade usando as chances da vara (fichas de 1 a 1000)."""
    chances = CHANCES[vara]
    sorteio = random.randint(1, 1000)
    acumulado = 0
    for raridade in RARIDADES:
        acumulado += chances[raridade]
        if sorteio <= acumulado:
            return raridade
    return 'comum'


def sortear_peixe(vara, perfeito, lugar):
    """Sorteia o peixe pescado no lugar. Acerto perfeito sorteia duas vezes e fica com o melhor."""
    raridade = sortear_raridade(vara)
    if perfeito:
        segunda = sortear_raridade(vara)
        if NIVEL_RARIDADE[segunda] > NIVEL_RARIDADE[raridade]:
            raridade = segunda
    opcoes = []
    for nome in PEIXES:
        peixe = PEIXES[nome]
        if peixe['raridade'] == raridade and (peixe['lugar'] == lugar or peixe['lugar'] == 'todos'):
            opcoes.append(nome)
    return opcoes[random.randint(0, len(opcoes) - 1)]


def sortear_zona():
    """Posição (em pixels) onde começa a parte verde da barra."""
    return random.randint(40, BARRA_LARGURA - ZONA_LARGURA)


def avaliar_timing(marcador, zona_inicio):
    """Diz se o aperto foi 'perfeito', 'bom' ou 'errou', pela posição do marcador."""
    meio = zona_inicio + ZONA_LARGURA // 2
    if marcador >= meio - PERFEITO_LARGURA // 2 and marcador <= meio + PERFEITO_LARGURA // 2:
        return 'perfeito'
    if marcador >= zona_inicio and marcador <= zona_inicio + ZONA_LARGURA:
        return 'bom'
    return 'errou'
