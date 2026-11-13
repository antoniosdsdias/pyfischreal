# Pyfish

Projeto Final de **Design de Software** — Insper, 2026.2.

## Integrantes

- Antônio Dias
- Marcos Rodrigues
- João Victor Peixoto

## Descrição
Jogo de pesca em 2D feito com Python e Pygame. Um velho de chapéu pesca na margem: aperte a tecla na hora certa para fisgar o peixe. Quanto melhor o timing e a vara, mais raro o peixe. Os peixes vão para o armazém, podem ser vendidos, e o dinheiro compra varas melhores e energéticos. São 4 lugares de pesca, um deles secreto.
No **multiplayer**, duas pessoas no mesmo teclado têm 1 minuto para pescar o máximo de peixes.
## Vídeo

*(link do vídeo do jogo funcionando)*

## Como instalar e jogar
Precisa de Python 3.10 ou mais novo.
```bash
pip install -r requirements.txt
python main.py
```
O arquivo a executar é o **`main.py`**. Usamos o **pygame-ce** (é o mesmo `import pygame`; tem versão pronta para o Python mais novo).
| Ação | Tecla |
|---|---|
| Andar nos menus | setas ou W/S, ENTER |
| Pescar (singleplayer e J1) | ESPAÇO |
| Pescar (J2 no multiplayer) | ENTER |
| Armazém / loja / mapa | A / L / M |
| Usar energético | E |
| Vender 1 / vender todos (no armazém) | V / T |
| Voltar | ESC |
## Regras do jogo
**A pesca.** ESPAÇO lança a linha. Depois de um tempo sorteado, o peixe morde: aparece "!" e uma barra com um marcador que anda da esquerda para a direita.
- Apertar no **amarelo** = perfeito; no **verde** = bom; no vermelho = errou.
- Apertar antes da mordida, errar ou demorar demais faz o peixe escapar e dá **2 segundos de castigo** sem poder lançar.
**Raridades.** Comum (cinza), raro (azul), épico (roxo), lendário (dourado) e **especial** (rosa, o mais raro). Cada vara tem "fichas" de 1000 para cada raridade, e o jogo sorteia um número de 1 a 1000. Com acerto **perfeito**, o jogo sorteia duas vezes e fica com o melhor resultado.
| Vara | Preço | Épico | Lendário | Especial |
|---|---|---|---|---|
| Comum | grátis | 5,5% | 1,4% | 0,1% |
| Rara | $ 150 | 10% | 2,8% | 0,2% |
| Épica | $ 600 | 16% | 5,5% | 0,5% |
| Lendária | $ 2000 | 23% | 10% | 1% |
**Lugares** (tecla M):
| Lugar | Como é | Para entrar |
|---|---|---|
| Lago Urbano | peixes fáceis, morde rápido, vale pouco | livre |
| Rio de Corredeira | o marcador é mais rápido: precisa de reflexo | livre |
| Mar Aberto | peixes gigantes, demora para morder, vale muito | Vara Rara ou melhor |
| Lixão (secreto) | em vez de peixe, lixo para reciclar (lata, bota, pneu, baú) | pescar 30 peixes |
**Energético** ($20, tecla E): por 30 segundos, a pesca fica 50% mais rápida (a espera até o peixe morder cai para 2/3).
**Multiplayer:** sempre no Lago Urbano, os dois com a Vara Comum e sem energético. Ganha quem pescar mais peixes em 1 minuto; no empate, ganha quem somar mais dinheiro em peixes.
**Progresso:** dinheiro, varas, lugar, energéticos e armazém ficam salvos em `save.json` (fora do Git).
## Estrutura do código
| Arquivo | Parte do jogo |
|---|---|
| `main.py` | liga o pygame e troca de tela (máquina de estados) |
| `config.py` | constantes: janela, cores, lugares, peixes, varas, chances, tempos e estados |
| `assets.py` | carrega fontes, imagens e sons uma vez só |
| `desenhos.py` | pixel art (velho, peixe, lixos, árvore) e cenário de cada lugar |
| `pesca.py` | regras: sortear raridade e peixe, avaliar o timing |
| `pescador.py` | classe `Pescador` (velho, vara, boia, barra e estados da pesca) |
| `dados.py` | salvar e carregar o progresso em `save.json` |
| `tela_menu.py` | menu inicial |
| `tela_single.py` | pesca sozinho (dinheiro, vara, lugar, energético) |
| `tela_mapa.py` | escolher o lugar de pesca |
| `tela_armazem.py` | grade com todos os peixes e venda |
| `tela_loja.py` | varas e energético |
| `tela_multi.py` | partida de 2 jogadores e resultado |
| `tela_config.py` | som e apagar progresso |
| `assets/sons/` | efeitos sonoros |
| `docs/` | explicação dos códigos |

## Regras que seguimos ao escrever o código

1. **Um arquivo para cada parte do jogo.** É a divisão do handout de PyGame da disciplina (`config.py`, `assets.py`, `sprites.py` e uma tela de jogo).
2. **Todos os números do jogo no `config.py`.** Preços, chances, tempos, cores e lugares ficam num só lugar.
3. **Regras separadas do desenho.** `pesca.py` só sorteia e julga o timing; quem desenha são as telas e o `Pescador`.
4. **A classe `Pescador` não toca som nem salva.** Ela só devolve o que aconteceu (`'lancou'`, `'pegou'`, `'errou'`), e a tela decide o resto. Por isso a mesma classe serve para o singleplayer e para os dois jogadores do multiplayer.
5. **Cada tela tem seu próprio loop** e devolve qual é a próxima tela, como no `jogo_v22.py` do handout.
6. **Desenhos feitos por nós, em pixel art com listas de strings.** 
9. **Tempo em milissegundos com `pygame.time.get_ticks()`**, como na explosão do handout: espera, barra, castigo, energético e o minuto do multiplayer não dependem do FPS.
10. **Comentários curtos.** Toda função tem uma docstring de uma linha dizendo o que faz; as explicações longas ficam em `docs/explicacao_dos_codigos.html`.
11. **Salvar a cada mudança.** O progresso é gravado a cada peixe, venda ou compra, então nada se perde se o jogo fechar.

## Referências

| O quê | Onde | Fonte |
|---|---|---|
| Estrutura do jogo (loop, estados, assets, arquivos) | todo o projeto | handout de PyGame de Design de Software |
| Documentação do pygame-ce | uso geral | https://pyga.me/docs/ |

## Uso de IA generativa

| Arquivo / trecho | Ferramenta | Quanto foi gerado | Como foi usado |
|---|---|---|---|
| Todos os arquivos `.py` (menu, pesca, lugares, energético, armazém, loja, mapa, multiplayer, configurações) | Claude Code (Anthropic) | 100% | escrito a partir da descrição do grupo; revisado e testado pelo grupo |
| `assets/sons/*.wav` | script feito com Claude Code | 100% | efeitos sonoros simples, sem direitos de terceiros |
| `docs/explicacao_dos_codigos.html` | Claude Code | 100% | explicação de cada bloco do código e perguntas para estudar |

**Parágrafo de uso:** usamos o Claude Code para escrever o jogo a partir das ideias do grupo (telas, pesca com timing, raridades, lugares, energético, armazém, loja e multiplayer), pedindo que usasse os conceitos dos handouts da disciplina e explicasse o que fugisse deles. Também geramos com ele a página que explica cada bloco do código, que usamos para estudar. Todos os integrantes revisaram o código.

### Anexo — interações com a IAg

- *(link ou arquivo com o histórico exportado das conversas de 06/11 e 07/11/2026)*
