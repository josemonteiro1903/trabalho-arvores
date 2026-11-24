import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from flask import Flask, jsonify, render_template, request

from kd_tree import KDTree
from red_black_tree import RedBlackTree
from tree_234 import Tree234, search as search234, validate as validate234

app = Flask(__name__)

# ==========================================
# ESTADO (em memória) E DADOS INICIAIS
# ==========================================
restaurantes = KDTree()   # ponto (x, y) -> nome do restaurante
pedidos = RedBlackTree()  # chave = número do pedido
catalogo = Tree234()      # chave = (nome em minúsculas, id do produto)
produtos = {}             # id -> dados do produto (a árvore guarda só a chave)
contador = {"pedido": 1000, "produto": 0}

STATUS = ["Recebido", "Em preparo", "A caminho", "Entregue"]


def novo_pedido(cliente, itens, restaurante, status="Recebido"):
    contador["pedido"] += 1
    num = contador["pedido"]
    pedidos.insert(num, {"cliente": cliente, "itens": itens,
                         "restaurante": restaurante, "status": status})
    return num


def novo_produto(nome, preco, categoria):
    contador["produto"] += 1
    pid = contador["produto"]
    produtos[pid] = {"id": pid, "nome": nome, "preco": preco, "categoria": categoria}
    catalogo.insert((nome.lower(), pid))
    return pid


# Dados iniciais: as árvores binárias (k-D e rubro-negra) começam com 21+ nós,
# como pede o enunciado do trabalho.
for nome, x, y in [("Pizzaria Bella", 10, 10), ("Sushi Kyoto", 4, 15), ("Burger Norte", 16, 5),
                   ("Cantina da Vó", 2, 7), ("Açaí do Porto", 7, 18), ("Churrasco Sul", 13, 14),
                   ("Vegana Verde", 18, 11), ("Padaria Central", 6, 3), ("Tapioca da Praça", 1, 12),
                   ("Pastelaria Feira", 9, 6), ("Peixaria Ver-o-Peso", 15, 19), ("Doceria Doce Lar", 19, 2),
                   ("Marmitaria Caseira", 3, 1), ("Lanchonete Esquina", 12, 3), ("Cafeteria Grão", 5, 10),
                   ("Temakeria Zen", 17, 16), ("Sorveteria Polar", 8, 13), ("Galeteria Brasa", 14, 8),
                   ("Pizzaria Forno a Lenha", 11, 17), ("Restaurante Mangal", 0, 4), ("Creperia Paris", 20, 20),
                   ("Espetinho do Zé", 6, 16)]:
    restaurantes.insert((float(x), float(y)), nome)

for n, p, c in [("Pizza Margherita", 42.0, "Pizza"), ("Hambúrguer Clássico", 28.5, "Lanche"),
                ("Combo Sushi 20 peças", 64.9, "Japonesa"), ("Açaí 500 ml", 18.0, "Sobremesa"),
                ("Suco de Laranja", 9.5, "Bebida"), ("Salada Caesar", 26.0, "Salada"),
                ("Refrigerante Lata", 6.0, "Bebida"), ("Água Mineral", 4.0, "Bebida"),
                ("Batata Frita", 15.0, "Porção"), ("Pudim", 12.0, "Sobremesa"),
                ("Tacacá", 25.0, "Regional"), ("Maniçoba", 32.0, "Regional"),
                ("Lasanha Bolonhesa", 38.0, "Massa"), ("Café Expresso", 7.0, "Bebida")]:
    novo_produto(n, p, c)

novo_pedido("Ana", ["Pizza Margherita", "Refrigerante Lata"], "Pizzaria Bella", "Em preparo")
novo_pedido("Bruno", ["Açaí 500 ml"], "Açaí do Porto", "A caminho")
novo_pedido("Carla", ["Combo Sushi 20 peças"], "Sushi Kyoto")
for cliente, itens, rest, st in [
        ("Diego", ["Hambúrguer Clássico", "Batata Frita"], "Burger Norte", "Entregue"),
        ("Elisa", ["Salada Caesar"], "Vegana Verde", "Recebido"),
        ("Fábio", ["Tacacá"], "Peixaria Ver-o-Peso", "Em preparo"),
        ("Gabi", ["Pudim", "Café Expresso"], "Doceria Doce Lar", "A caminho"),
        ("Hugo", ["Lasanha Bolonhesa"], "Cantina da Vó", "Entregue"),
        ("Iara", ["Maniçoba"], "Restaurante Mangal", "Recebido"),
        ("João", ["Pizza Margherita"], "Pizzaria Forno a Lenha", "Em preparo"),
        ("Karen", ["Açaí 500 ml", "Água Mineral"], "Açaí do Porto", "Entregue"),
        ("Leo", ["Combo Sushi 20 peças", "Refrigerante Lata"], "Temakeria Zen", "A caminho"),
        ("Marina", ["Suco de Laranja"], "Padaria Central", "Recebido"),
        ("Nina", ["Batata Frita"], "Lanchonete Esquina", "Entregue"),
        ("Otávio", ["Hambúrguer Clássico"], "Burger Norte", "Em preparo"),
        ("Paula", ["Café Expresso"], "Cafeteria Grão", "Entregue"),
        ("Rafael", ["Pizza Margherita", "Suco de Laranja"], "Pizzaria Bella", "A caminho"),
        ("Sofia", ["Salada Caesar", "Água Mineral"], "Vegana Verde", "Recebido"),
        ("Tiago", ["Tacacá", "Maniçoba"], "Restaurante Mangal", "Em preparo"),
        ("Úrsula", ["Pudim"], "Sorveteria Polar", "Entregue"),
        ("Vítor", ["Lasanha Bolonhesa", "Refrigerante Lata"], "Cantina da Vó", "Recebido")]:
    novo_pedido(cliente, itens, rest, st)


# ==========================================
# AUXILIARES
# ==========================================
def erro(msg, codigo=400):
    return jsonify(erro=msg), codigo


def num(valor, nome):
    try:
        v = float(valor)
    except (TypeError, ValueError):
        raise ValueError(f"'{nome}' precisa ser um número.")
    if not math.isfinite(v):                 # recusa nan e inf
        raise ValueError(f"'{nome}' precisa ser um número finito.")
    return v


def corpo():
    """Corpo JSON da requisição como dicionário ({} se vier vazio, nulo ou inválido)."""
    d = request.get_json(force=True, silent=True)
    return d if isinstance(d, dict) else {}


def texto(valor):
    return "" if valor is None else str(valor).strip()


def rest_json(node, dist=None):
    d = {"nome": node.data, "x": node.point[0], "y": node.point[1]}
    if dist is not None:
        d["dist"] = round(dist, 2)
    return d


def estrutura_kd():
    def f(n, d):
        if n is None:
            return None
        filhos = [c for c in (f(n.left, d + 1), f(n.right, d + 1)) if c]
        return {"t": f"{n.data} ({n.point[0]:g}, {n.point[1]:g}) · corte em {'x' if d % 2 == 0 else 'y'}",
                "c": filhos}
    return f(restaurantes.root, 0)


def estrutura_rb():
    def f(n):
        if n == pedidos.NIL:
            return None
        return {"t": f"#{n.key}", "cor": n.color, "c": [c for c in (f(n.left), f(n.right)) if c]}
    return f(pedidos.root)


def estrutura_234():
    def f(n):
        return {"t": " | ".join(produtos[k[1]]["nome"] for k in n.keys),
                "c": [] if n.leaf else [f(c) for c in n.children]}
    return f(catalogo.root) if catalogo.inorder() else None


# ==========================================
# RESTAURANTES (árvore k-D)
# ==========================================
@app.route("/")
def index():
    return render_template("index.html", status=STATUS)


@app.get("/api/restaurantes")
def listar_restaurantes():
    return jsonify(itens=[rest_json(n) for n in restaurantes.nodes()],
                   estrutura=estrutura_kd(), altura=restaurantes.height(),
                   valida=restaurantes.validate())


@app.post("/api/restaurantes")
def criar_restaurante():
    d = corpo()
    nome = texto(d.get("nome"))
    if not nome:
        return erro("Informe o nome do restaurante.")
    try:
        ponto = (num(d.get("x"), "x"), num(d.get("y"), "y"))
    except ValueError as e:
        return erro(str(e))
    if not restaurantes.insert(ponto, nome):
        return erro("Já existe um restaurante nessa coordenada.", 409)
    return jsonify(ok=True), 201


@app.delete("/api/restaurantes")
def excluir_restaurante():
    try:
        ponto = (num(request.args.get("x"), "x"), num(request.args.get("y"), "y"))
    except ValueError as e:
        return erro(str(e))
    if not restaurantes.delete(ponto):
        return erro("Restaurante não encontrado.", 404)
    return jsonify(ok=True)


@app.get("/api/restaurantes/proximos")
def proximos():
    try:
        alvo = (num(request.args.get("x"), "x"), num(request.args.get("y"), "y"))
    except ValueError as e:
        return erro(str(e))
    try:
        n = int(request.args.get("n", 3))
    except ValueError:
        return erro("'n' precisa ser um número inteiro.")
    if n < 1:
        return erro("'n' precisa ser pelo menos 1.")
    return jsonify(itens=[rest_json(no, d) for no, d in restaurantes.k_nearest(alvo, n)])


# ==========================================
# PEDIDOS (árvore rubro-negra)
# ==========================================
def pedido_json(no):
    return {"numero": no.key, "cor": no.color, **no.value}


@app.get("/api/pedidos")
def listar_pedidos():
    return jsonify(itens=[{"numero": i["key"], "cor": i["color"], **i["value"]} for i in pedidos.inorder()],
                   estrutura=estrutura_rb(), altura=pedidos.height(), valida=pedidos.validate())


@app.get("/api/pedidos/<int:numero>")
def buscar_pedido(numero):
    no = pedidos.search(numero)
    return jsonify(pedido_json(no)) if no else erro("Pedido não encontrado.", 404)


@app.post("/api/pedidos")
def criar_pedido():
    d = corpo()
    cliente = texto(d.get("cliente"))
    itens = d.get("itens")
    if not isinstance(itens, list):              # aceita lista ou texto separado por vírgula
        itens = texto(itens).split(",")
    itens = [texto(i) for i in itens if texto(i)]
    if not cliente or not itens:
        return erro("Informe o cliente e ao menos um item (separe por vírgula).")
    numero = novo_pedido(cliente, itens, texto(d.get("restaurante")))
    return jsonify(numero=numero), 201


@app.put("/api/pedidos/<int:numero>")
def atualizar_pedido(numero):
    no = pedidos.search(numero)
    status = corpo().get("status")
    if not no:
        return erro("Pedido não encontrado.", 404)
    if status not in STATUS:
        return erro("Status inválido.")
    no.value["status"] = status
    return jsonify(ok=True)


@app.delete("/api/pedidos/<int:numero>")
def excluir_pedido(numero):
    return jsonify(ok=True) if pedidos.delete(numero) else erro("Pedido não encontrado.", 404)


# ==========================================
# CATÁLOGO (árvore 2-3-4)
# ==========================================
@app.get("/api/catalogo")
def listar_catalogo():
    q = (request.args.get("q") or "").strip().lower()
    itens = [produtos[k[1]] for k in catalogo.inorder() if q in k[0]]  # já vem em ordem alfabética
    return jsonify(itens=itens, estrutura=estrutura_234(), altura=catalogo.height(),
                   valida=_valida_234())


def _valida_234():
    try:
        validate234(catalogo.root)
        return True
    except AssertionError:
        return False


@app.post("/api/catalogo")
def criar_produto():
    d = corpo()
    nome = texto(d.get("nome"))
    try:
        preco = num(d.get("preco"), "preco")
    except ValueError as e:
        return erro(str(e))
    if not nome or preco < 0:
        return erro("Informe um nome e um preço válido.")
    pid = novo_produto(nome, preco, texto(d.get("categoria")) or "Outros")
    return jsonify(id=pid), 201


@app.delete("/api/catalogo/<int:pid>")
def excluir_produto(pid):
    p = produtos.get(pid)
    if not p or not catalogo.delete((p["nome"].lower(), pid)):
        return erro("Produto não encontrado.", 404)
    del produtos[pid]
    return jsonify(ok=True)


# ==========================================
# ERROS DA API EM JSON (a página espera JSON, nunca HTML)
# ==========================================
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def erro_http(e):
    codigo = getattr(e, "code", 500)
    if request.path.startswith("/api/"):
        msg = {404: "Não encontrado.", 405: "Método não permitido."}.get(codigo, "Erro interno no servidor.")
        return erro(msg, codigo)
    return e


if __name__ == "__main__":
    app.run(debug=True)
