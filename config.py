"""Constantes do jogo: janela, cores, lugares, peixes, varas, chances, tempos e estados."""

# janela
TITULO = 'Pyfish'
WIDTH = 960
HEIGHT = 540
FPS = 60

# arquivos (o jogo é aberto de dentro da pasta dele)
ARQUIVO_SAVE = 'save.json'
ARQUIVO_MUSICA = 'background music pygame.mp3'

# cenário (posição em pixels, combina com as imagens de fundo)
CHAO_Y = 384    # altura do píer onde o velho pisa
AGUA_Y = 400    # superfície da água (barra e mensagens ficam acima dela)

# cores (R, G, B)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 220, 60)
VERMELHO = (220, 60, 60)
VERDE = (70, 200, 90)
FUNDO_PAINEL = (40, 30, 25)
BORDA_PAINEL = (190, 140, 70)

# raridades: nome que aparece na tela e cor
RARIDADES = ['comum', 'raro', 'epico', 'lendario', 'especial']
NOME_RARIDADE = {'comum': 'Comum', 'raro': 'Raro', 'epico': 'Épico',
                 'lendario': 'Lendário', 'especial': 'Especial'}
COR_RARIDADE = {'comum': (160, 160, 170), 'raro': (70, 140, 255), 'epico': (170, 80, 230),
                'lendario': (255, 200, 40), 'especial': (255, 80, 200)}
NIVEL_RARIDADE = {'comum': 0, 'raro': 1, 'epico': 2, 'lendario': 3, 'especial': 4}  # para comparar qual é melhor

# lugares de pesca: nome, descrição e tempos (em milissegundos)
LUGARES = ['lago', 'rio', 'mar', 'lixao']
LUGAR = {
    'lago': {'nome': 'Lago Urbano', 'descricao': 'Peixes fáceis. Morde rápido, vale pouco.',
             'espera_min': 1000, 'espera_max': 2500, 'tempo_barra': 1600},
    'rio': {'nome': 'Rio de Corredeira', 'descricao': 'Peixes ágeis: o marcador é mais rápido.',
            'espera_min': 1500, 'espera_max': 4000, 'tempo_barra': 1000},
    'mar': {'nome': 'Mar Aberto', 'descricao': 'Peixes gigantes. Demora, mas vale muito.',
            'espera_min': 3000, 'espera_max': 6500, 'tempo_barra': 1300},
    'lixao': {'nome': 'Lixão', 'descricao': 'Em vez de peixe, lixo para reciclar.',
              'espera_min': 1500, 'espera_max': 4000, 'tempo_barra': 1400},
}
PEIXES_PARA_LIXAO = 30  # quantos peixes pescar para descobrir o lixão

# peixes (e lixos): onde aparecem, raridade, preço e nome da imagem em assets/img/peixes
PEIXES = {
    'Lambari': {'lugar': 'lago', 'raridade': 'comum', 'preco': 3, 'imagem': 'lambari'},
    'Carpa': {'lugar': 'lago', 'raridade': 'raro', 'preco': 15, 'imagem': 'carpa'},
    'Tilápia': {'lugar': 'lago', 'raridade': 'epico', 'preco': 40, 'imagem': 'tilapia'},
    'Tambaqui': {'lugar': 'lago', 'raridade': 'lendario', 'preco': 120, 'imagem': 'tambaqui'},
    'Piaba': {'lugar': 'rio', 'raridade': 'comum', 'preco': 5, 'imagem': 'piaba'},
    'Truta': {'lugar': 'rio', 'raridade': 'raro', 'preco': 25, 'imagem': 'truta'},
    'Dourado': {'lugar': 'rio', 'raridade': 'epico', 'preco': 90, 'imagem': 'dourado'},
    'Pirarucu': {'lugar': 'rio', 'raridade': 'lendario', 'preco': 300, 'imagem': 'pirarucu'},
    'Sardinha': {'lugar': 'mar', 'raridade': 'comum', 'preco': 15, 'imagem': 'sardinha'},
    'Atum': {'lugar': 'mar', 'raridade': 'raro', 'preco': 70, 'imagem': 'atum'},
    'Peixe-Espada': {'lugar': 'mar', 'raridade': 'epico', 'preco': 200, 'imagem': 'peixe_espada'},
    'Tubarão': {'lugar': 'mar', 'raridade': 'lendario', 'preco': 600, 'imagem': 'tubarao'},
    'Lata': {'lugar': 'lixao', 'raridade': 'comum', 'preco': 2, 'imagem': 'lata'},
    'Bota Velha': {'lugar': 'lixao', 'raridade': 'raro', 'preco': 4, 'imagem': 'bota'},
    'Pneu': {'lugar': 'lixao', 'raridade': 'epico', 'preco': 8, 'imagem': 'pneu'},
    'Baú': {'lugar': 'lixao', 'raridade': 'lendario', 'preco': 150, 'imagem': 'bau'},
    'Peixe Especial': {'lugar': 'todos', 'raridade': 'especial', 'preco': 1000, 'imagem': 'especial'},
}

# varas: as mesmas 4 classes dos peixes
VARAS = ['comum', 'raro', 'epico', 'lendario']
NOME_VARA = {'comum': 'Vara Comum', 'raro': 'Vara Rara', 'epico': 'Vara Épica',
             'lendario': 'Vara Lendária'}
PRECO_VARA = {'comum': 0, 'raro': 150, 'epico': 600, 'lendario': 2000}

# chances de cada raridade, em "fichas" de um total de 1000, para cada vara
CHANCES = {
    'comum': {'comum': 700, 'raro': 230, 'epico': 55, 'lendario': 14, 'especial': 1},
    'raro': {'comum': 560, 'raro': 310, 'epico': 100, 'lendario': 28, 'especial': 2},
    'epico': {'comum': 430, 'raro': 350, 'epico': 160, 'lendario': 55, 'especial': 5},
    'lendario': {'comum': 300, 'raro': 360, 'epico': 230, 'lendario': 100, 'especial': 10},
}

# cerveja: por 30 s a pesca fica 50% mais rápida e com mais sorte, mas o perfeito fica menor
PRECO_CERVEJA = 20
DURACAO_CERVEJA = 30000
PERFEITO_LARGURA_CERVEJA = 6    # meio amarelo da barra com cerveja (sem cerveja: PERFEITO_LARGURA)
CERVEJAS_PARA_BEBADO = 2        # a partir de 2 cervejas seguidas a tela balança
BALANCO = [0, 2, 4, 6, 4, 2, 0, -2, -4, -6, -4, -2]   # quanto a tela anda, em pixels, quando está bêbado

# tempos da pesca, em milissegundos (espera e barra mudam com o lugar)
TEMPO_MOSTRA_PEIXE = 1500
TEMPO_CASTIGO = 2000    # errou o timing: 2 s sem poder lançar
TEMPO_MULTI = 60000     # partida do multiplayer: 1 minuto
TEMPO_QUADRO = 200      # animação do velho: troca de imagem a cada 200 ms
TEMPO_BALANCO = 90     # bêbado: a tela muda de posição a cada 90 ms

# barra do timing (em pixels)
BARRA_LARGURA = 200
ZONA_LARGURA = 60       # parte verde: acertou
PERFEITO_LARGURA = 10   # meio da parte verde: perfeito

# estados (telas)
SAIR = 0
MENU = 1
SINGLE = 2
MULTI = 3
CONFIG = 4
ARMAZEM = 5
LOJA = 6
MAPA = 7
