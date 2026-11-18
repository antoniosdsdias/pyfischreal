"""Singleplayer: o velho pescando sozinho, com dinheiro, vara, lugar e energético."""
import pygame


from assets import tocar
from config import (AMARELO, ARMAZEM, BRANCO, COR_RARIDADE, DURACAO_ENERGETICO, FPS, HEIGHT, LOJA,
                    LUGAR, MAPA, MENU, NOME_VARA, SAIR, VERDE, WIDTH)
from dados import guardar_peixe, salvar
from desenhos import escrever, painel
from pescador import Pescador
from tela_mapa import motivo_bloqueio


DICAS = {
    'parado': 'ESPAÇO: lançar a linha',
    'esperando': 'Espere o peixe morder...',
    'mordida': 'ESPAÇO quando o marcador estiver no verde!',
    'pegou': '',
    'errou': 'Espere para lançar de novo',
}




def tela_single(window, assets, progresso):
    """Loop da pesca sozinho. Devolve MENU, ARMAZEM, LOJA, MAPA ou SAIR."""
    clock = pygame.time.Clock()
    velho = Pescador(250, '', assets)
    velho.vara = progresso['vara']
    if motivo_bloqueio(progresso, progresso['lugar']) != '':
        progresso['lugar'] = 'lago'     # trocou para uma vara fraca demais para o mar
    velho.lugar = progresso['lugar']
    while True:
        clock.tick(FPS)
        agora = pygame.time.get_ticks()


        # trata eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return MENU
                if evento.key == pygame.K_a:
                    return ARMAZEM
                if evento.key == pygame.K_l:
                    return LOJA
                if evento.key == pygame.K_m:
                    return MAPA
                if evento.key == pygame.K_e:
                    usar_energetico(progresso, agora)
                if evento.key == pygame.K_SPACE:
                    resultado = velho.apertou(agora)
                    if resultado == 'lancou':
                        tocar(assets, progresso, 'lancar')
                    elif resultado == 'errou':
                        tocar(assets, progresso, 'errou')
                    elif resultado == 'pegou':
                        tocar(assets, progresso, 'pegou')
                        guardar_peixe(progresso, velho.ultimo_peixe)
                        salvar(progresso)


        # atualiza o estado do jogo
        velho.rapido = agora < progresso['energetico_ate']
        resultado = velho.update(agora)
        if resultado == 'mordeu':
            tocar(assets, progresso, 'mordida')
        elif resultado == 'errou':
            tocar(assets, progresso, 'errou')


        # gera saídas
        window.blit(assets['fundos'][velho.lugar], (0, 0))
        velho.desenhar(window, assets, agora)
        desenhar_painel(window, assets, progresso, velho, agora)
        escrever(window, assets['fonte_pequena'], 'A: armazém   L: loja   M: mapa   E: energético   ESC: menu',
                 BRANCO, WIDTH - 280, 25)
        escrever(window, assets['fonte'], DICAS[velho.estado], BRANCO, WIDTH // 2, HEIGHT - 30)
        pygame.display.update()

def usar_energetico(progresso, agora):
    """Gasta um energético e liga o efeito por 30 s (se não estiver ligado)."""
    if progresso['energeticos'] > 0 and agora >= progresso['energetico_ate']:
        progresso['energeticos'] -= 1
        progresso['energetico_ate'] = agora + DURACAO_ENERGETICO
        salvar(progresso)




def desenhar_painel(window, assets, progresso, velho, agora):
    """Caixa do canto: dinheiro, vara, lugar e energético."""
    painel(window, 12, 12, 270, 140)
    escrever(window, assets['fonte'], f'$ {progresso["dinheiro"]}', AMARELO, 147, 36)
    vara = progresso['vara']
    escrever(window, assets['fonte_pequena'], NOME_VARA[vara], COR_RARIDADE[vara], 147, 66)
    escrever(window, assets['fonte_pequena'], LUGAR[velho.lugar]['nome'], BRANCO, 147, 92)
    if velho.rapido:
        segundos = (progresso['energetico_ate'] - agora) // 1000 + 1
        escrever(window, assets['fonte_pequena'], f'Energético: {segundos} s', VERDE, 147, 120)
    else:
        escrever(window, assets['fonte_pequena'], f'Energéticos: {progresso["energeticos"]}', BRANCO, 147, 120)
