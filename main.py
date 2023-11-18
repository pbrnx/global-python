import json
import dados_usuarios

def carregar_dados_alimentos(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return {}

def calcular_calorias_refeicao(alimentos):
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
    return total_calorias

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
            tmb = 655 + (9.6 * peso) + (1.8 * altura) - (4.7 * idade)
        else:
            tmb = 66 + (13.7 * peso) + (5 * altura) - (6.8 * idade)
        return int(tmb)
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
    else:
        fator = 1.9
    return int(tmb * fator)

def mostrar_cardapio(alimentos):
    print("\nCardápio de Alimentos com Informações Nutricionais:\n")
    for alimento, dados in alimentos.items():
        print(f"{alimento.capitalize()}:")
        for chave, valor in dados.items():
            print(f"  {chave.capitalize()}: {valor}")
        print()

def mostrar_calorias_restantes(usuario):
    if usuario:
        calorias_restantes = usuario['get'] - usuario['calorias_ingeridas']
        print(f"\nGET: {usuario['get']} calorias")
        print(f"Calorias restantes para hoje: {calorias_restantes} calorias\n")
    else:
        print("Usuário não logado ou dados não disponíveis.")

def mostrar_menu():
    print("\nMenu Principal do hAppVida Fitness")
    print("1. Login")
    print("2. Criar Conta")
    print("3. Calcular Taxa Metabólica Basal (TMB)")
    print("4. Calcular Calorias da Refeição")
    print("5. Cardápio")
    print("6. Verificar Calorias Restantes")
    print("7. Sair")

def main():
    dados_alimentos = carregar_dados_alimentos('./alimentos_brasileiros.json')
    usuario_atual = None

    while True:
        mostrar_menu()
        escolha_menu = input("Escolha uma opção: ")

        if escolha_menu == '1':
            nome_usuario = input("Digite seu nome de usuário: ")
            senha = input("Digite sua senha: ")
            if dados_usuarios.validar_login(nome_usuario, senha):
                usuario_atual = dados_usuarios.obter_usuario(nome_usuario)
                print(f"Bem-vindo de volta, {nome_usuario}!")
            else:
                print("Nome de usuário ou senha incorretos.")

        elif escolha_menu == '2':
            nome_usuario = input("Escolha um nome de usuário: ")
            senha = input("Escolha uma senha: ")
            if nome_usuario in dados_usuarios.usuarios:
                print("Nome de usuário já existe.")
            else:
                dados_usuarios.adicionar_usuario(nome_usuario, senha)
                print(f"Conta criada com sucesso. Bem-vindo(a), {nome_usuario}!")
                usuario_atual = dados_usuarios.obter_usuario(nome_usuario)

        elif escolha_menu == '3':
            if usuario_atual:
                sexo = input_sexo()
                idade = input("Informe a idade: ")
                peso = input("Informe o peso (em kg): ")
                altura = input("Informe a altura (em cm): ")
                tmb_usuario = calcular_tmb(sexo, idade, peso, altura)
                print(f"Sua Taxa Metabólica Basal é: {tmb_usuario:.2f} calorias/dia")
                dias_exercicio = int(input("Quantos dias por semana você faz exercício físico? "))
                get_usuario = calcular_get(tmb_usuario, dias_exercicio)
                print(f"Seu Gasto Energético Total estimado é: {get_usuario:.2f} calorias/dia")
                dados_usuarios.atualizar_dados_usuario(nome_usuario, get_usuario, usuario_atual['calorias_ingeridas'])
            else:
                print("Por favor, faça login ou crie uma conta primeiro.")

        elif escolha_menu == '4':
            if usuario_atual and dados_alimentos:
                calorias_refeicao = calcular_calorias_refeicao(dados_alimentos)
                print(f"Total de calorias da refeição: {calorias_refeicao:.2f} calorias")
                calorias_restantes = usuario_atual['get'] - calorias_refeicao
                print(f"Você ainda pode consumir {calorias_restantes:.2f} calorias hoje se deseja manter seu peso")
                dados_usuarios.atualizar_dados_usuario(nome_usuario, usuario_atual['get'], calorias_refeicao)
            else:
                print("Dados dos alimentos não disponíveis ou usuário não logado.")

        elif escolha_menu == '5':
            mostrar_cardapio(dados_alimentos)

        elif escolha_menu == '6':
            if usuario_atual:
                mostrar_calorias_restantes(usuario_atual)
            else:
                print("Por favor, faça login ou crie uma conta para acessar esta opção.")

        elif escolha_menu == '7':
            print("Obrigado por usar o hAppVida Fitness!")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
