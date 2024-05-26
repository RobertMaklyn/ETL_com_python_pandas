import streamlit as st
import pandas as pd
import sqlite3


# Conectar ao banco de dados SQlite
conn = sqlite3.connect('C:/Users/Robert/projetoscraping/data/quotes.db')

# Carregar os dados em um DataFrame pandas
df = pd.read_sql_query('SELECT * FROM mercado_livre_items', conn)

# Fechar Conexão com banco de dados
conn.close()

# Titulo da aplicação
st.title('Pesquisa de Mercado - Tênis Esportivo')
col1, col2, col3 = st.columns(3)

#KPI 1: Número total de items
total_items = df.shape[0]
col1.metric(label='Número Total de Itens', value=total_items)

#KPI 2: Número de Marcas Unicas
unique_brands = df['brand'].unique().tolist()
num_unique_brands = len(unique_brands)
col2.metric(label='Número de Marcas Unicas', value=num_unique_brands)

#KPI 3: Preço Médio
average_price = df['new_price'].mean()
col3.metric(label='Preço Médio (R$)', value=f'{average_price:.2f}')

# Quais marcas mais enconctradas até a página 10
st.subheader('marcas mais enconctradas até a página 10')
col1, col2 = st.columns([4,2])
top10_pages_brand = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top10_pages_brand)
col2.write(top10_pages_brand)

# Preço medio por marca
st.subheader('Preço medio por marca')
col1,col2 =st.columns([4,2])
average_price_brand = df.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_brand)
col2.write(average_price_brand)

# Satisfação por marca
st.subheader('Satisfação por marca')
col1,col2 = st.columns([4,2])
zero_reviews = df[df['review_rating_number'] > 0]
review_brand = zero_reviews.groupby('brand')['review_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(review_brand)
col2.write(review_brand)

