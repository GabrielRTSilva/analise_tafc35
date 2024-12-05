import numpy as np
import pandas as pd


## ------ CLASSE JOGADOR ------ ##

# Essa classe contem os seguintes parametros:
  
  # Atributos:    retorna variaveis do tipo string, contento nome, lista de recepcoes, levantamentos e ataque
  # Objeto:       retorna um dicionario, contendo nome, recepcao, levantamento e ataques (os values das ultimas tres keys sao obejetos tipo list.)

#*** adicionar -> numero da dupla, perna boa, lado que joga, jogos disputados e qtd de vitorias

class Jogador:   # Recebe como argumento uma lista com o nome do jogador, suas recepcoes, seus levantamentos e seus ataques. 

  def __init__ (self, lista):  # Inicializa o Objeto
    self.nome = lista[0][0]
    self.numeroDupla = lista[0][1]
    self.pernaBoa = lista[0][2]
    self.vitorias = lista[0][5]
    self.ataques = list(lista[1])
    self.recepcoes = list(lista[2])
    self.levantamentos = list(lista[3])
  
  def Atributos(self):  # Mostra os Atributos do Objeto
    return 'Atributos do  ' + str(self.nome) + 'Recepção: ' + str(self.recepcoes) + 'Levantamento: ' + str(self.levantamentos) + 'Ataque: ' + str(self.ataques)
  
  def Objeto(self):  # Mostra o Objeto em Formato Dict
    objeto = {
      'Nome': self.nome,
      'Ataques':  self.ataques,
      'Recepções': self.recepcoes,
      'Levantamentos': self.levantamentos
    }
  
    return objeto
  
  def Recepcoes (self):
    return self.recepcoes
  
  def Levantamentos (self):
    return self.levantamentos

  def Ataques (self):
    return self.ataques
  

#FUNÇÕES GENÉRICAS

def limpaDados(lista):                                                                # Função para limpar os dados NaN do array unidimensional
  listaLimpa = []

  for item in lista:
    if item == '-':
      item = 0
      listaLimpa.append(item)
    else:
      listaLimpa.append(item)
  return listaLimpa

def SelecionaMetrica(lista: list, num: int):                                          # Função para selecionar a métrica, sendo ela acertos (0), bolas que passaram (1) e erros (2)

  listaLimpa = limpaDados(lista)

  listaDosIndexes = list(range(num, len(listaLimpa), 3 ))  
  
  metrica = []
  k = 0

  while k < (len(listaDosIndexes)):
    for index, item2 in enumerate(listaLimpa):
      if index == listaDosIndexes[k]:
        metrica.append(listaLimpa[index])
    
    k = k + 1

  return metrica

#FUNÇÕES PARA GERAR PARAMETROS DE ANALISE 

def Eficacia (lista: list):                                                           # Calcula a eficacia de um atributo da classe Jogador, podendo ser ataques, levantamentos e rececpcoes. Return: type(float, round(2)) 

  listaLimpa = limpaDados(lista)

  acertos = SelecionaMetrica(listaLimpa, 0)

  eficacia = round((sum(acertos)/ sum(listaLimpa)),2)
  
  return eficacia 

def PontosConvertidos(lista: list,lista2: list):                                      # Calcula a capacidade de aproveitamento de um jogador em converter levantamentos em pontos Return: type(float, round(2))

  ataquesRealizados = SelecionaMetrica(lista, 0)
  acertosLevantamento = SelecionaMetrica(lista2, 0)
  pontosConvertidos = round((sum(ataquesRealizados) / sum(acertosLevantamento)),2)

  return pontosConvertidos

def VariacaoDeJogadas(lista: list):                                                   # Funcao que ira retornar quantos ataques o jogador variou 

  listaLimpa = limpaDados(lista)     
  
  listaPontos = SelecionaMetrica(listaLimpa, 0)
  listaNaoPontos = SelecionaMetrica(listaLimpa, 1)

  arr = np.column_stack((listaPontos, listaNaoPontos))

  variacoes = 0
  linha = 0

  while linha < len(arr):                             # Esse loop percorre as linhas e os elementos das colunas para contar se houve variacao dos ataques
    for i in arr[linha]:
      if i != 0:
        variacoes += 1
        break
      else:
        continue
    linha += 1

  return variacoes

# FUNÇÕES PARA ESTRUTURAR OS DADOS NA CLASSE JOGADOR

def TornarJogador(idJogador: int):                                                    # Função que retorna todos os atributos do jogador estruturados na classe Jogador. Type Object
  
  cont = 3
  atributos = []


  df = pd.read_excel('tafc35-smalldata.xlsx', sheet_name = 1)
    
  lista = df.iloc[idJogador - 1]
  arr = np.array(lista)
  atributos.append(arr)

  
  while cont >= 3 and cont < 6:   
    df = pd.read_excel('tafc35-smalldata.xlsx', sheet_name = f'{cont}')
    
    listaB = df.iloc[idJogador]
    arrB = np.array(listaB)
    atributos.append(arrB)

    cont += 1
  
  atributosLimpos = []

  for item in map(limpaDados, atributos):
    del item[0]
    atributosLimpos.append(item)
  
  objetoJogador = Jogador(atributosLimpos)
  return objetoJogador
  
#TESTE DE ANALISE

listaJogadores = [TornarJogador(i) for i in range(1, 33)]

# PEGAR OS ATRIBUTOS DE DETERMINADO JOGADOR
  # Vasculhar o arquivo no range(1,6) -FEITO
  # Para cada Jogador - FEITO
    # Pegar todas as linhas que tenha o respectivo id dentro do range(1,33) -FEITO
    # Converter em np.arr - FEITO
# JUNTAR ESSES ATRIBUTOS EM UMA LISTA COM SEU NOME

#ARGUMENTO 1

      # JOGADOR MENOS PERIGOSO DE ACORDO COM A QUANTIDADE DE ATAQUES ( SE O JOGADOR ATACOU VARIAS VEZES SIGNIFICA QUE ELE RECEBEU MAIS SAQUES E CONSEQUENTEMENTE SERIA MENOR O INDICE DE PERICULOSIDADE)


## LOOP PARA DIVIDIR AS DUPLAS VENCEDORAS 

listaDictsEficaciaP = []
listaDictsEficaciaI = []

contador = 0

for jogador in listaJogadores:
  if jogador.vitorias == 1 and contador %2 == 0:
    listaDictsEficaciaP.append({'NOME': jogador.nome, 'ATAQUES': sum(SelecionaMetrica(jogador.ataques,0)) + sum(SelecionaMetrica(jogador.ataques,1)), 'AG': jogador.ataques ,'EFICACIA': Eficacia(jogador.ataques)})  
  elif jogador.vitorias == 1 and contador %2 != 0:
    listaDictsEficaciaI.append({'NOME': jogador.nome, 'ATAQUES': sum(SelecionaMetrica(jogador.ataques,0)) + sum(SelecionaMetrica(jogador.ataques,1)), 'AG': jogador.ataques , 'EFICACIA': Eficacia(jogador.ataques)})

  contador = contador + 1

listaDictsEZIP = list(zip(listaDictsEficaciaP, listaDictsEficaciaI))  # ESSA VARIAVEL CONTEM OS JOGADORES DAS DUPLAS UNIDOS E SEUS ATRIBUTOS

### DADOS PARA GRAFICO DE RELAÇÃO DE ATAQUES RECEBIDOS POR DUPLAS

ataquesJogador1 = []
ataquesJogador2 = []

for jogador1, jogador2 in listaDictsEZIP:
  ataquesJogador1.append({jogador1['NOME']: jogador1['ATAQUES']})
  ataquesJogador2.append({jogador2['NOME']: jogador2['ATAQUES']})

print(f'Lista dos ataques dos jogadores 1 das duplas {ataquesJogador1} \nLista dos ataques dos jogadores 2 das duplas {ataquesJogador2}')     
#CASO SEJA NECESSARIO/INTERESSANTE ZIPAR AS LISTAS ACIMAS PARA DIAGRAMAR O GRAFICO

# DADOS PARA GRAFICOS DOS JOGADORES MENOS PERIGOSOS E SUAS EFICACIAS

listaEficaciaMP = []

for jogador1, jogador2 in listaDictsEZIP:
  if jogador1['ATAQUES'] > jogador2['ATAQUES']:
    listaEficaciaMP.append({jogador1['NOME']: Eficacia(jogador1['AG'])})
  else:
    listaEficaciaMP.append({jogador2['NOME']: Eficacia(jogador2['AG'])})

print(f'Lista da eficacia dos jogadores menos perigosos: {listaEficaciaMP}')

# MEDIA GERAL DA EFICACIA DOS ATAQUES REALIZADOS CORRETAMENTE

listaMediaE = []

for jogador in listaJogadores:
  listaMediaE.append(Eficacia(jogador.ataques))

MediaE = round(sum(listaMediaE)/ len(listaMediaE),2)

print(f'A media geral da eficacia e {MediaE}')

#ARGUMENTO 2


      # CAPACIDADE DE ADAPTAÇÃO AO JOGO: OS JOGADORES CLASSIFICADOSVARIARAM MAIS ATAQUES QUE A MEDIA DOS JOGADORES NOS JOGOS

# DICIONARIO COM ELEMENTO DOS JOGADORES CLASSIFICADOS PARA O SEGUNDO ARGUMENTO

listaDictsARG2I = []
listaDictsARG2P = []
count = 0

for jogador in listaJogadores:
  if jogador.vitorias == 1 and count %2 == 0:
    listaDictsARG2I.append({'NOME': jogador.nome, 'VJ': VariacaoDeJogadas(jogador.ataques), 'AG': jogador.ataques ,'LG': jogador.levantamentos})  
  elif jogador.vitorias == 1 and count %2 != 0:
    listaDictsARG2P.append({'NOME': jogador.nome, 'VJ': VariacaoDeJogadas(jogador.ataques), 'AG': jogador.ataques ,'LG': jogador.levantamentos})  

  count = count + 1

# VARIAÇÃO DE JOGADAS DOS JOGADORES CLASSIFICADOS

jogadorClassificadoVJ = []

for jogador1, jogador2 in list(zip(listaDictsARG2I,listaDictsARG2P)):
  jogadorClassificadoVJ.append({jogador1['NOME'] : jogador1['VJ']})
  jogadorClassificadoVJ.append({jogador2['NOME'] : jogador2['VJ']})

print(f"Lista dos Jogadores Classificados e a quantidade de jogadas variadas: {jogadorClassificadoVJ}")

# JOGADOR QUE MAIS VARIOU PONTOS NA DUPLA E SUA CONVERSAO DE PONTOS

listaPVePC = []

for jogador1, jogador2 in list(zip(listaDictsARG2I, listaDictsARG2P)):
  if jogador1['VJ'] > jogador2['VJ']:
    listaPVePC.append({jogador1['NOME'] : PontosConvertidos(jogador1['AG'], jogador2['LG'])})
  elif jogador1['VJ'] < jogador2['VJ']:
    listaPVePC.append({jogador2['NOME'] : PontosConvertidos(jogador2['AG'], jogador1['LG'])})

print(f'Lista dos jogadores que mais variou jogadas da dupla e sua porcentagem de conversao de pontos {listaPVePC}')

# MEDIA DAS VARIACOES DE JOGADAS DE TODOS OS JOGADORES

listaPMediaVJ = []

for jogador in listaJogadores:
  listaPMediaVJ.append(VariacaoDeJogadas(jogador.ataques))

MediaVJ = round(sum(listaPMediaVJ)/len(listaPMediaVJ),2)
print(f"Essa e a media das Jogadas Variadas pelos jogadores {MediaVJ}")

# MEDIA GERAL DE CONVERSÃO DE PONTOS

listaJogadoresImpar = []
listaJogadoresPar = []

cont = 0

for jogador in listaJogadores:
  if cont == 0:
    listaJogadoresPar.append(jogador)
  elif cont % 2 != 0:
    listaJogadoresImpar.append(jogador)
  elif cont % 2 == 0:
    listaJogadoresPar.append(jogador)

  cont = cont + 1
       
listaPMediaPC = []

for jogador1, jogador2 in zip(listaJogadoresImpar, listaJogadoresPar):                    #ESSE LOOP ITERA SOBRE AS DUPLAS E RETORNA NA listaPMediaPC os pontos convertidos
  listaPMediaPC.append(PontosConvertidos(jogador1.ataques, jogador2.levantamentos))
  listaPMediaPC.append(PontosConvertidos(jogador2.ataques, jogador1.levantamentos)) 

MediaPC = round((sum(listaPMediaPC)/ (len(listaPMediaPC))),2)
print(f"Essa e a media geral de pontos convertidos {MediaPC}")
