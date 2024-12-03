import random
import os

def criar_arquivo_com_palavras():
    try:
        palavras_adicionais = [
            "tijolo", "quadro", "parede", "tomada", "verde",
            "parafuso", "foto", "branco", "computador", "estofado"
        ]
        if not os.path.exists("lista_palavras.txt") or os.stat("lista_palavras.txt").st_size == 0:
            with open("lista_palavras.txt", "w") as lista_palavras:
                for palavra in palavras_adicionais:
                    lista_palavras.write(palavra + "\n")
        else:
            with open("lista_palavras.txt", "r") as lista_palavras:
                palavras_existentes = lista_palavras.read().splitlines()
            with open("lista_palavras.txt", "a") as lista_palavras:
                for palavra in palavras_adicionais:
                    if palavra not in palavras_existentes:
                        lista_palavras.write(palavra + "\n")
    except Exception as e:
        print(f"Erro ao criar ou adicionar palavras ao arquivo: {e}")

def ranking():
    jogadores = {}
    try:
        with open("historico_tentativas.txt", "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(", ")
                if len(partes) == 3:
                    try:
                        nome = partes[0].split(": ")[1]
                        tentativas = int(partes[1].split(": ")[1])
                        erros = int(partes[2].split(": ")[1])
                        if nome in jogadores:
                            jogadores[nome]['tentativas'] += tentativas
                            jogadores[nome]['erros'] += erros
                        else:
                            jogadores[nome] = {'tentativas': tentativas, 'erros': erros}
                    except ValueError:
                        print(f"Erro ao processar a linha: {linha}")
                else:
                    print(f"Formato inválido na linha: {linha}")
        ranking = []
        for nome, stats in jogadores.items():
            acertos = stats['tentativas'] - stats['erros']
            pontuacao = (acertos / stats['tentativas']) * 100 if stats['tentativas'] > 0 else 0
            ranking.append((nome, pontuacao))
        ranking.sort(key=lambda x: x[1], reverse=True)
        print("\nRanking dos Jogadores:")
        for i, (nome, pontuacao) in enumerate(ranking, start=1):
            print(f"{i}. {nome} - {pontuacao:.2f}% de acertos")
    except FileNotFoundError:
        print("Nenhum histórico de tentativas encontrado.")

def jogar():
    criar_arquivo_com_palavras()
    with open("lista_palavras.txt", "r") as lista_palavras:
        palavras = [palavra.strip() for palavra in lista_palavras.readlines()]
    palavra_escolhida = random.choice(palavras).lower()
    lista_base = list(palavra_escolhida)
    lista_erros = []
    lista_jogador = []
    lista_display = ["_"] * len(lista_base)
    Nome_jogador = input("Digite seu nome: ")
    while True:
        erros = len(lista_erros)
        if erros >= 5:
            print("PERDEU! A palavra era:\n", palavra_escolhida)
            with open("historico_tentativas.txt", "a") as historico:
                historico.write(f"Nome: {Nome_jogador}, Tentativas: {len(lista_jogador)}, Erros: {erros}\n")
            break
        jogada_atual = input("Sua jogada: ")
        if len(jogada_atual) != 1 or not jogada_atual.isalpha():
            print("Por favor, insira apenas uma letra válida!")
            continue
        jogada_atual = jogada_atual.lower()
        if jogada_atual in lista_jogador:
            print("Você já tentou essa letra. Escolha outra!")
            continue
        lista_jogador.append(jogada_atual)
        if jogada_atual in lista_base:
            print("Acertou!")
            for i in range(len(lista_base)):
                if lista_base[i] == jogada_atual:
                    lista_display[i] = jogada_atual
        else:
            print("Errou!")
            lista_erros.append(jogada_atual)
        if "_" not in lista_display:
            print("Parabéns, você ganhou! A palavra era:", palavra_escolhida)
            with open("historico_tentativas.txt", "a") as historico:
                historico.write(f"Nome: {Nome_jogador}, Tentativas: {len(lista_jogador)}, Erros: {erros}\n")
            break
        print("Progresso:", " ".join(lista_display))

def adicionar():
    try:
        with open("lista_palavras.txt", "a+") as lista_palavras:
            lista_palavras.seek(0)
            palavras_existentes = lista_palavras.read().splitlines()
            while True:
                nova_palavra = input("Digite uma palavra para adicionar à lista \n(ou 'sair' para terminar):\n ")
                nova_palavra = nova_palavra.lower().strip()
                if nova_palavra == "sair":
                    print("Saindo...")
                    break
                if nova_palavra == "":
                    print("Entrada inválida. Por favor, digite uma palavra válida.")
                    continue
                if any(char.isdigit() for char in nova_palavra):
                    print("Entrada inválida. A palavra não pode conter números.")
                    continue
                if nova_palavra in palavras_existentes:
                    print(f"A palavra '{nova_palavra}' já existe e não será adicionada.")
                    continue
                lista_palavras.write(nova_palavra + "\n")
                lista_palavras.flush()
                palavras_existentes.append(nova_palavra)
                print(f"A palavra '{nova_palavra}' foi adicionada com sucesso!")
    except Exception as e:
        print(f"Erro ao abrir ou escrever no arquivo: {e}")

while True:
    print("Bem vindo ao melhor jogo da forca!")
    print("Escolha uma opção: \n1. Jogar \n2. Ver ranking \n3. Adicionar palavra \n4. Sair")
    try:
        opcao = int(input("Digite a opção desejada: "))
        if 1 <= opcao <= 4:
            if opcao == 1:
                jogar()
            elif opcao == 2:
                ranking()
            elif opcao == 3:
                adicionar()
            elif opcao == 4:
                print("Até a próxima!")
                break
        else:
            print("Opção inválida!")
    except ValueError:
        print("Entrada inválida! Por favor, insira um número inteiro.")
