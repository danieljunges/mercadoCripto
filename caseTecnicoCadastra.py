# -*- coding: utf-8 -*-
"""Case Técnico - Cadastra"""

import requests
import pandas as pd
import psycopg2
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

def tratar_limite_requisicoes(resposta, url):
    tentativas = 0
    while resposta.status_code == 429 and tentativas < 5:
            tempo_espera = 2 ** tentativas
            print(f"Limite de requisições atingido em {url}. Esperando {tempo_espera} segundos...")
            time.sleep(tempo_espera)
            resposta = requests.get(url)
            tentativas += 1
    return resposta


def converterTimestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def pegarAssets():
    url = 'https://api.coincap.io/v2/assets'
    resposta = requests.get(url)
    resposta = tratar_limite_requisicoes(resposta, url)
    if resposta.status_code == 200:
        dados = resposta.json()['data']
        return pd.DataFrame(dados)
    else:
        return None

def pegarAssetPorId(id):
    url = f'https://api.coincap.io/v2/assets/{id}'
    resposta = requests.get(url)
    resposta = tratar_limite_requisicoes(resposta, url)
    if resposta.status_code == 200:
        dados = resposta.json()['data']
        return pd.DataFrame([dados])
    else:
        return None

def pegarHistoricoAsset(id):
    url = f'https://api.coincap.io/v2/assets/{id}/history?interval=d1'
    resposta = requests.get(url)
    resposta = tratar_limite_requisicoes(resposta, url)
    if resposta.status_code == 200:
        dados = resposta.json()['data']
        for item in dados:
            item['time'] = converterTimestamp(item['time'])
        return pd.DataFrame(dados)
    else:
        return None

def pegarExchanges():
    url = 'https://api.coincap.io/v2/exchanges'
    resposta = requests.get(url)
    resposta = tratar_limite_requisicoes(resposta, url)
    if resposta.status_code == 200:
        dados = resposta.json()['data']
        return pd.DataFrame(dados)
    else:
        return None

def pegarMarkets():
    url = 'https://api.coincap.io/v2/markets'
    resposta = requests.get(url)
    resposta = tratar_limite_requisicoes(resposta, url)
    if resposta.status_code == 200:
        dados = resposta.json()['data']
        return pd.DataFrame(dados)
    else:
        return None

load_dotenv()


def conectar_banco():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_DATABASE"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT")
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def inserir_assets(df, conn):
    cur = conn.cursor()
    for index, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO assets (id, rank, symbol, name, supply, maxSupply, marketCapUsd, volumeUsd24Hr, priceUsd, changePercent24Hr, vwap24Hr)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['id'], row['rank'], row['symbol'], row['name'], row['supply'], row['maxSupply'], row['marketCapUsd'], row['volumeUsd24Hr'], row['priceUsd'], row['changePercent24Hr'], row['vwap24Hr']))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
    cur.close()

def inserir_asset_por_id(df, conn):
    cur = conn.cursor()
    for index, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO asset_por_id (id, rank, symbol, name, supply, maxSupply, marketCapUsd, volumeUsd24Hr, priceUsd, changePercent24Hr, vwap24Hr)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['id'], row['rank'], row['symbol'], row['name'], row['supply'], row['maxSupply'], row['marketCapUsd'], row['volumeUsd24Hr'], row['priceUsd'], row['changePercent24Hr'], row['vwap24Hr']))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
    cur.close()

def inserir_historico_asset(df, conn, asset_id):
    cur = conn.cursor()
    for index, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO historico_asset (priceUsd, time, asset_id)
                VALUES (%s, %s, %s)
            """, (row['priceUsd'], row['time'], asset_id))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
    cur.close()

def inserir_exchanges(df, conn):
    cur = conn.cursor()
    for index, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO exchanges (exchangeId, name, rank, percentTotalVolume, volumeUsd, tradingPairs, socket, exchangeUrl)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['exchangeId'], row['name'], row['rank'], row['percentTotalVolume'], row['volumeUsd'], row['tradingPairs'], row['socket'], row['exchangeUrl']))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            print(f"Exchange com ID {row['exchangeId']} já existe na tabela.")
            conn.rollback()
    cur.close()

def inserir_markets(df, conn):
    cur = conn.cursor()
    for index, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO markets (exchangeId, rank, baseSymbol, baseId, quoteSymbol, quoteId, priceQuote, priceUsd, volumeUsd24Hr, percentExchangeVolume, tradesCount24Hr)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['exchangeId'], row['rank'], row['baseSymbol'], row['baseId'], row['quoteSymbol'], row['quoteId'], row['priceQuote'], row['priceUsd'], row['volumeUsd24Hr'], row['percentExchangeVolume'], row['tradesCount24Hr']))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
    cur.close()

def main():
    conn = conectar_banco()
    if conn:
        criptomoedas = ['bitcoin', 'solana', 'ethereum']
        df_assets = pegarAssets()
        if df_assets is not None:
            inserir_assets(df_assets, conn)
            print("Dados de assets inseridos com sucesso!")

        for cripto in criptomoedas:
            df_asset_por_id = pegarAssetPorId(cripto)
            if df_asset_por_id is not None:
                inserir_asset_por_id(df_asset_por_id, conn)
                print(f"Dados de asset_por_id para {cripto} inseridos com sucesso!")

            df_historico_asset = pegarHistoricoAsset(cripto)
            if df_historico_asset is not None:
                inserir_historico_asset(df_historico_asset, conn, cripto)
                print(f"Dados de historico_asset para {cripto} inseridos com sucesso!")

        df_exchanges = pegarExchanges()
        if df_exchanges is not None:
            if not df_exchanges.empty:
                inserir_exchanges(df_exchanges, conn)
                print("Dados de exchanges inseridos com sucesso!")
            else:
                print("DataFrame df_exchanges está vazio. Nenhum dado foi inserido.")

        df_markets = pegarMarkets()
        if df_markets is not None:
            inserir_markets(df_markets, conn)
            print("Dados de markets inseridos com sucesso!")

        conn.close()
    else:
        print("Não foi possível conectar ao banco de dados.")

if __name__ == "__main__":
    main()

