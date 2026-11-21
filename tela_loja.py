"""Loja: comprar varas, escolher qual usar e comprar energéticos."""
import pygame


from assets import tocar
from config import (AMARELO, BRANCO, CHANCES, COR_RARIDADE, FPS, HEIGHT, NOME_VARA,
                    PRECO_ENERGETICO, PRECO_VARA, SAIR, SINGLE, VARAS, VERDE, VERMELHO, WIDTH)
from dados import salvar
from desenhos import escrever, painel


ITENS = VARAS + ['energetico']   # as 4 varas e, por último, o energético
ALTURA_LINHA = 66




def tela_loja(window, assets, progresso):
    """Lista os itens; ENTER compra (ou passa a usar a vara, se já tiver)."""
    clock = pygame.time.Clock()
    escolha = 0
    mensagem = ''
    while True:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_l:
                    return SINGLE
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    escolha = (escolha - 1) % len(ITENS)
                    mensagem = ''
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    escolha = (escolha + 1) % len(ITENS)
                    mensagem = ''
                elif evento.key == pygame.K_RETURN:
                    if ITENS[escolha] == 'energetico':
                        mensagem = comprar_energetico(progresso, assets)
                    else:
                        mensagem = comprar_ou_usar(progresso, ITENS[escolha], assets)


        window.blit(assets['fundos'][progresso['lugar']], (0, 0))
        painel(window, 120, 15, WIDTH - 240, HEIGHT - 30)
        escrever(window, assets['fonte_grande'], 'Loja', AMARELO, WIDTH // 2, 62)
        escrever(window, assets['fonte'], f'$ {progresso["dinheiro"]}', AMARELO, WIDTH - 220, 62)
        for i in range(len(ITENS)):
            y = 100 + i * ALTURA_LINHA
            if ITENS[i] == 'energetico':
                desenhar_energetico(window, assets, progresso, y, i == escolha)
            else:
                desenhar_vara(window, assets, progresso, ITENS[i], y, i == escolha)
        cor = VERDE
        if mensagem == 'Dinheiro insuficiente':
            cor = VERMELHO
        escrever(window, assets['fonte'], mensagem, cor, WIDTH // 2, HEIGHT - 68)
        escrever(window, assets['fonte_pequena'], 'Setas: escolher    ENTER: comprar / usar    ESC: voltar',
                 BRANCO, WIDTH // 2, HEIGHT - 40)
        pygame.display.update()




def desenhar_fundo_linha(window, y, selecionada):
    """Destaque amarelo atrás da linha escolhida."""
    if selecionada:
        pygame.draw.rect(window, (90, 70, 45), (150, y, WIDTH - 300, ALTURA_LINHA - 6))
        pygame.draw.rect(window, AMARELO, (150, y, WIDTH - 300, ALTURA_LINHA - 6), 3)




def desenhar_vara(window, assets, progresso, vara, y, selecionada):
    """Uma vara: desenho, nome, chances e preço (ou se já é sua)."""
    desenhar_fundo_linha(window, y, selecionada)
    window.blit(assets['vara'], (170, y + 3))
    escrever(window, assets['fonte'], NOME_VARA[vara], COR_RARIDADE[vara], 340, y + 18)
    chances = CHANCES[vara]
    texto = f'Épico {chances["epico"] / 10}%   Lendário {chances["lendario"] / 10}%   Especial {chances["especial"] / 10}%'
    escrever(window, assets['fonte_pequena'], texto, BRANCO, 400, y + 43)
    if progresso['vara'] == vara:
        situacao = 'Em uso'
    elif vara in progresso['varas']:
        situacao = 'Comprada'
    else:
        situacao = f'$ {PRECO_VARA[vara]}'
    escrever(window, assets['fonte'], situacao, AMARELO, WIDTH - 230, y + 30)




def desenhar_energetico(window, assets, progresso, y, selecionada):
    """O energético: o que faz, quantos você tem e o preço."""
    desenhar_fundo_linha(window, y, selecionada)
    window.blit(assets['energetico'], (170, y + 3))
    escrever(window, assets['fonte'], 'Energético', VERDE, 340, y + 18)
    escrever(window, assets['fonte_pequena'], f'Pesca 50% mais rápida por 30 s (tecla E). Você tem {progresso["energeticos"]}.',
             BRANCO, 440, y + 43)
    escrever(window, assets['fonte'], f'$ {PRECO_ENERGETICO}', AMARELO, WIDTH - 230, y + 30)




def comprar_ou_usar(progresso, vara, assets):
    """Compra a vara (se tiver dinheiro) ou passa a usá-la. Devolve a mensagem."""
    if vara in progresso['varas']:
        progresso['vara'] = vara
        salvar(progresso)
        return f'Usando a {NOME_VARA[vara]}'
    if progresso['dinheiro'] < PRECO_VARA[vara]:
        return 'Dinheiro insuficiente'
    progresso['dinheiro'] -= PRECO_VARA[vara]
    progresso['varas'].append(vara)
    progresso['vara'] = vara
    tocar(assets, progresso, 'moeda')
    salvar(progresso)
    return f'Comprou a {NOME_VARA[vara]}!'




def comprar_energetico(progresso, assets):
    """Compra 1 energético, se tiver dinheiro. Devolve a mensagem."""
    if progresso['dinheiro'] < PRECO_ENERGETICO:
        return 'Dinheiro insuficiente'
    progresso['dinheiro'] -= PRECO_ENERGETICO
    progresso['energeticos'] += 1
    tocar(assets, progresso, 'moeda')
    salvar(progresso)
    return 'Comprou 1 energético! Use com a tecla E.'
