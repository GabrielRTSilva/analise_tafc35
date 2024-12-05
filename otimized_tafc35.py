import pandas as pd
import numpy as np

class Jogador:
    def __init__(self, nome, numeroDupla, pernaBoa, vitorias, ataques, recepcoes, levantamentos):
        self.nome = nome
        self.numeroDupla = numeroDupla
        self.pernaBoa = pernaBoa
        self.vitorias = vitorias
        self.ataques = ataques
        self.recepcoes = recepcoes
        self.levantamentos = levantamentos
    
    def objeto(self):
        return {
            'Nome': self.nome,
            'Vitorias': self.vitorias,
            'Numero da Dupla': self.numeroDupla,
            'Ataques': self.ataques,
            'Recepções': self.recepcoes,
            'Levantamentos': self.levantamentos
        }

# Carregamento e limpeza dos dados

def carregar_dados():
    sheets = pd.read_excel('tafc35-smalldata.xlsx', sheet_name=None)
    return sheets

def criar_jogador(dados, idJogador):
    info_jogador = dados['Sheet1'].iloc[idJogador-1].replace('-', 0)
    ataques = dados['Sheet3'].iloc[idJogador].replace('-', 0)
    recepcoes = dados['Sheet4'].iloc[idJogador].replace('-', 0)
    levantamentos = dados['Sheet5'].iloc[idJogador].replace('-', 0)
    
    return Jogador(info_jogador['Nome'], info_jogador['NumeroDupla'], info_jogador['PernaBoa'],
                   info_jogador['Vitorias'], ataques.tolist(), recepcoes.tolist(), levantamentos.tolist())

# Funções 

def eficacia(ataques):
    ataques = np.array(ataques)
    return np.round(ataques[ataques != 0].mean(), 2)

def variacao_de_jogadas(ataques):
    ataques = np.array(ataques)
    return len(ataques[ataques != 0])

# Exemplo de uso
dados = carregar_dados()
jogadores = [criar_jogador(dados, i) for i in range(1, 33)]

# Exemplo de análise
eficacias = [eficacia(jogador.ataques) for jogador in jogadores]
variacao_jogadas = [variacao_de_jogadas(jogador.ataques) for jogador in jogadores]

