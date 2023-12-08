import pandas as pd
import numpy as np

class TreeNode:
    def __init__(self, atributo=None, rotulo=None, count=0):
        self.atributo = atributo  # Atributo associado ao nó
        self.rotulo = rotulo  # Rótulo da classe (só é usado para folhas)
        self.count = count  # Número de elementos na folha
        self.ramos = {}  # Dicionário de ramos (valor do atributo -> subárvore)

#Calcula a entropia
def entropia(data, classe):
    class_counts = data[classe].value_counts()
    total_exemplos = len(data)
    valor_entropia = 0

    for count in class_counts:
        probabilidade = count / total_exemplos
        valor_entropia -= probabilidade * np.log2(probabilidade)

    return valor_entropia

# Calcula o ganho de informação para um atributo específico
def ganho(data, atributo, classe):
    valores_atributo = data[atributo].unique()
    total_exemplos = len(data)
    gain = entropia(data, classe)

    for valor in valores_atributo:
        subset = data[data[atributo] == valor]
        subset_entropia = entropia(subset, classe)
        subset_size = len(subset)
        gain -= (subset_size / total_exemplos) * subset_entropia

    return gain

# Calcula o ganho de informação para cada atributo e retorna o melhor
def seleciona_melhor_atributo(data, atributos, classe):
    melhor_atributo = None
    melhor_ganho = -np.inf

    for atributo in atributos:
        gain = ganho(data, atributo, classe)
        if gain > melhor_ganho:
            melhor_atributo = atributo
            melhor_ganho = gain

    return melhor_atributo

#Constrói a árvore de decisão
def constroi(data, atributos, classe):
    rotulos_classe = data[classe].unique()

    # Todos os exemplos têm a mesma classe
    if len(rotulos_classe) == 1:
        return TreeNode(rotulo=rotulos_classe[0], count=len(data))

    # Não há mais atributos para dividir
    if len(atributos) == 0:
        classe_mais_freq = data[classe].value_counts().idxmax()
        return TreeNode(rotulo=classe_mais_freq, count=len(data))

    # Seleciona o melhor atributo para dividir o conjunto de dados
    melhor_atributo = seleciona_melhor_atributo(data, atributos, classe)
    raiz = TreeNode(atributo=melhor_atributo)

    # Cria sub-árvore para cada valor do atributo selecionado
    valores_atributo = data[melhor_atributo].unique()
    for valor in valores_atributo:
        subset = data[data[melhor_atributo] == valor]
        if len(subset) == 0:
            classe_mais_freq = data[classe].value_counts().idxmax()
            raiz.ramos[valor] = TreeNode(rotulo=classe_mais_freq, count=0)
        else:
            atributos_restantes = []
            for atributo in atributos:
                if atributo != melhor_atributo:
                    atributos_restantes.append(atributo)
            raiz.ramos[valor] = constroi(subset, atributos_restantes, classe)

    return raiz

#Imprime a árvore
def print_tree(node, indent=''):
    if node.rotulo is not None:
        print(indent + 'Classe:', node.rotulo, '(Count: %d)' %node.count)
    else:
        print(indent + 'Atributo:', node.atributo)
        for valor, sub_arvore in node.ramos.items():
            print(indent + '|')
            print(indent + '|----Valor:', valor)
            print_tree(sub_arvore, indent + '|    ')

#Classifica um exemplo
def classify(exemplo, node):
    # Se o nó atual for folha, imprime a classe da folha
    if node.rotulo is not None:
        print('Classe:', node.rotulo)
    else:
        valor_atributo = exemplo[node.atributo]
        for valor in node.ramos:
            #Se o valor do atributo já existir na árvore, continua recursivamente
            if valor_atributo == str(valor):
                proximo_node = node.ramos[valor]
                classify(exemplo, proximo_node)
                return
        # Valor do atributo não existe na árvore, retorna o mais frequente
        classe_mais_freq = maior_classe(node)
        print('O valor do atributo %s não foi encontrado na árvore. Classe prevista: %s' %(node.atributo, classe_mais_freq))

#Retorna a classe mais frequente
def maior_classe(node):
    counts = {}
    for sub_arvore in node.ramos.values():
        if sub_arvore.count is not None:
            counts[sub_arvore.rotulo] = counts.get(sub_arvore.rotulo, 0) + sub_arvore.count

    if counts:
        classe_mais_freq = max(counts, key=counts.get)
    else:
        classe_mais_freq = None

    return classe_mais_freq

def main():
    data = None
    print("Indique o dataset no formato <nome>.csv:")
    while True:
        file = input()
        try:
            data = pd.read_csv(file)
            break
        # Mostra uma mensagem de erro se o ficheiro não for encontrado
        except FileNotFoundError:
            print("O ficheiro especificado não foi encontrado. Por favor insira o ficheiro csv correto.")

    #Constroi o dataset, elimina o identificador (coluna 0) e separa os atributos da classe a ser prevista
    df = pd.DataFrame(data)
    coluna_classe = df.columns[-1]
    df = df.drop(df.columns[0], axis=1)
    atributos = df.drop(df.columns[-1], axis=1)

    #Constrói a árvore
    tree = constroi(df, atributos, coluna_classe)
    print()

    #Imprime a árvore
    print('Árvore de Decisão:\n')
    print_tree(tree)
    print()

    #Caso em que se pretende classificar um exemplo específico
    print('Deseja classificar um exemplo? (Responda Y/N)')
    res = input()
    while res != 'Y' and res != 'y' and res != 'N' and res != 'n':
        print('Por favor insira um valor válido (Y/N)')
        res = input()
    print()

    if res == 'Y' or res=='y':
        #Número de exemplos que se pretende classificar
        print('Quantos exemplos deseja classificar?')
        while True:
            num_input = input()

            try:
                num = int(num_input)
                break
            except ValueError:
                print('Valor inválido. Insira um valor válido.')
        print()

        #Lista com as colunas
        atributos = list(data)
        atributos.remove(atributos[-1])

        #Diz o formato de input a ser inserido
        print('Insira os exemplos, um de cada vez.')
        print('Use este formato:', end=' ')
        for i in range (len(atributos)-1):
            print('<%s>' %atributos[i], end=',')
        print('<%s>' %atributos[-1])
        print('O programa vai prever o valor para a classe [%s].\n' %coluna_classe)

        atributos.remove(atributos[0]) #Remove o identificador

        iter = 1 #numero do exemplo
        while num>0:
            print('Exemplo %d:' %iter)
            valor = input()
            valor = valor.split(',') #lista com os valores
            while len(valor) != len(atributos) +1:
                print('Número de colunas incorreto. Insira com o formato pedido.')
                valor = input()
                valor = valor.split(',')
            exemplo = dict() #dicionário {atributo: valor}
            i = 1 #não lê o identificador
            for atributo in atributos:
                exemplo[atributo] = valor[i]
                i += 1
            classify(exemplo, tree) #classifica o exemplo
            num-=1
            iter+=1

if __name__ == '__main__':
    main()
