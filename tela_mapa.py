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


def tela_mapa(window, assets, progresso):
    """Lista os 4 lugares. Setas escolhem, ENTER vai para o lugar, ESC volta."""
    clock = pygame.time.Clock()
    escolha = 0
    mensagem = ''
    while True:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR #fecha jogo
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_m: #esc ou m
                    return SINGLE #singplayer
                if evento.key == pygame.K_UP or evento.key == pygame.K_w: #seta pra cima ou w
                    escolha = (escolha - 1) % len(LUGARES) #Diminui o índice para selecionar o lugar anterior
                    mensagem = ''
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s: #seta pra baixo ou s
                    escolha = (escolha + 1) % len(LUGARES) #Aumenta o índice para selecionar o lugar seguinte
                    mensagem = ''
                elif evento.key == pygame.K_RETURN:
                    lugar = LUGARES[escolha]
                    mensagem = motivo_bloqueio(progresso, lugar)#pega funcao anteiror para saber se pode ir ou não
                    if mensagem == '': #ta liberado
                        progresso['lugar'] = lugar
                        salvar(progresso)
                        return SINGLE

        window.blit(assets['fundos'][progresso['lugar']], (0, 0))
        painel(window, 120, 20, WIDTH - 240, HEIGHT - 40)
        escrever(window, assets['fonte_grande'], 'Mapa', AMARELO, WIDTH // 2, 60)
        for i in range(len(LUGARES)):
            desenhar_lugar(window, assets, progresso, LUGARES[i], 100 + i * ALTURA_LINHA, i == escolha)
        escrever(window, assets['fonte'], mensagem, VERMELHO, WIDTH // 2, HEIGHT - 75)
        escrever(window, assets['fonte_pequena'], 'Setas: escolher    ENTER: ir    ESC: voltar',
                 BRANCO, WIDTH // 2, HEIGHT - 42)
        pygame.display.update()


def desenhar_lugar(window, assets, progresso, lugar, y, selecionado):
    "Uma linha do mapa: nome, descrição e se está liberado."
    if selecionado:
        pygame.draw.rect(window, AMARELO, (150, y, WIDTH - 300, ALTURA_LINHA - 8), 3) #desenha um retângulo amarelo ao redor do lugar selecionado
    bloqueio = motivo_bloqueio(progresso, lugar) # pega o motivo pelo qual não se pode pescar no lugar
    nome = LUGAR[lugar]['nome']
    descricao = LUGAR[lugar]['descricao']
    if lugar == 'lixao' and bloqueio != '': #se o lugar for o lixão e estiver bloqueado, mostra um nome e descrição diferente
        nome = '???'
        descricao = 'Um lugar secreto...'
    if progresso['lugar'] == lugar: #se lugar for o mesmo que o progresso, mostra que o jogador está lá
        nome = nome + '  (você está aqui)'
    escrever(window, assets['fonte'], nome, AMARELO, WIDTH // 2, y + 20) #nome em amarelo
    escrever(window, assets['fonte_pequena'], descricao, BRANCO, WIDTH // 2, y + 45) # descrição em branco
    if bloqueio != '':
        escrever(window, assets['fonte_pequena'], bloqueio, VERMELHO, WIDTH // 2, y + 67) #se estiver bloqueado, mostra o motivo em vermelho