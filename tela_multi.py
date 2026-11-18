"""Multiplayer no Lago Urbano: dois velhos, 1 minuto, quem pesca mais. J1 = ESPAÇO, J2 = ENTER."""
import pygame

from assets import tocar
from config import (AMARELO, BRANCO, COR_RARIDADE, FPS, HEIGHT, MENU, MULTI, NOME_RARIDADE,
                    PEIXES, RARIDADES, SAIR, TEMPO_MULTI, WIDTH)
from desenhos import escrever, painel
from pescador import Pescador


def tela_multi(window, assets, progresso):
    """Partida de 1 minuto. No fim, chama a tela de resultado."""
    clock = pygame.time.Clock()
    j1 = Pescador(250, 'J1', assets)
    j2 = Pescador(560, 'J2', assets)
    inicio = pygame.time.get_ticks()
    while True:
        clock.tick(FPS)
        agora = pygame.time.get_ticks()
        restante = TEMPO_MULTI - (agora - inicio)

        # trata eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return MENU
                if evento.key == pygame.K_SPACE:
                    tocar_resultado(j1.apertou(agora), assets, progresso)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    tocar_resultado(j2.apertou(agora), assets, progresso)

        # atualiza o estado do jogo
        for jogador in [j1, j2]:
            resultado = jogador.update(agora)
            if resultado == 'mordeu':
                tocar(assets, progresso, 'mordida')
            elif resultado == 'errou':
                tocar(assets, progresso, 'errou')
        if restante <= 0:
            return tela_resultado(window, assets, j1, j2)

        # gera saídas
        window.blit(assets['fundos']['lago'], (0, 0))
        j1.desenhar(window, assets, agora)
        j2.desenhar(window, assets, agora)
        escrever(window, assets['fonte'], f'J1 - peixes: {len(j1.peixes)}', AMARELO, 120, 30)
        escrever(window, assets['fonte'], f'J2 - peixes: {len(j2.peixes)}', AMARELO, WIDTH - 120, 30)
        segundos = (restante + 999) // 1000
        escrever(window, assets['fonte_grande'], f'{segundos // 60}:{segundos % 60:02d}', BRANCO, WIDTH // 2, 40)
        escrever(window, assets['fonte'], 'J1: ESPAÇO        J2: ENTER', BRANCO, WIDTH // 2, HEIGHT - 30)
        pygame.display.update()


def tocar_resultado(resultado, assets, progresso):
    """Toca o som certo para o que aconteceu ao apertar a tecla."""
    if resultado == 'lancou':
        tocar(assets, progresso, 'lancar')
    elif resultado == 'pegou':
        tocar(assets, progresso, 'pegou')
    elif resultado == 'errou':
        tocar(assets, progresso, 'errou')

        
def resumo(jogador):
    """Quantos peixes, valor total e quantos de cada raridade."""
    contagem = {}
    for raridade in RARIDADES:
        contagem[raridade] = 0
    valor = 0
    for nome in jogador.peixes:
        contagem[PEIXES[nome]['raridade']] += 1
        valor += PEIXES[nome]['preco']
    return len(jogador.peixes), valor, contagem




def tela_resultado(window, assets, j1, j2):
    """Tela final: mostra quem ganhou. ENTER: revanche, ESC: menu."""
    clock = pygame.time.Clock()
    qtd1, valor1, contagem1 = resumo(j1)
    qtd2, valor2, contagem2 = resumo(j2)
    if qtd1 > qtd2 or (qtd1 == qtd2 and valor1 > valor2):
        titulo = 'J1 venceu!'
    elif qtd2 > qtd1 or (qtd1 == qtd2 and valor2 > valor1):
        titulo = 'J2 venceu!'
    else:
        titulo = 'Empate!'
    while True:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return MULTI
                if evento.key == pygame.K_ESCAPE:
                    return MENU


        window.blit(assets['fundos']['lago'], (0, 0))
        escrever(window, assets['fonte_titulo'], titulo, AMARELO, WIDTH // 2, 75)
        desenhar_placar(window, assets, 'J1', qtd1, valor1, contagem1, 100)
        desenhar_placar(window, assets, 'J2', qtd2, valor2, contagem2, WIDTH // 2 + 20)
        escrever(window, assets['fonte_pequena'], 'ENTER: revanche    ESC: menu', BRANCO, WIDTH // 2, HEIGHT - 25)
        pygame.display.update()




def desenhar_placar(window, assets, nome, quantidade, valor, contagem, x):
    """Painel de um jogador: total, valor e peixes por raridade."""
    largura = WIDTH // 2 - 120
    painel(window, x, 140, largura, 350)
    centro = x + largura // 2
    escrever(window, assets['fonte_grande'], nome, AMARELO, centro, 175)
    escrever(window, assets['fonte'], f'Peixes: {quantidade}   ·   $ {valor}', BRANCO, centro, 222)
    for i in range(len(RARIDADES)):
        raridade = RARIDADES[i]
        texto = f'{NOME_RARIDADE[raridade]}: {contagem[raridade]}'
        escrever(window, assets['fonte'], texto, COR_RARIDADE[raridade], centro, 270 + i * 42)

