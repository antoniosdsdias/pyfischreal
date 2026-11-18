"""Configurações: ligar e desligar o som."""
import pygame

from assets import tocar_musica
from config import AMARELO, BRANCO, FPS, HEIGHT, MENU, SAIR, WIDTH
from dados import salvar
from desenhos import escrever, painel


def tela_config(window, assets, progresso):
    """ENTER em 'Som' liga/desliga a música e os efeitos; 'Voltar' volta ao menu."""
    clock = pygame.time.Clock()
    escolha = 0
    while True:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return MENU
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    escolha = 1 - escolha      # só 2 opções: 0 vira 1 e 1 vira 0
                elif evento.key == pygame.K_RETURN:
                    if escolha == 0:
                        progresso['som'] = not progresso['som']
                        salvar(progresso)
                        tocar_musica(progresso)
                    else:
                        return MENU

        som = 'Som: Desligado'
        if progresso['som']:
            som = 'Som: Ligado'
        opcoes = [som, 'Voltar']

        window.blit(assets['fundos']['lago'], (0, 0))
        painel(window, WIDTH // 2 - 250, 120, 500, 260)
        escrever(window, assets['fonte_grande'], 'Configurações', AMARELO, WIDTH // 2, 170)
        for i in range(len(opcoes)):
            cor = BRANCO
            if i == escolha:
                cor = AMARELO
            escrever(window, assets['fonte'], opcoes[i], cor, WIDTH // 2, 250 + i * 60)
        escrever(window, assets['fonte_pequena'], 'Setas: escolher    ENTER: mudar    ESC: voltar',
                 BRANCO, WIDTH // 2, HEIGHT - 30)
        pygame.display.update()
