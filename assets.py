"""Carrega fontes, imagens e sons uma vez só, num dicionário, e toca os sons e a música."""
from os import path

import pygame

from config import ARQUIVO_MUSICA, LUGARES, PEIXES


def carregar_assets():
    """Devolve o dicionário com tudo que o jogo usa (precisa da janela já criada)."""
    assets = {}

    # fontes (None = a fonte padrão do pygame)
    assets['fonte_titulo'] = pygame.font.SysFont(None, 110)
    assets['fonte_grande'] = pygame.font.SysFont(None, 60)
    assets['fonte'] = pygame.font.SysFont(None, 34)
    assets['fonte_pequena'] = pygame.font.SysFont(None, 24)

    # um fundo para cada lugar (sem transparência: convert)
    assets['fundos'] = {}
    for lugar in LUGARES:
        assets['fundos'][lugar] = pygame.image.load('assets/img/fundos/' + lugar + '.png').convert()

    # animações do velho: 4 imagens para cada momento da pesca
    assets['velho_parado'] = []
    assets['velho_pescando'] = []
    assets['velho_mordida'] = []
    for i in range(4):
        assets['velho_parado'].append(pygame.image.load('assets/img/velho/parado' + str(i) + '.png').convert_alpha())
        assets['velho_pescando'].append(pygame.image.load('assets/img/velho/pescando' + str(i) + '.png').convert_alpha())
        assets['velho_mordida'].append(pygame.image.load('assets/img/velho/mordida' + str(i) + '.png').convert_alpha())

    # o J2 do multiplayer: o mesmo velho com as cores invertidas (pasta velho2)
    assets['velho2_parado'] = []
    assets['velho2_pescando'] = []
    assets['velho2_mordida'] = []
    for i in range(4):
        assets['velho2_parado'].append(pygame.image.load('assets/img/velho2/parado' + str(i) + '.png').convert_alpha())
        assets['velho2_pescando'].append(pygame.image.load('assets/img/velho2/pescando' + str(i) + '.png').convert_alpha())
        assets['velho2_mordida'].append(pygame.image.load('assets/img/velho2/mordida' + str(i) + '.png').convert_alpha())
    assets['pier'] = pygame.image.load('assets/img/pier.png').convert_alpha()   # píer embaixo do J2

    # um desenho para cada peixe; o nome do arquivo vem do config (PEIXES[nome]['imagem'])
    assets['peixes'] = {}
    for nome in PEIXES:
        arquivo = 'assets/img/peixes/' + PEIXES[nome]['imagem'] + '.png'
        assets['peixes'][nome] = pygame.image.load(arquivo).convert_alpha()

    # itens da loja (com fundo transparente: convert_alpha)
    assets['vara'] = pygame.image.load('assets/img/vara.png').convert_alpha()
    assets['cerveja'] = pygame.image.load('assets/img/cerveja.png').convert_alpha()

    # efeitos sonoros curtos
    assets['sons'] = {}
    for nome in ['lancar', 'mordida', 'pegou', 'errou', 'moeda']:
        assets['sons'][nome] = pygame.mixer.Sound('assets/sons/' + nome + '.ogg')
    return assets


def tocar(assets, progresso, nome):
    """Toca um efeito sonoro, se o som estiver ligado nas configurações."""
    if progresso['som']:
        assets['sons'][nome].play()


def tocar_musica(progresso):
    """Toca a música de fundo sem parar; se o som estiver desligado, para."""
    if not path.exists(ARQUIVO_MUSICA):
        return  # sem o arquivo da música, o jogo roda sem ela
    if progresso['som']:
        pygame.mixer.music.load(ARQUIVO_MUSICA)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  # -1 = repetir para sempre
    else:
        pygame.mixer.music.stop()
