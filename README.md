# App de entregas: árvores em ação

Trabalho AV2 de Teoria dos Grafos (CESUPA): árvores balanceadas aplicadas a um app de entregas de comida.

- **k-D** (`src/kd_tree.py`): restaurantes por coordenada e busca dos mais próximos
- **Rubro-negra** (`src/red_black_tree.py`): pedidos, ordenados por número
- **2-3-4** (`src/tree_234.py`): catálogo de produtos, em ordem alfabética

As três árvores foram feitas do zero, com nós ligados. Nenhuma biblioteca de árvore é usada: o Flask serve só a página e o matplotlib só desenha as figuras da k-D.

## Requisitos
- Python 3.10 ou mais recente
- Pacotes de `requirements.txt` (Flask e matplotlib)

## Executar
Abra um terminal na pasta do projeto (a que contém `app.py`) e rode:
```
pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:5000 no navegador. No Windows, se `python` não funcionar, use `py` no lugar.

O app começa com 22 restaurantes (k-D), 21 pedidos (rubro-negra) e 14 produtos (2-3-4). Os dados ficam só na memória e voltam ao estado inicial quando o servidor reinicia.

## O que dá para fazer no app
| Aba | Árvore | Inserção | Exclusão | Busca |
|---|---|---|---|---|
| Restaurantes | k-D | cadastrar restaurante (x, y) | excluir restaurante | N restaurantes mais próximos de um ponto (clique no mapa) |
| Pedidos | rubro-negra | novo pedido | excluir pedido | localizar pedido pelo número |
| Catálogo | 2-3-4 | novo produto | excluir produto | filtrar por nome (percurso em ordem) |

Cada aba mostra a estrutura atual da árvore, a altura e se as propriedades continuam válidas depois de cada operação.

## Testes
Na mesma pasta:
```
python tests/test_red_black.py
python tests/test_234.py
python tests/test_kd.py
```
- `test_red_black.py`: insere 25 chaves, exclui algumas e valida as propriedades da rubro-negra.
- `test_234.py`: inserções, exclusões e um teste de estresse com valores aleatórios, validando a 2-3-4 a cada passo.
- `test_kd.py`: eletropostos num mapa de 20 x 20 km; gera as figuras de `imagens_kd/` (construção pela mediana, inserção, vizinho mais próximo, busca por região e exclusão).

## Elementos repetidos
- **Rubro-negra:** chave repetida é rejeitada (`insert` retorna `False`). No app isso não acontece, porque o número do pedido é gerado em sequência.
- **2-3-4:** chave repetida é rejeitada. No app a chave é (nome em minúsculas, id do produto), então dois produtos com o mesmo nome são aceitos como produtos diferentes.
- **k-D:** ponto idêntico (mesmo x e mesmo y) é rejeitado. Pontos com o mesmo valor em um eixo vão para a direita (maior ou igual).

## Estrutura
```
app.py              servidor Flask e rotas da API
templates/index.html  página do app
src/                árvores (k-D, rubro-negra, 2-3-4)
tests/              scripts de teste
imagens_kd/         figuras geradas pelo teste da k-D
```
