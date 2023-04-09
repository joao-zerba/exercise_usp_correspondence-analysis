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


#%% Exercício complementar (MCA)

heart = pd.read_csv("heart.csv")

print(heart.head())

#%% Informações gerais do dataset

print(heart.info())

#%% Ajustando categorias da variável "HeartDisease"

heart.loc[heart['HeartDisease']==0,'Disease'] = "No"
heart.loc[heart['HeartDisease']==1,'Disease'] = "Yes"

#%% Selecionando apenas as variáveis categóricas
 

colunas = heart.select_dtypes(['object']).columns

df = heart[colunas]
df

# Neste caso, foi criado um novo dataset "df"

#%% Gerando tabelas de contingência para os pares de variáveis

from itertools import combinations

for item in list(combinations(df.columns, 2)):
    print(item, "\n")
    tabela = pd.crosstab(df[item[0]], df[item[1]])
    
    print(tabela, "\n")
    
    chi2, pvalor, gl, freq_esp = chi2_contingency(tabela)

    print(f"estatística qui²: {chi2}") # estatística qui²
    print(f"p-valor da estatística: {pvalor}") # p-valor da estatística
    print(f"graus de liberdade: {gl} \n") # graus de liberdade

#%% Identificando as variáveis e suas categorias únicas

for col in df:
    print(col, df[col].unique())

#%% Ajustando variáveis (Type = category)

catcols = df.select_dtypes(['object']).columns

df[catcols] = df[catcols].astype('category')

df.info()


#%% Indicação das variáveis utilizadas na MCA

mca_cols = df.select_dtypes(['category']).columns
print(len(mca_cols), 'features used for MCA are', mca_cols.tolist())

#%% Criando a MCA

mca = prince.MCA()

mca = mca.fit(df[mca_cols])


#%% Identificando as coordenadas (categorias e observações)

print(mca.column_coordinates(df[mca_cols]))
print(mca.row_coordinates(df[mca_cols]))

#%% Criando o mapa perceptual

# ax = mca.plot_coordinates(X=df[mca_cols],
#                              figsize=(16,12),
#                              show_row_points = True,
#                              show_column_points = True,
#                              show_row_labels=False,
#                              column_points_size = 100,
#                              show_column_labels = True)
#TODO make perceptual map