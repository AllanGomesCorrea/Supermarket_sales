#Retirado database de https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales/data
import pandas as pd
import matplotlib.pyplot as plt


file_name = 'supermarket_sales.csv'
df = pd.read_csv(file_name)


#Inspecionar o dataframe inicial
# print('Número de colunas = ',len(df.columns))
# print(df.columns.tolist())
# print('Total de linhas = ', len(df))
#print(df.head(5))

#As colunas desejadas a serem trabalhadas
# select_columns = [
#     '',
# ]
# df_selected = df[select_columns].copy()


#Explorar os dados

#Analisar a distribuicao entre as 4 colunas 
print(df.groupby(['City'])['Invoice ID'].count())
print(df.groupby(['Customer type'])['Invoice ID'].count())
print(df.groupby(['Gender'])['Invoice ID'].count())
print(df.groupby(['Product line'])['Invoice ID'].count())

#Agrupar um pouco mais para identificar detalhes
print(df.groupby(['City', 'Gender'])['Invoice ID'].count())
print(df.groupby(['City', 'Customer type'])['Invoice ID'].count())
print(df.groupby(['City', 'Gender', 'Customer type'])['Invoice ID'].count()) #identificar a onde aumentar numero de members

#Investigar um grupo específico e mostrar as categorias uma por uma
group_exp = df.groupby(['City', 'Gender', 'Customer type'])['Product line']
print(group_exp.get_group(('Yangon', 'Male', 'Member')).value_counts())

# Criar gráfico de barras
# df_aux = group_exp.get_group(('Yangon', 'Male', 'Member')).value_counts()
# plt.figure(figsize=(10, 6))
# plt.bar(df_aux.index, df_aux.values, color='skyblue')
# plt.xlabel('Categoria')
# plt.ylabel('Quantidade')
# plt.title('Quantidade de compras (Yangon, Male, Member) por categoria')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()


#Investigar o consumo feminino e masculino
print(df.groupby(['Gender', 'Customer type', 'Product line'])['Invoice ID'].count()) #identificar onde o membro tem maior consumo
total_products = df.groupby(['Gender', 'Customer type', 'Product line'])['Quantity'].sum()
total_products_df = pd.DataFrame(total_products)
print(total_products_df.sort_values(['Gender', 'Quantity'], ascending=False))
# Plotar gráfico de barras
index = total_products.index
df_aux = pd.DataFrame(total_products.values, index=index, columns=['Quantity'])
# plt.figure(figsize=(10, 6))
# plt.bar(df_aux.index.map(str), df_aux['Quantity'], color='skyblue')
# plt.xlabel('Categoria')
# plt.ylabel('Quantidade')
# plt.title('Número de produtos (Gender, Member) por categoria')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()
df_aux.to_csv('quantidade_produtos.csv')


#Explorar o total em dinheiro do consumo feminino e masculino
total_price = df.groupby(['Gender', 'Customer type', 'Product line'])['Total'].sum()
print(total_price)
total_price_df = pd.DataFrame(total_price)
print(total_price_df.sort_values(['Gender', 'Total'], ascending=False)) #apesar de Sports ser o mais vendido entre Members Female, ele está em 3. Food lidera o ranking de vendas em valor
# Plotar gráfico de barras
df_aux = total_price_df.copy()
# plt.figure(figsize=(10, 6))
# plt.bar(df_aux.index.map(str), df_aux['Total'], color='skyblue')
# plt.xlabel('Categoria')
# plt.ylabel('Total')
# plt.title('Número total $ (Gender, Member) por categoria')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()
df_aux.to_csv('total.csv')

#Explorar o valor dos itens
print(df.groupby(['Customer type', 'Product line'])['Unit price'].mean())
print(df.groupby(['Customer type', 'Product line'])['Quantity'].mean())
