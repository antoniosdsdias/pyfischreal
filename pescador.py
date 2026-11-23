"""Classe Pescador: o velho animado, os estados da pesca e a barra do timing."""
import random

import pygame

from config import (AGUA_Y, AMARELO, BARRA_LARGURA, BRANCO, CHANCES, CHAO_Y, COR_RARIDADE, LUGAR,
                    NIVEL_RARIDADE, PEIXES, PERFEITO_LARGURA, PERFEITO_LARGURA_CERVEJA, PRETO,
                    RARIDADES, TEMPO_CASTIGO, TEMPO_MOSTRA_PEIXE, TEMPO_QUADRO, VERDE, VERMELHO,
                    ZONA_LARGURA)
from desenhos import escrever


def sortear_raridade(vara):
    """Sorteia uma raridade com as chances da vara (fichas de 1 a 1000)."""
    sorteio = random.randint(1, 1000)
    acumulado = 0
    for raridade in RARIDADES:
        acumulado += CHANCES[vara][raridade]
        if sorteio <= acumulado:
            return raridade
    return 'comum'


def sortear_peixe(vara, sorteios, lugar):
    """Sorteia a raridade 'sorteios' vezes, fica com a melhor e escolhe um peixe do lugar."""
    raridade = sortear_raridade(vara)
    for i in range(sorteios - 1):
        outra = sortear_raridade(vara)
        if NIVEL_RARIDADE[outra] > NIVEL_RARIDADE[raridade]:
            raridade = outra
    opcoes = []
    for nome in PEIXES:
        peixe = PEIXES[nome]
        if peixe['raridade'] == raridade and (peixe['lugar'] == lugar or peixe['lugar'] == 'todos'):
            opcoes.append(nome)
    return opcoes[random.randint(0, len(opcoes) - 1)]


def avaliar_timing(marcador, zona, perfeito):
    """Diz se o aperto foi 'perfeito', 'bom' ou 'errou', pela posição do marcador na barra."""
    meio = zona + ZONA_LARGURA // 2
    if marcador >= meio - perfeito // 2 and marcador <= meio + perfeito // 2:
        return 'perfeito'
    if marcador >= zona and marcador <= zona + ZONA_LARGURA:
        return 'bom'
    return 'errou'


class Pescador(pygame.sprite.Sprite):
    """Um velho pescando. Estados: parado, esperando, mordida, pegou e errou."""

    def __init__(self, x, nome, assets):
        """Cria o pescador em pé no píer, na posição x."""
        pygame.sprite.Sprite.__init__(self)        # construtor da classe mãe (Sprite)
        self.parado = assets['velho_parado']       # 4 imagens de cada animação
        self.pescando = assets['velho_pescando']   # já com a linha e a boia na água
        self.mordida = assets['velho_mordida']     # boia afundando
        if nome == 'J2':                           # o J2 usa o velho de cores invertidas
            self.parado = assets['velho2_parado']
            self.pescando = assets['velho2_pescando']
            self.mordida = assets['velho2_mordida']
        self.image = self.parado[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = CHAO_Y  + 13                # pé no píer
        self.boia_x = x + 250                      # onde a boia fica (mensagens em cima dela)
        self.nome = nome                           # 'J1', 'J2' ou '' no singleplayer
        self.vara = 'comum'
        self.lugar = 'lago'
        self.cerveja = False                       # True enquanto a cerveja faz efeito
        self.estado = 'parado'
        self.inicio = 0                            # instante (ms) em que entrou no estado atual
        self.espera = 0                            # quanto o peixe vai demorar para morder
        self.zona = 0                              # onde começa a parte verde da barra
        self.ultimo_peixe = ''
        self.ultimo_acerto = ''                    # 'perfeito', 'bom', 'cedo', 'errou' ou 'tarde'
        self.peixes = []                           # peixes pescados nesta partida

    def mudar(self, estado, agora):
        """Troca de estado e guarda a hora da troca."""
        self.estado = estado
        self.inicio = agora

    def marcador(self, agora):
        """Posição do marcador na barra, de 0 até BARRA_LARGURA."""
        return (agora - self.inicio) * BARRA_LARGURA // LUGAR[self.lugar]['tempo_barra']

    def largura_perfeito(self):
        """Tamanho do meio amarelo da barra: menor com cerveja."""
        if self.cerveja:
            return PERFEITO_LARGURA_CERVEJA
        return PERFEITO_LARGURA

    def apertou(self, agora):
        """Reage à tecla de pesca. Devolve 'lancou', 'pegou', 'errou' ou None."""
        if self.estado == 'parado':
            self.espera = random.randint(LUGAR[self.lugar]['espera_min'], LUGAR[self.lugar]['espera_max'])
            if self.cerveja:
                self.espera = self.espera * 2 // 3   # cerveja: 50% mais rápido
            self.mudar('esperando', agora)
            return 'lancou'
        if self.estado == 'esperando':
            self.ultimo_acerto = 'cedo'
            self.mudar('errou', agora)
            return 'errou'
        if self.estado == 'mordida':
            resultado = avaliar_timing(self.marcador(agora), self.zona, self.largura_perfeito())
            if resultado == 'errou':
                self.ultimo_acerto = 'errou'
                self.mudar('errou', agora)
                return 'errou'
            self.ultimo_acerto = resultado
            sorteios = 1                           # cada sorteio a mais é uma chance de peixe melhor
            if resultado == 'perfeito':
                sorteios += 1
            if self.cerveja:
                sorteios += 1                      # cerveja: mais sorte
            self.ultimo_peixe = sortear_peixe(self.vara, sorteios, self.lugar)
            self.peixes.append(self.ultimo_peixe)
            self.mudar('pegou', agora)
            return 'pegou'
        return None                                # pegou ou errou: a tecla não faz nada

    def update(self, agora):
        """Chamado a cada quadro: avança no tempo e escolhe a imagem. Devolve 'mordeu', 'errou' ou None."""
        aviso = None
        tempo = agora - self.inicio
        if self.estado == 'esperando' and tempo >= self.espera:
            self.zona = random.randint(40, BARRA_LARGURA - ZONA_LARGURA)   # sorteia a parte verde
            self.mudar('mordida', agora)
            aviso = 'mordeu'
        elif self.estado == 'mordida' and self.marcador(agora) > BARRA_LARGURA:
            self.ultimo_acerto = 'tarde'
            self.mudar('errou', agora)
            aviso = 'errou'
        elif self.estado == 'pegou' and tempo >= TEMPO_MOSTRA_PEIXE:
            self.mudar('parado', agora)
        elif self.estado == 'errou' and tempo >= TEMPO_CASTIGO:
            self.mudar('parado', agora)

        quadro = (agora // TEMPO_QUADRO) % 4       # 0, 1, 2, 3, 0... a cada 200 ms
        if self.estado == 'esperando':
            self.image = self.pescando[quadro]
        elif self.estado == 'mordida':
            self.image = self.mordida[quadro]
        else:
            self.image = self.parado[quadro]
        return aviso

    def desenhar(self, window, assets, agora):
        """Desenha o velho e, por cima, o nome, a barra e as mensagens."""
        window.blit(self.image, self.rect)
        if self.nome != '':
            escrever(window, assets['fonte'], self.nome, AMARELO, self.rect.x + 50, self.rect.y + 20)

        if self.estado == 'mordida':
            escrever(window, assets['fonte_grande'], '!', AMARELO, self.boia_x, AGUA_Y - 50)
            self.desenhar_barra(window, agora, self.boia_x - BARRA_LARGURA // 2, AGUA_Y - 110)

        if self.estado == 'pegou':
            peixe = assets['peixes'][self.ultimo_peixe]
            window.blit(peixe, (self.boia_x - peixe.get_width() // 2, AGUA_Y - 170))
            cor = COR_RARIDADE[PEIXES[self.ultimo_peixe]['raridade']]
            escrever(window, assets['fonte'], self.ultimo_peixe, cor, self.boia_x, AGUA_Y - 90)
            if self.ultimo_acerto == 'perfeito':
                escrever(window, assets['fonte_pequena'], 'PERFEITO!', AMARELO, self.boia_x, AGUA_Y - 65)

        if self.estado == 'errou':
            texto = 'Escapou!'
            if self.ultimo_acerto == 'cedo':
                texto = 'Cedo demais!'
            escrever(window, assets['fonte'], texto, VERMELHO, self.boia_x, AGUA_Y - 90)

    def desenhar_barra(self, window, agora, x, y):
        """Barra do timing: vermelho = erro, verde = acerto, amarelo = perfeito, branco = marcador."""
        pygame.draw.rect(window, PRETO, (x - 3, y - 3, BARRA_LARGURA + 6, 24))
        pygame.draw.rect(window, VERMELHO, (x, y, BARRA_LARGURA, 18))
        pygame.draw.rect(window, VERDE, (x + self.zona, y, ZONA_LARGURA, 18))
        meio = self.zona + ZONA_LARGURA // 2
        perfeito = self.largura_perfeito()
        pygame.draw.rect(window, AMARELO, (x + meio - perfeito // 2, y, perfeito, 18))
        pygame.draw.rect(window, BRANCO, (x + self.marcador(agora) - 2, y - 6, 4, 30))
