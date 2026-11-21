"""Armazém: todos os peixes do jogo em grade, com quantidade e venda."""
import pygame


from assets import tocar
from config import (AMARELO, BRANCO, COR_RARIDADE, FPS, HEIGHT, LUGAR, NOME_RARIDADE, PEIXES,
                    SAIR, SINGLE, WIDTH)
from dados import salvar
from desenhos import escrever, painel


COLUNAS = 7
CELULA = 105  # tamanho de cada quadrado da grade, em pixels




def tela_armazem(window, assets, progresso):
    """Mostra os peixes ('?' se nunca pescou) e vende com V ou T."""
    clock = pygame.time.Clock()
    nomes = []
    for nome in PEIXES:
        nomes.append(nome)
    escolha = 0
    while True:
        clock.tick(FPS)
        nome = nomes[escolha]
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_a:
                    return SINGLE
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    escolha = (escolha + 1) % len(nomes)
                elif evento.key == pygame.K_LEFT:
                    escolha = (escolha - 1) % len(nomes)
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    escolha = (escolha + COLUNAS) % len(nomes)
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    escolha = (escolha - COLUNAS) % len(nomes)
                elif evento.key == pygame.K_v:
                    vender(progresso, nome, 1, assets)
                elif evento.key == pygame.K_t and nome in progresso['armazem']:
                    vender(progresso, nome, progresso['armazem'][nome], assets)


        window.blit(assets['fundos'][progresso['lugar']], (0, 0))
        painel(window, 60, 15, WIDTH - 120, HEIGHT - 30)
        escrever(window, assets['fonte_grande'], 'Armazém', AMARELO, WIDTH // 2, 50)
        escrever(window, assets['fonte'], f'$ {progresso["dinheiro"]}', AMARELO, WIDTH - 170, 50)


        inicio_x = (WIDTH - COLUNAS * CELULA) // 2
        for i in range(len(nomes)):
            x = inicio_x + (i % COLUNAS) * CELULA
            y = 80 + (i // COLUNAS) * CELULA
            desenhar_celula(window, assets, progresso, nomes[i], x, y, i == escolha)


        desenhar_detalhes(window, assets, progresso, nome)
        escrever(window, assets['fonte_pequena'], 'Setas: escolher    V: vender 1    T: vender todos    ESC: voltar',
                 BRANCO, WIDTH // 2, HEIGHT - 35)
        pygame.display.update()




def desenhar_celula(window, assets, progresso, nome, x, y, selecionada):
    """Um quadrado da grade: o peixe se já pescou, '?' se não."""
    cor_fundo = (70, 60, 55)
    if selecionada:
        cor_fundo = (120, 100, 60)
    pygame.draw.rect(window, cor_fundo, (x + 4, y + 4, CELULA - 8, CELULA - 8))
    if nome in progresso['colecao']:
        pygame.draw.rect(window, COR_RARIDADE[PEIXES[nome]['raridade']], (x + 4, y + 4, CELULA - 8, CELULA - 8), 3)
        imagem = assets['peixes'][nome]
        window.blit(imagem, (x + CELULA // 2 - imagem.get_width() // 2, y + CELULA // 2 - imagem.get_height() // 2))
    else:
        escrever(window, assets['fonte_grande'], '?', BRANCO, x + CELULA // 2, y + CELULA // 2)
    if nome in progresso['armazem']:
        escrever(window, assets['fonte_pequena'], f'x{progresso["armazem"][nome]}', BRANCO,
                 x + CELULA - 26, y + CELULA - 20)
    if selecionada:
        pygame.draw.rect(window, AMARELO, (x, y, CELULA, CELULA), 3)




def desenhar_detalhes(window, assets, progresso, nome):
    """Linha de baixo com nome, raridade, preço e quantidade do peixe escolhido."""
    y = HEIGHT - 100
    lugar = 'Todos os lugares'
    if PEIXES[nome]['lugar'] != 'todos':
        lugar = LUGAR[PEIXES[nome]['lugar']]['nome']
    if nome not in progresso['colecao']:
        escrever(window, assets['fonte'], '??? (ainda não pescado)', BRANCO, WIDTH // 2, y)
        escrever(window, assets['fonte_pequena'], f'Onde: {lugar}', BRANCO, WIDTH // 2, y + 28)
        return
    raridade = PEIXES[nome]['raridade']
    quantidade = 0
    if nome in progresso['armazem']:
        quantidade = progresso['armazem'][nome]
    texto = f'{nome}  ·  {NOME_RARIDADE[raridade]}  ·  $ {PEIXES[nome]["preco"]} cada  ·  guardados: {quantidade}'
    escrever(window, assets['fonte'], texto, COR_RARIDADE[raridade], WIDTH // 2, y)
    escrever(window, assets['fonte_pequena'], f'Onde: {lugar}', BRANCO, WIDTH // 2, y + 28)




def vender(progresso, nome, quantidade, assets):
    """Vende peixes do armazém e soma o dinheiro."""
    if nome not in progresso['armazem'] or quantidade <= 0:
        return
    progresso['armazem'][nome] -= quantidade
    progresso['dinheiro'] += PEIXES[nome]['preco'] * quantidade
    if progresso['armazem'][nome] == 0:
        del progresso['armazem'][nome]
    tocar(assets, progresso, 'moeda')
    salvar(progresso)
