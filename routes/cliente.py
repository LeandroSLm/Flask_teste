from flask import Blueprint, render_template, request, redirect, url_for
import json
import os

# Criação do Blueprint
cliente_route = Blueprint("cliente", __name__)

# Caminho do arquivo JSON onde os dados serão salvos
CLIENTES_FILE = 'clientes.json'

# Função para carregar os clientes do arquivo JSON
def carregar_clientes():
    if os.path.exists(CLIENTES_FILE):
        with open(CLIENTES_FILE, 'r') as f:
            return json.load(f)
    return []

# Função para salvar os clientes no arquivo JSON
def salvar_clientes(clientes):
    with open(CLIENTES_FILE, 'w') as f:
        json.dump(clientes, f)

# Carregar os clientes ao iniciar
CLIENTES = carregar_clientes()

@cliente_route.route("/")
def lista_clientes():
    # Renderiza a lista de clientes no template
    return render_template("lista_clientes.html", clientes=CLIENTES)


@cliente_route.route("/<string:cliente_cpf>")
def exibir_detalhes_clientes(cliente_cpf):
    print("CLIENTES:", CLIENTES) 
    for objeto in CLIENTES:
        if objeto["cpf"] == cliente_cpf:
            return f"ID: {objeto['id']}, Nome: {objeto['nome']}, CPF: {objeto['cpf']}, Data de Nascimento: {objeto['data_de_nascimento']}"
    return "Cliente não encontrado", 404
 
@cliente_route.route("/", methods=["POST"])
def inserir_clientes():
    data = request.form
    novo_usuario = {
        "id": len(CLIENTES) + 1, 
        "nome": data["nome"],
        "cpf": data["cpf"],
        "data_de_nascimento": data["data_de_nascimento"]  
    }
    CLIENTES.append(novo_usuario)
    salvar_clientes(CLIENTES)  
    print(novo_usuario)
    return redirect(url_for('cliente.lista_clientes'))  

@cliente_route.route("/new")
def form_cliente():
    return render_template("form_clientes.html")
