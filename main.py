import json

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

def calcular_tmb(sexo, idade, peso, altura):
    try:
        idade = int(idade)
        peso = float(peso)
        altura = float(altura)
        if sexo.lower() == 'feminino':
            tmb = 655 + (9.6 * peso) + (1.8 * altura) - (4.7 * idade)
        else:
            tmb = 66 + (13.7 * peso) + (5 * altura) - (6.8 * idade)
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
    return tmb * fator


def mostrar_cardapio(alimentos):
    print("\nCardápio de Alimentos com Informações Nutricionais:\n")
    for alimento, dados in alimentos.items():
        print(f"{alimento.capitalize()}:")
        for chave, valor in dados.items():
            print(f"  {chave.capitalize()}: {valor}")
        print()


def mostrar_menu():
    print("\nMenu Principal do hAppVida Fitness")
    print("1. Calcular Taxa Metabólica Basal (TMB)")
    print("2. Calcular Calorias da Refeição")
    print("3. Cardápio")
    print("4. Sair")

def main():
    dados_alimentos = carregar_dados_alimentos('./alimentos_brasileiros.json')
    tmb_usuario = None
    get_usuario = None

    while True:
        mostrar_menu()
        escolha_menu = input("Escolha uma opção: ")

        if escolha_menu == '1':
            sexo = input("Informe o sexo (masculino/feminino): ")
            idade = input("Informe a idade: ")
            peso = input("Informe o peso (em kg): ")
            altura = input("Informe a altura (em cm): ")
            tmb_usuario = calcular_tmb(sexo, idade, peso, altura)
            if tmb_usuario:
                print(f"Sua Taxa Metabólica Basal é: {tmb_usuario:.2f} calorias/dia")
                dias_exercicio = int(input("Quantos dias por semana você faz exercício físico? "))
                get_usuario = calcular_get(tmb_usuario, dias_exercicio)
                print(f"Seu Gasto Energético Total estimado é: {get_usuario:.2f} calorias/dia")

        elif escolha_menu == '2':
            if dados_alimentos:
                calorias_refeicao = calcular_calorias_refeicao(dados_alimentos)
                print(f"Total de calorias da refeição: {calorias_refeicao:.2f} calorias")
                if get_usuario:
                    calorias_restantes = get_usuario - calorias_refeicao
                    print(f"Você ainda pode consumir {calorias_restantes:.2f} calorias hoje se deseja manter seu peso")
            else:
                print("Dados dos alimentos não disponíveis.")

        elif escolha_menu == '3':
            mostrar_cardapio(dados_alimentos)

        elif escolha_menu == '4':
            print("Obrigado por usar o hAppVida Fitness!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()

