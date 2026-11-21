"""Singleplayer: o velho pescando sozinho, com dinheiro, vara, lugar e cerveja."""
import pygame


from assets import tocar
from config import (AMARELO, ARMAZEM, BALANCO, BRANCO, CERVEJAS_PARA_BEBADO, COR_RARIDADE,
                    DURACAO_CERVEJA, FPS, HEIGHT, LOJA, LUGAR, MAPA, MENU, NOME_VARA, SAIR,
                    TEMPO_BALANCO, VERMELHO, WIDTH)
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
                if evento.key == pygame.K_b:
                    beber_cerveja(progresso, agora)
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
        velho.cerveja = agora < progresso['cerveja_ate']
        bebado = velho.cerveja and progresso['cervejas_seguidas'] >= CERVEJAS_PARA_BEBADO
        resultado = velho.update(agora)
        if resultado == 'mordeu':
            tocar(assets, progresso, 'mordida')
        elif resultado == 'errou':
            tocar(assets, progresso, 'errou')


        # gera saídas
        window.blit(assets['fundos'][velho.lugar], (0, 0))
        velho.desenhar(window, assets, agora)
        desenhar_painel(window, assets, progresso, velho, bebado, agora)
        escrever(window, assets['fonte_pequena'], 'A: armazém   L: loja   M: mapa   B: beber cerveja   ESC: menu',
                 BRANCO, WIDTH - 270, 25)
        escrever(window, assets['fonte'], DICAS[velho.estado], BRANCO, WIDTH // 2, HEIGHT - 30)

        # bêbado: a imagem da janela é empurrada um pouco, seguindo a lista BALANCO
        if bebado:
            i = (agora // TEMPO_BALANCO) % len(BALANCO)
            window.scroll(BALANCO[i], BALANCO[(i + 3) % len(BALANCO)] // 2)
        pygame.display.update()

def beber_cerveja(progresso, agora):
    """Bebe 1 cerveja: o efeito dura 30 s; bebendo antes de acabar, soma mais 30 s e conta seguida."""
    if progresso['cervejas'] == 0:
        return
    progresso['cervejas'] -= 1
    if agora < progresso['cerveja_ate']:       # ainda está com efeito: cerveja seguida
        progresso['cerveja_ate'] += DURACAO_CERVEJA
        progresso['cervejas_seguidas'] += 1
    else:
        progresso['cerveja_ate'] = agora + DURACAO_CERVEJA
        progresso['cervejas_seguidas'] = 1
    salvar(progresso)




def desenhar_painel(window, assets, progresso, velho, bebado, agora):
    """Caixa do canto: dinheiro, vara, lugar e cerveja."""
    painel(window, 12, 12, 270, 140)
    escrever(window, assets['fonte'], f'$ {progresso["dinheiro"]}', AMARELO, 147, 36)
    vara = progresso['vara']
    escrever(window, assets['fonte_pequena'], NOME_VARA[vara], COR_RARIDADE[vara], 147, 66)
    escrever(window, assets['fonte_pequena'], LUGAR[velho.lugar]['nome'], BRANCO, 147, 92)
    if velho.cerveja:
        segundos = (progresso['cerveja_ate'] - agora) // 1000 + 1
        texto = f'Cerveja: {segundos} s'
        cor = AMARELO
        if bebado:
            texto = f'Bêbado! {segundos} s'
            cor = VERMELHO
        escrever(window, assets['fonte_pequena'], texto, cor, 147, 120)
    else:
        escrever(window, assets['fonte_pequena'], f'Cervejas: {progresso["cervejas"]}', BRANCO, 147, 120)
