import json
from os import path

from config import ARQUIVO_SAVE


def progresso_novo():
    """Dicionário de quem nunca jogou."""
    return {
        'dinheiro': 0,
        'vara': 'comum',          # vara em uso
        'varas': ['comum'],       # varas compradas
        'armazem': {},            # peixe -> quantos tem guardados
        'colecao': {},            # peixe -> quantos já pescou na vida
        'lugar': 'lago',          # onde está pescando
        'cervejas': 0,            # quantas cervejas tem para beber
        'cerveja_ate': 0,         # até que instante (ms) a cerveja faz efeito
        'cervejas_seguidas': 0,   # quantas bebeu sem o efeito acabar (2 ou mais = bêbado)
        'som': True,
    }


def carregar():
    """Lê o save.json; se ainda não existe, começa do zero."""
    if not path.exists(ARQUIVO_SAVE):
        return progresso_novo()
    with open(ARQUIVO_SAVE, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
    progresso = json.loads(conteudo)
    novo = progresso_novo()
    for chave in novo:              # save antigo: completa o que faltar
        if chave not in progresso:
            progresso[chave] = novo[chave]
    progresso['cerveja_ate'] = 0      # o relógio do jogo recomeça ao abrir
    progresso['cervejas_seguidas'] = 0
    return progresso


def salvar(progresso):
    """Escreve o progresso no save.json."""
    with open(ARQUIVO_SAVE, 'w', encoding='utf-8') as arquivo:
        arquivo.write(json.dumps(progresso))


def guardar_peixe(progresso, nome):
    """Coloca um peixe no armazém e na coleção."""
    if nome in progresso['armazem']:
        progresso['armazem'][nome] += 1
    else:
        progresso['armazem'][nome] = 1
    if nome in progresso['colecao']:
        progresso['colecao'][nome] += 1
    else:
        progresso['colecao'][nome] = 1


def total_pescado(progresso):
    """Quantos peixes já pescou na vida, somando todos."""
    total = 0
    for nome in progresso['colecao']:
        total += progresso['colecao'][nome]
    return total
