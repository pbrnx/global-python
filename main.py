#INTEGRANTES:
#Pedro Augusto Barone - RM99781
#João Pedro de Albuquerque Oliveira - RM:551579

import dados_usuarios
from functions import *

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
                while True:  # Adicione um loop para verificar a entrada do usuário
                    dias_exercicio = int(input("Quantos dias por semana você faz exercício físico? "))
                    if 0 <= dias_exercicio <= 7:  # Certifique-se de que o valor está entre 0 e 7
                        break
                    else:
                        print("Número inválido. Insira um número de dias entre 0 e 7.")
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