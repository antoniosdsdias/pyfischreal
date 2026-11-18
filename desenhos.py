"""Funções pequenas de desenho usadas em todas as telas: texto e caixa."""
import pygame

from config import BORDA_PAINEL, FUNDO_PAINEL, PRETO


def escrever(window, fonte, texto, cor, centro_x, centro_y):
    '''Escreve um texto centralizado, com sombra preta para ler em qualquer fundo.'''
    sombra = fonte.render(texto, True, PRETO)
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect()
    retangulo.centerx = centro_x
    retangulo.centery = centro_y
    window.blit(sombra, (retangulo.x + 2, retangulo.y + 2))
    window.blit(imagem, retangulo)


def painel(window, x, y, largura, altura):
    '''Caixa marrom com borda, usada no armazém, na loja, no mapa e nas mensagens.'''
    pygame.draw.rect(window, FUNDO_PAINEL, (x, y, largura, altura))
    pygame.draw.rect(window, BORDA_PAINEL, (x, y, largura, altura), 4)
