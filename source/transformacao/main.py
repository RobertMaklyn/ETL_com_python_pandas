import pandas as pd
import sqlite3
from datetime import datetime

# Definir o  caminho do arquivo JSONL
df = pd.read_json('C:/Users/Robert/projetoscraping/data/data.jsonl', lines=True)

# Setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Adicionar a coluna _Source com valor fixo
df['_source'] = 'https://lista.mercadolivre.com.br/tenis-de-corrida-masculino'

# Adicionar a coluna _data_coleta com a data e horas atuais
df['_data_coleta'] = datetime.now()

# Tratar valores nulos e coluncas numericas
df['old_prices_reais'] = df['old_prices_reais'].fillna(0).astype(float)
df['old_prices_centavos'] = df['old_prices_centavos'].fillna(0).astype(float)
df['new_prices_reais'] = df['new_prices_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['review_rating_number'] = df['review_rating_number'].fillna(0).astype(float)

# Remover os parênteses das coluna review_amount
df['review_amount'] = df['review_amount'].str.replace('[\(\)]', '', regex=True)
df['review_amount'] = df['review_amount'].fillna(0).astype(int)

# Tratas os preços como float e calcular os valores totais
df['old_price'] = df['old_prices_reais'] + df['old_prices_centavos'] / 100
df['new_price'] = df['new_prices_reais'] + df['new_price_centavos'] / 100

# Remover colunas antigas 
df.drop(columns=['old_prices_reais','old_prices_centavos','new_prices_reais','new_price_centavos'], inplace=True)

# Conectar ao banco de dados SQlite (ou criar um novo)
conn = sqlite3.connect('C:/Users/Robert/projetoscraping/data/quotes.db')

# Salvar o data framase no banco de dados
df.to_sql('mercado_livre_items', conn, if_exists='replace', index=False)

# Fechar Conexão com banco de dados
conn.close()

# para rodar o pandas dentro da pasta source
# python transformacao/main.py