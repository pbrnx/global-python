import os
import json
import dados_usuarios

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_dados_alimentos(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return {}

def calcular_calorias_refeicao(alimentos, calorias_ja_consumidas):
    total_calorias = 0
    while True:
        alimento = input("Digite o nome do alimento (ou 'sair' para finalizar): ").lower()
        if alimento == 'sair':
            break
        if alimento in alimentos:
            gramas = float(input(f"Quantas gramas de {alimento} você comeu? "))
            calorias_por_100g = alimentos[alimento]['calorias']
            calorias = (gramas / 100) * calorias_por_100g
            total_calorias += calorias
        else:
            print("Alimento não encontrado.")
    return total_calorias + calorias_ja_consumidas

def input_sexo():
    while True:
        sexo = input("Informe o sexo (masculino/feminino): ").lower()
        if sexo in ["masculino", "feminino"]:
            return sexo
        else:
            print("Por favor, insira 'masculino' ou 'feminino'.")

def calcular_tmb(sexo, idade, peso, altura):
    try:
        idade = int(idade)
        peso = float(peso)
        altura = float(altura)
        if sexo.lower() == 'feminino':
            tmb = int(655 + (9.6 * peso) + (1.8 * altura) - (4.7 * idade))
        else:
            tmb = int(66 + (13.7 * peso) + (5 * altura) - (6.8 * idade))
        return tmb
    except ValueError:
        print("Por favor, insira valores numéricos válidos para idade, peso e altura.")
        return None

def calcular_get(tmb, dias_exercicio):
    if dias_exercicio <= 1:
        fator = 1.2
    elif 2 <= dias_exercicio <= 3:
        fator = 1.375
    elif 4 <= dias_exercicio <= 5:
        fator = 1.55
    elif 6 <= dias_exercicio <= 7:
        fator = 1.725
    return int(tmb * fator)

def registrar_objetivo(usuario_atual, nome_usuario):
    print("Qual é o seu objetivo de peso?")
    print("1. Manter")
    print("2. Perder")
    print("3. Ganhar")
    
    opcoes_objetivo = {1: 'manter', 2: 'perder', 3: 'ganhar'}
    escolha_valida = False

    while not escolha_valida:
        try:
            escolha = int(input("Escolha uma opção (1-3): "))
            if escolha in opcoes_objetivo:
                objetivo = opcoes_objetivo[escolha]
                escolha_valida = True
            else:
                print("Por favor, escolha uma opção válida.")
        except ValueError:
            print("Por favor, insira um número válido.")

    usuario_atual['objetivo'] = objetivo
    dados_usuarios.atualizar_dados_usuario(nome_usuario, usuario_atual['get'], usuario_atual['calorias_ingeridas'], usuario_atual.get('peso', 0), objetivo)
    print(f"Objetivo atualizado para '{objetivo}'.")


def mostrar_cardapio(alimentos):
    print("\nCardápio de Alimentos com Calorias por 100g:\n")
    for alimento, dados in alimentos.items():
        calorias = dados.get('calorias', 'Não disponível')
        print(f"{alimento.capitalize()}: {calorias} cal")

    # Opção para adicionar um novo alimento
    if input("\nAlgum alimento não está na lista? Deseja adicionar agora? (sim/não): ").lower() == 'sim':
        adicionar_alimento(alimentos)

def adicionar_alimento(alimentos):
    def solicitar_entrada(mensagem):
        entrada = input(mensagem)
        if entrada.lower() == 'cancelar':
            print("Operação cancelada.")
            return None
        return entrada

    nome_alimento = solicitar_entrada("Digite o nome do novo alimento (ou 'cancelar' para interromper): ").lower()
    if nome_alimento is None:
        return

    try:
        calorias = float(solicitar_entrada("Calorias por 100g (ou 'cancelar' para interromper): "))
        proteinas = float(solicitar_entrada("Proteínas por 100g (ou 'cancelar' para interromper): "))
        carboidratos = float(solicitar_entrada("Carboidratos por 100g (ou 'cancelar' para interromper): "))
        fibras = float(solicitar_entrada("Fibras por 100g (ou 'cancelar' para interromper): "))
        gorduras = float(solicitar_entrada("Gorduras por 100g (ou 'cancelar' para interromper): "))
    except ValueError:
        print("Entrada inválida. Operação cancelada.")
        return
    except TypeError:
        # Cancelamento durante a conversão para float
        return

    alimentos[nome_alimento] = {
        "calorias": calorias,
        "proteinas": proteinas,
        "carboidratos": carboidratos,
        "fibras": fibras,
        "gorduras": gorduras
    }

    # Salvar as alterações no arquivo JSON
    with open('./alimentos_brasileiros.json', 'w') as arquivo:
        json.dump(alimentos, arquivo, indent=4)

    print(f"Alimento '{nome_alimento}' adicionado com sucesso.")


def mostrar_calorias_restantes(usuario):
    if usuario:
        objetivo = usuario.get('objetivo', 'manter')
        calorias_ja_consumidas = usuario['calorias_ingeridas']
        calorias_recomendadas = usuario['get'] - 200 if objetivo == 'perder' else (usuario['get'] + 400 if objetivo == 'ganhar' else usuario['get'])
        calorias_restantes = calorias_recomendadas - calorias_ja_consumidas
        print(f"\nGET: {usuario['get']} calorias")
        print(f"Você já consumiu {calorias_ja_consumidas} calorias hoje.")
        print(f"Calorias recomendadas para hoje ({objetivo}): {calorias_recomendadas} calorias")
        if calorias_restantes > 0:
            print(f"Calorias restantes para hoje: {calorias_restantes} calorias\n")
        else: 
            print("Calorias restantes para hoje: 0")
    else:
        print("Usuário não logado ou dados não disponíveis.")

def limpar_calorias_consumidas(usuario_atual, nome_usuario):
    if usuario_atual:
        usuario_atual['calorias_ingeridas'] = 0
        dados_usuarios.atualizar_dados_usuario(nome_usuario, usuario_atual['get'], 0, usuario_atual.get('peso', 0), usuario_atual.get('objetivo', 'manter'))
        print("As calorias consumidas foram zeradas para o dia.")
    else:
        print("Usuário não logado ou dados não disponíveis.")

def mostrar_menu(usuario_logado=False):
    print('-' * 35)
    print("Menu Principal do hAppVida Fitness")
    print('-' * 35)
    if usuario_logado:
        print("1. Calcular Gasto Energético Total")
        print("2. Registrar Objetivo")
        print("3. Inserir Calorias da Refeição")
        print("4. Mostrar Calorias Restantes")
        print("5. Cardápio")
        print("6. Limpar Calorias Consumidas")
        print("7. Sair")
    else:
        print("1. Login")
        print("2. Criar Conta")
