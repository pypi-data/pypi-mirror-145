#!/usr/bin/env python
# coding: utf-8

#!pip3 install kaleido --upgrade


import numpy as np
import pandas as pd
import plotly.graph_objects as go


def create_table_cloro():
    # Criando tabela
    df = pd.DataFrame(
        {
            'População De': [0, 5001, 10001, 50001, 200001, 500001],
            'População Até': [5000, 10000, 50000, 200000, 500000, np.inf],
            'Nº de Amostras': [6, 9, '8 + (1 para cada 7,5 mil habitantes)', '10 + (1 para cada 10 mil habitantes)', '20 + (1 para cada 20 mil habitantes)', '35 + (1 para cada 50 mil habitantes)']
        }
    )

    # Criando e Ajustando Coluna Adicional
    df['Nº de Amostras Fixo'] = df['Nº de Amostras'].str.split('+').str[0]
    df['Nº de Amostras Fixo'] = df['Nº de Amostras Fixo'].fillna(df['Nº de Amostras']).astype(float)

    # Criando e Ajustando Coluna Adicional
    df['Nº de Amostras Variável'] = df['Nº de Amostras'].str.split('+').str[-1]
    df['Nº de Amostras Variável'] = df['Nº de Amostras Variável'].fillna(0)
    df['Nº de Amostras Variável'] = df['Nº de Amostras Variável'].replace({'\(1 para cada': '','mil habitantes\)': '',',': '.'}, regex=True).astype(float)
    df['Nº de Amostras Variável'] = (df['Nº de Amostras Variável']*1000).astype(int)

    # Tabela
    return df


def numero_amostras_cloro(x):
    df_cloro = create_table_cloro()
    array = np.where(
        (x >= df_cloro['População De']) & (x <= df_cloro['População Até']) & (df_cloro['Nº de Amostras Variável']>0),
        (df_cloro['Nº de Amostras Fixo'] + x/(df_cloro['Nº de Amostras Variável'])),
        np.where(
            (x >= df_cloro['População De']) & (x <= df_cloro['População Até']) & (df_cloro['Nº de Amostras Variável']==0),
                 df_cloro['Nº de Amostras Fixo'], np.nan
        )
    )    
    array = np.trunc(array)
    array = array[~np.isnan(array)]
    return array[0]


def create_table_fluoreto():
    # Criando tabela
    df = pd.DataFrame(
        {
            'População De': [0, 50001, 100001, 100001, 500001, 1000001],
            'População Até': [50000, 100000, 200000, 500000, 1000000, np.inf],
            'Nº de Amostras': [5, 7, 9, 13, 18, 27]
        }
    )
    # Tabela
    return df


def numero_amostras_fluoreto(x):
    df = create_table_fluoreto()
    array = np.where(
        (x >= df['População De']) & (x <= df['População Até']), df['Nº de Amostras'], np.nan
    )
    array = np.trunc(array)
    array = array[~np.isnan(array)]
    return array[0]




