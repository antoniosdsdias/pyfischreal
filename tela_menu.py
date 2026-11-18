'''Tela inicial: nome do jogo e as opções.'''
import pygame

from config import AMARELO, BRANCO, CHAO_Y, CONFIG, FPS, MULTI, SAIR, SINGLE, TEMPO_QUADRO, TITULO, WIDTH
from desenhos import escrever

OPCOES = ['Singleplayer', 'Multiplayer', 'Configurações', 'Sair']
DESTINOS = [SINGLE, MULTI, CONFIG, SAIR]


def tela_menu(window, assets):
    '''Mostra o menu e devolve o estado escolhido.'''
    clock = pygame.time.Clock()
    escolha = 0
    while True:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    escolha = (escolha - 1) % len(OPCOES)
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    escolha = (escolha + 1) % len(OPCOES)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    return DESTINOS[escolha]
                elif evento.key == pygame.K_ESCAPE:
                    return SAIR
                
        quadro = (pygame.time.get_ticks() // TEMPO_QUADRO) % 4 #calcula o quadro atual da animação do velho parado
        velho = assets['velho_parado'][quadro] #pega o quadro atual da animação do velho parado
        window.blit(assets['fundos']['lago'], (0, 0)) #desenha o fundo
        window.blit(velho, (60, CHAO_Y - velho.get_height())) #desenha o velho parado
        escrever(window, assets['fonte_titulo'], TITULO, AMARELO, WIDTH // 2, 90) #escreve o título do jogo
        for i in range(len(OPCOES)):
            fonte = assets['fonte']
            cor = BRANCO
            if i == escolha:
                fonte = assets['fonte_grande'] #se a opção estiver selecionada, usa fonte maior e a cor amarela
                cor = AMARELO
            escrever(window, fonte, OPCOES[i], cor, WIDTH // 2, 180 + i * 50) # desenha a opcão do menu
        escrever(window, assets['fonte_pequena'], 'Setas ou W/S: escolher    ENTER: confirmar',
                 BRANCO, WIDTH // 2, 515) # mostra as instruções de como jogar
        pygame.display.update()