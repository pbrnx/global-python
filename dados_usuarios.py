import json

caminho_arquivo = 'usuarios.json'

def carregar_usuarios():
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

def salvar_usuarios(usuarios):
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(usuarios, arquivo, indent=4)

usuarios = carregar_usuarios()

def adicionar_usuario(nome_usuario, senha):
    usuarios[nome_usuario] = {
        "senha": senha,
        "get": 0,
        "calorias_ingeridas": 0
    }
    salvar_usuarios(usuarios)

def validar_login(nome_usuario, senha):
    usuario = usuarios.get(nome_usuario)
    if usuario and usuario['senha'] == senha:
        return True
    return False

def obter_usuario(nome_usuario):
    return usuarios.get(nome_usuario, None)

def atualizar_dados_usuario(nome_usuario, get, calorias_ingeridas):
    if nome_usuario in usuarios:
        usuarios[nome_usuario]['get'] = get
        usuarios[nome_usuario]['calorias_ingeridas'] = calorias_ingeridas
        salvar_usuarios(usuarios)
