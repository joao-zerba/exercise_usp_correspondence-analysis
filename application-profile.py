# -*- coding: utf-8 -*-

"""
Análise de Correspondência Simples e Múltipla

Referências:
Wilson Tarantin Junior
Helder Prado Santos

"""
#%% Carregar as bibliotecas

# Executar o seguinte comando no console: pip install -r requirements.txt

# Em seguida, importar os pacotes

import pandas as pd
import prince
from scipy.stats import chi2_contingency

#%% Análise de Correspondência Simples (ANACOR)

# Importar o banco de dados
## Fonte: Fávero e Belfiore (2017, Capítulo 11)

perfil = pd.read_excel("perfil_aplicacao.xlsx")

print(perfil)

#%% Analisando os dados do dataset

print(perfil.info())

#%% Analisando as características descritivas das variáveis do dataset

print(perfil.describe())

#%% Criando a tabela de contingência

tabela = pd.crosstab(perfil["Perfil"], perfil["Tipo de Aplicação"])

print(tabela)

#%% Analisando a significância estatística da associação (teste qui²)

chi2, pvalor, df, freq_esp = chi2_contingency(tabela)

print(f"estatística qui²: {chi2}") # estatística qui²
print(f"p-valor da estatística: {pvalor}") # p-valor da estatística
print(f"graus de liberdade: {df}") # graus de liberdade

#%% Elaborando a ANACOR

# Inicializando a instância da Anacor
ca = prince.CA()

#%% Ajustes do dataframe

# Renomeando as linhas e colunas do dataframe

tabela.columns.rename('Investimento', inplace=True)
tabela.index.rename('Perfil', inplace=True)

print(tabela)

#%% Fit do modelo

# Note que o input é a tabela de contingência criada antes

ca = ca.fit(tabela)

#%% Obtendo as coordenadas em linha e coluna

print(ca.row_coordinates(tabela), "\n")
print(ca.column_coordinates(tabela))

#%% Obtendo os eigenvalues

print(ca.eigenvalues_)

#%% Obtendo a inércia principal total

# É a soma dos eigenvalues (também é a divisão: estat. qui² / N)
# Quanto maior a inércia principal total, maior é a associação entre categorias

print(ca.total_inertia_)

#%% Inércia explicada por dimensão

# Indica o percentual da a inércia principal total explicado por cada dimensão

#print(ca.explained_inertia_)

#%% Massas em linhas

print(ca.row_masses_)

#%% Massas em colunas

print(ca.col_masses_)

#%% Por fim, podemos plotar o mapa perceptual

# ax = ca.plot_coordinates(X=tabela,
#                          ax=None,
#                          figsize=(10,10),
#                          x_component=0,
#                          y_component=1,
#                          show_row_labels=True,
#                          show_col_labels=True)

#%% Plotando o mapa percentual interativo

import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default='browser'

chart_df = pd.DataFrame({'obs_x':ca.row_coordinates(tabela)[0].values,
                         'obs_y': ca.row_coordinates(tabela)[1].values})

fig = go.Figure(data=go.Scatter(x=chart_df['obs_x'],
                                y=chart_df['obs_y'],
                                name=tabela.index.name,
                                textposition="top center",
                                text=tabela.index,
                                mode="markers+text",))

fig.add_trace(go.Scatter(
    x=ca.column_coordinates(tabela)[0].values,
    mode="markers+text",
    name=tabela.columns.name,
    textposition="top center",
    y=ca.column_coordinates(tabela)[1].values,
    text=ca.column_coordinates(tabela).index
))

fig.update_layout(
    autosize=False,
    width=800,
    height=800,
    title_text='Coordenadas principais'

)

fig.show()