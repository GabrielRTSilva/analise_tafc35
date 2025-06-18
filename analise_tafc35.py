#BIBLIOTECAS

import pandas as pd
import numpy as np


## ------ CLASSE JOGADOR ------ ##

# Essa classe contem os seguintes métodos:
  
  # Objeto:         retorna um dicionario, contendo nome, recepcao, levantamento e ataques (os values das ultimas tres keys sao obejetos tipo list.)
  # Ataques:        retorna uma lista com todos os tipos de ataques realizados.
  # Recepções:      retorna uma lista com todos os tipos de recepções.
  # Levantamentos:  retorna uma lista com todos os tipos de levantamentos realizados.

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
    
  def Objeto(self):  # Mostra o Objeto em Formato Dict
    objeto = {
      'Nome ': self.nome,
      'Vitorias': self.vitorias,
      'Numero da Dupla': self.numeroDupla,
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
  
# FUNÇÃO PARA CRIAR OBJETO DA CLASSE JOGADOR

def TornarJogador(idJogador: int):                                                           # Função que retorna todos os atributos do jogador estruturados na classe Jogador. Type Object
  
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

#FUNÇÕES GENÉRICAS

def limpaDados(lista: list):                                                                 # Função para limpar os dados NaN do array unidimensional
  listaLimpa = []

  for item in lista:
    if item == '-':
      item = 0
      listaLimpa.append(item)
    else:
      listaLimpa.append(item)
  return listaLimpa

def SelecionaMetrica(lista: list, num: int):                                                 # Função para selecionar a métrica, sendo ela acertos (0), bolas que passaram (1) e erros (2) 

  listaLimpa = limpaDados(lista)

  listaDosIndexes = list(range(num, len(listaLimpa), 3))  
  
  metrica = []
  k = 0

  while k < (len(listaDosIndexes)):
    for index, item2 in enumerate(listaLimpa):
      if index == listaDosIndexes[k]:
        metrica.append(listaLimpa[index])
    
    k = k + 1

  return metrica

#FUNÇÕES PARA GERAR PARAMETROS DE ANALISE 

def MovimentoComMaisAcertos (lista: list):                                                   # Funcao que retorna o maior valor da lista e seu indice. Return: type(Dict)

  listaLimpa = limpaDados(lista)

  maxValueIndex = range(len(listaLimpa))
  maxValueZip = dict(zip(maxValueIndex, listaLimpa))
  maxValue = max(maxValueZip.items(), key=lambda x: x[1])       # Essa lambda funciona como argumento para a funcao max achar o maior Value do dicionario e retornar 

  listMaxValue = list(maxValue)

  dictMaxValue = {}
  dictMaxValue[listMaxValue[0]] = listMaxValue[1]

  return dictMaxValue

def MovimentoComMenosAcertos (lista: list):                                                  # Funcao que retorna o menor valor da lista e seu indice. Return: type(Dict)
  
  listaLimpa = limpaDados(lista)

  minValueIndex = range(len(listaLimpa))
  minValueZip = dict(zip(minValueIndex, listaLimpa))
  minValue = min(minValueZip.items(), key=lambda x: x[1])       # Essa lambda funciona como argumento para a funcao max achar o maior Value do dicionario e retornar 

  listMinValue = list(minValue)

  dictMinValue = {}
  dictMinValue[listMinValue[0]] = listMinValue[1]

  return dictMinValue

def MediaMetrica(lista: list, num: int):                                                     # Calcula a media da lista. Return: type(float) 

  acertos = SelecionaMetrica(lista, num)
    
  mediaList = round(float(sum(acertos) / len(acertos)),2)

  return mediaList

def Eficacia (lista: list):                                                                  # Calcula a eficacia de um atributo da classe levantamento e rececpcao. Return: type(float, round(2)) 
  
  listaLimpa = limpaDados(lista)

  acertos = SelecionaMetrica(listaLimpa, 0)
  
  eficacia = round((sum(acertos)/ sum(listaLimpa)),2)
  
  return eficacia 

def PontosConvertidos(lista: list, lista2: list ):                                           # Calcula a capacidade de aproveitamento de um jogador em converter levantamentos em pontos Return: type(float, round(2))
                                                                                      
  ataquesRealizados = SelecionaMetrica(lista, 0)
  acertosLevantamento = SelecionaMetrica(lista2, 0)

  pontosConvertidos = round((sum(ataquesRealizados) / sum(acertosLevantamento)),2)

  return pontosConvertidos

def VariacaoDeJogadas(lista: list ):                                                         # Funcao que ira retornar quantos ataques o jogador variou 

  listaLimpa = limpaDados(lista)     
  
  listaPontos = SelecionaMetrica(listaLimpa, 0)
  listaNaoPontos = SelecionaMetrica(listaLimpa, 1)

  arr = np.column_stack((listaPontos, listaNaoPontos))

  variacoes = 0
  linha = 0

  while linha < len(arr):                             # Esse loop percorre as linhas e os elementos das linhas para contar se houve variacao dos ataques
    for i in arr[linha]:
      if i != 0:
        variacoes += 1
        break
      else:
        continue
    linha += 1                        

  return variacoes

# DADOS ESTRUTURADOS PARA ANALISE

      #Jogadores

listaJogadores = [TornarJogador(i) for i in range(1, 33)]

# ANÁLISES 

      #ARGUMENTO 1

# LOOP PARA DIVIDIR AS DUPLAS VENCEDORAS 

listaDictsEficaciaP = []
listaDictsEficaciaI = []

contador = 0

for jogador in listaJogadores:
  if jogador.vitorias == 1 and contador %2 == 0:
    listaDictsEficaciaP.append({'NOME': jogador.nome, 'ATAQUES': sum(SelecionaMetrica(jogador.ataques,0)) + sum(SelecionaMetrica(jogador.ataques,1)), 'AG': jogador.ataques ,'EFICACIA': Eficacia(jogador.ataques)})  
  elif jogador.vitorias == 1 and contador %2 != 0:
    listaDictsEficaciaI.append({'NOME': jogador.nome, 'ATAQUES': sum(SelecionaMetrica(jogador.ataques,0)) + sum(SelecionaMetrica(jogador.ataques,1)), 'AG': jogador.ataques , 'EFICACIA': Eficacia(jogador.ataques)})

  contador = contador + 1

listaDictsEZIP = list(zip(listaDictsEficaciaP, listaDictsEficaciaI))                       # ESSA VARIAVEL CONTEM OS JOGADORES DAS DUPLAS UNIDOS E SEUS ATRIBUTOS

# DADOS PARA GRAFICO DE RELAÇÃO DE ATAQUES RECEBIDOS POR DUPLAS

ataquesJogador1 = []
ataquesJogador2 = []

for jogador1, jogador2 in listaDictsEZIP:
  ataquesJogador1.append({jogador1['NOME']: jogador1['ATAQUES']})
  ataquesJogador2.append({jogador2['NOME']: jogador2['ATAQUES']})

# DADOS PARA GRAFICOS DOS JOGADORES MENOS PERIGOSOS E SUAS EFICACIAS

listaEficaciaMP = []

for jogador1, jogador2 in listaDictsEZIP:
  if jogador1['ATAQUES'] > jogador2['ATAQUES']:
    listaEficaciaMP.append({jogador1['NOME']: Eficacia(jogador1['AG'])})
  else:
    listaEficaciaMP.append({jogador2['NOME']: Eficacia(jogador2['AG'])})

# MEDIA GERAL DA EFICACIA DOS ATAQUES REALIZADOS CORRETAMENTE

listaMediaE = []

for jogador in listaJogadores:
  listaMediaE.append(Eficacia(jogador.ataques))

MediaE = round(sum(listaMediaE)/ len(listaMediaE),2)

      #ARGUMENTO 2

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

# JOGADOR QUE MAIS VARIOU PONTOS NA DUPLA E SUA CONVERSAO DE PONTOS

listaPVePC = []

for jogador1, jogador2 in list(zip(listaDictsARG2I, listaDictsARG2P)):
  if jogador1['VJ'] > jogador2['VJ']:
    listaPVePC.append({jogador1['NOME'] : PontosConvertidos(jogador1['AG'], jogador2['LG'])})
  elif jogador1['VJ'] < jogador2['VJ']:
    listaPVePC.append({jogador2['NOME'] : PontosConvertidos(jogador2['AG'], jogador1['LG'])})

# MEDIA DAS VARIACOES DE JOGADAS DE TODOS OS JOGADORES

listaPMediaVJ = []

for jogador in listaJogadores:
  listaPMediaVJ.append(VariacaoDeJogadas(jogador.ataques))

MediaVJ = round(sum(listaPMediaVJ)/len(listaPMediaVJ),2)

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

# DADOS ESTRUTURADOS

      # GRÁFICO 1

colunaDuplas = []
colunaNomesG1 = []
colunaAtaques = []

for jogador in listaJogadores:
  if jogador.vitorias == 1:
    colunaDuplas.append(jogador.numeroDupla)
    colunaNomesG1.append(jogador.nome)
    colunaAtaques.append(sum(SelecionaMetrica(jogador.ataques,0)) + sum(SelecionaMetrica(jogador.ataques,1)))

      # GRÁFICO 2

listaDictsEficaciaP = []
listaDictsEficaciaI = []

contador = 0

for jogador in listaJogadores:
  if jogador.vitorias == 1 and contador %2 == 0:
    listaDictsEficaciaP.append({'NOME': jogador.nome, 'ATAQUES': sum(SelecionaMetrica(jogador.ataques,0)) + sum(SelecionaMetrica(jogador.ataques,1)), 'AG': jogador.ataques ,'EFICACIA': Eficacia(jogador.ataques)})  
  elif jogador.vitorias == 1 and contador %2 != 0:
    listaDictsEficaciaI.append({'NOME': jogador.nome, 'ATAQUES': sum(SelecionaMetrica(jogador.ataques,0)) + sum(SelecionaMetrica(jogador.ataques,1)), 'AG': jogador.ataques , 'EFICACIA': Eficacia(jogador.ataques)})

  contador = contador + 1

listaDictsEZIP = list(zip(listaDictsEficaciaP, listaDictsEficaciaI))

ataquesJogador1 = []
ataquesJogador2 = []

for jogador1, jogador2 in listaDictsEZIP:
  ataquesJogador1.append({jogador1['NOME']: jogador1['ATAQUES']})
  ataquesJogador2.append({jogador2['NOME']: jogador2['ATAQUES']})

colunaNomesG2 = []
colunaEficacia = []
mediaEficacia = 0.26

for jogador1, jogador2 in listaDictsEZIP:
  if jogador1['ATAQUES'] > jogador2['ATAQUES']:
    colunaNomesG2.append(jogador1['NOME'])
    colunaEficacia.append(Eficacia(jogador1['AG']))
  else:
    colunaNomesG2.append(jogador2['NOME'])
    colunaEficacia.append(Eficacia(jogador1['AG']))

      # GRÁFICO 3

colunaJogadasVariadas = []
mediaJogadasVariadas = 6 
contador = 0

for jogador in listaJogadores:
  if jogador.vitorias == 1:
    colunaJogadasVariadas.append(VariacaoDeJogadas(jogador.ataques))

      # GRÁFICO 4

listaDictsARG2I = []
listaDictsARG2P = []
count = 0

for jogador in listaJogadores:
  if jogador.vitorias == 1 and count %2 == 0:
    listaDictsARG2I.append({'NOME': jogador.nome, 'VJ': VariacaoDeJogadas(jogador.ataques), 'AG': jogador.ataques ,'LG': jogador.levantamentos})  
  elif jogador.vitorias == 1 and count %2 != 0:
    listaDictsARG2P.append({'NOME': jogador.nome, 'VJ': VariacaoDeJogadas(jogador.ataques), 'AG': jogador.ataques ,'LG': jogador.levantamentos}) 
  count = count + 1

colunaPontosConvertidos = []
colunaNomesG4 = []
mediaPontosConvertidos = 0.40

for jogador1, jogador2 in list(zip(listaDictsARG2I, listaDictsARG2P)):
  colunaPontosConvertidos.append(PontosConvertidos(jogador1['AG'], jogador2['LG']))
  colunaNomesG4.append(jogador1['NOME'])
  colunaPontosConvertidos.append(PontosConvertidos(jogador2['AG'], jogador1['LG']))
  colunaNomesG4.append(jogador2['NOME'])

# DATA FRAME PARA ANALISE

      # TABELA PARA O GRÁFICO 1 

grafico1 = {'NOME' : colunaNomesG1, 'No DUPLA': colunaDuplas, 'ATAQUES' : colunaAtaques}
TabelaG1 = pd.DataFrame(grafico1)
TabelaG1.to_excel('TabelaG1.xlsx')

      # TABELA PARA O GRÁFICO 2

grafico2 = {'NOME': colunaNomesG2, 'EFICÁCIA': colunaEficacia, 'MediaGEficacia': mediaEficacia}
TabelaG2 = pd.DataFrame(grafico2)
TabelaG2.to_excel('TabelaG2.xlsx')

      # TABELA PARA O GRÁFICO 3

grafico3 = {'NOME': colunaNomesG1, 'Jogadas Variadas(JV)': colunaJogadasVariadas, 'Media JV': mediaJogadasVariadas}
TabelaG3 = pd.DataFrame(grafico3)
TabelaG3.to_excel('TabelaG3.xlsx')

      # TABELA PARA O GRÁFICO 4

grafico4 = {'NOME': colunaNomesG4, 'PontosConvertidos (PC)': colunaPontosConvertidos, 'Media PC': mediaPontosConvertidos}
TabelaG4 = pd.DataFrame(grafico4)
TabelaG4.to_excel('TabelaG4.xlsx')

