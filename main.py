import pygame

from assets import carregar_assets, tocar_musica
from config import ARMAZEM, CONFIG, HEIGHT, LOJA, MAPA, MENU, MULTI, SAIR, SINGLE, TITULO, WIDTH
from dados import carregar, salvar
from tela_armazem import tela_armazem
from tela_config import tela_config
from tela_loja import tela_loja
from tela_mapa import tela_mapa
from tela_menu import tela_menu
from tela_multi import tela_multi
from tela_single import tela_single

# inicialização
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITULO)
assets = carregar_assets()
progresso = carregar()  
tocar_musica(progresso)
estado = MENU
while estado != SAIR:
    if estado == MENU:
        estado = tela_menu(window, assets)
    elif estado == SINGLE:
        estado = tela_single(window, assets, progresso)
    elif estado == ARMAZEM:
        estado = tela_armazem(window, assets, progresso)
    elif estado == LOJA:
        estado = tela_loja(window, assets, progresso)
    elif estado == MAPA:
        estado = tela_mapa(window, assets, progresso)
    elif estado == MULTI:
        estado = tela_multi(window, assets, progresso)
    elif estado == CONFIG:
        estado = tela_config(window, assets, progresso)

salvar(progresso)
pygame.quit()
