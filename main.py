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
    else:
        fator = 1.9
    return int(tmb * fator)

def registrar_objetivo(usuario_atual, nome_usuario):
    objetivo = input("Qual é o seu objetivo? (manter, perder, ganhar): ").lower()
    usuario_atual['objetivo'] = objetivo
    dados_usuarios.atualizar_dados_usuario(nome_usuario, usuario_atual['get'], usuario_atual['calorias_ingeridas'], usuario_atual.get('peso', 0), objetivo)
    print(f"Objetivo atualizado para '{objetivo}'.")

def mostrar_cardapio(alimentos):
    print("\nCardápio de Alimentos com Informações Nutricionais:\n")
    for alimento, dados in alimentos.items():
        print(f"{alimento.capitalize()}:")
        for chave, valor in dados.items():
            print(f"  {chave.capitalize()}: {valor}")
        print()

def mostrar_calorias_restantes(usuario):
    if usuario:
        objetivo = usuario.get('objetivo', 'manter')
        calorias_ja_consumidas = usuario['calorias_ingeridas']
        calorias_recomendadas = usuario['get'] - 200 if objetivo == 'perder' else (usuario['get'] + 400 if objetivo == 'ganhar' else usuario['get'])
        calorias_restantes = calorias_recomendadas - calorias_ja_consumidas
        print(f"\nGET: {usuario['get']} calorias")
        print(f"Você já consumiu {calorias_ja_consumidas} calorias hoje.")
        print(f"Calorias recomendadas para hoje ({objetivo}): {calorias_recomendadas} calorias")
        print(f"Calorias restantes para hoje: {calorias_restantes} calorias\n")
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
    print("\nMenu Principal do hAppVida Fitness")
    if usuario_logado:
        print("1. Calcular Taxa Metabólica Basal (TMB)")
        print("2. Registrar Objetivo")
        print("3. Inserir Calorias da Refeição")
        print("4. Mostrar Calorias Restantes")
        print("5. Cardápio")
        print("6. Limpar Calorias Consumidas")
        print("7. Sair")
    else:
        print("1. Login")
        print("2. Criar Conta")
        print("3. Sair")

def main():
    limpar_tela()
    dados_alimentos = carregar_dados_alimentos('./alimentos_brasileiros.json')
    usuario_atual = None
    nome_usuario = None

    while True:
        if usuario_atual:
            mostrar_menu(usuario_logado=True)
        else:
            mostrar_menu(usuario_logado=False)

        escolha_menu = input("Escolha uma opção: ")

        if escolha_menu == '1':
            if usuario_atual:
                limpar_tela()
                sexo = input_sexo()
                idade = input("Informe a idade: ")
                peso = input("Informe o peso (em kg): ")
                altura = input("Informe a altura (em cm): ")
                tmb_usuario = calcular_tmb(sexo, idade, peso, altura)
                dias_exercicio = int(input("Quantos dias por semana você faz exercício físico? "))
                get_usuario = calcular_get(tmb_usuario, dias_exercicio)
                dados_usuarios.atualizar_dados_usuario(nome_usuario, get_usuario, usuario_atual['calorias_ingeridas'], peso, usuario_atual['objetivo'])
                print(f"Seu Gasto Energético Total estimado é: {get_usuario} calorias/dia")
            else:
                limpar_tela()
                nome_usuario = input("Digite seu nome de usuário: ")
                senha = input("Digite sua senha: ")
                if dados_usuarios.validar_login(nome_usuario, senha):
                    usuario_atual = dados_usuarios.obter_usuario(nome_usuario)
                    print(f"Bem-vindo de volta, {nome_usuario}!")
                else:
                    print("Nome de usuário ou senha incorretos.")

        elif escolha_menu == '2':
            if usuario_atual:
                limpar_tela()
                registrar_objetivo(usuario_atual, nome_usuario)
            else:
                limpar_tela()
                print("O hAppVida Fitness é uma solução inovadora e interativa para quem busca um estilo de vida mais saudável e consciente.\nEste aplicativo foi cuidadosamente projetado para atender às necessidades de indivíduos que desejam monitorar \nsua dieta de maneira eficiente e personalizada.\nLembre-se, é sempre melhor prevenir do que remediar, e uma boa alimentação é a melhor solução para isso! \n\nAgora, crie sua conta e faça parte do nosso projeto:\n ")
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
                limpar_tela()
                total_calorias = calcular_calorias_refeicao(dados_alimentos, usuario_atual['calorias_ingeridas'])
                print(f"Total de calorias da refeição: {total_calorias - usuario_atual['calorias_ingeridas']} calorias")
                usuario_atual['calorias_ingeridas'] = total_calorias
                dados_usuarios.atualizar_dados_usuario(nome_usuario, usuario_atual['get'], total_calorias, usuario_atual.get('peso', 0), usuario_atual['objetivo'])

        elif escolha_menu == '4':
            if usuario_atual:
                limpar_tela()
                mostrar_calorias_restantes(usuario_atual)

        elif escolha_menu == '5':
            if usuario_atual:
                limpar_tela()
                mostrar_cardapio(dados_alimentos)

        elif escolha_menu == '6':
            if usuario_atual:
                limpar_tela()
                limpar_calorias_consumidas(usuario_atual, nome_usuario)

        elif escolha_menu == '7':
            print("Obrigado por usar o hAppVida Fitness!")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()