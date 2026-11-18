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

