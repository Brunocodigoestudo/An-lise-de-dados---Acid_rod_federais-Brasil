#!/usr/bin/env python
# coding: utf-8

# # Bibliotecas e pacotes utilizados

# In[1]:


pip install prettytable


# In[2]:


import pandas as pd
from prettytable import PrettyTable
import os
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


# Configurações de estilo para seaborn
sns.set(style="whitegrid")


# # Apontando para o caminho onde estão os arquivos e validando se todos os arquivos estão de acordo.

# In[8]:


# Especifique o diretório onde estão os arquivos CSV
diretorio = r'C:\Users\User\PROJETOS_PYTHON\Análise de Dados\Análise de dados - Acidentes rodovias federais Brasil'


# In[9]:


# Iterar pelos anos
for ano in range(2007, 2016):
    arquivo = f'datatran{ano}.csv'
    caminho_arquivo = os.path.join(diretorio, arquivo)


# In[10]:


for arquivo in os.listdir(diretorio):
    print(arquivo)


# In[11]:


print(f'Lendo arquivo: {caminho_arquivo}')


# In[12]:


for ano in range(2007, 2016):
    arquivo = f'datatran{ano}.csv'
    caminho_arquivo = os.path.join(diretorio, arquivo)
    
    print(f'Lendo arquivo: {caminho_arquivo}')
    
    try:
        # Especificar tipos de dados para as colunas 5 e 6 (br e km)
        col_types = {'br': str, 'km': str}
        
        # Ler o CSV com o delimitador correto, encoding e tipos de dados
        df = pd.read_csv(caminho_arquivo, delimiter=';', encoding='latin-1', dtype=col_types)
        dataframes.append(df)
        
        print('Arquivo lido com sucesso.')
    except Exception as e:
        print(f'Erro ao ler o arquivo {caminho_arquivo}: {e}')


# # Concatenação (union) dos DataFrames e informações do DataFrame

# In[13]:


resultado = pd.concat(dataframes, ignore_index=True)


# In[14]:


# Exibir as primeiras linhas do DataFrame
print(resultado.head())


# In[15]:


df.info


# In[16]:


# Informações sobre o DataFrame (colunas, tipos de dados, etc.)
print(resultado.info())


# # Aqui começamos as análises de dados

# In[18]:


# Contagem de valores únicos em uma coluna específica (por exemplo, 'uf')
uf_counts = resultado['uf'].value_counts()


# In[19]:


# Criar uma tabela para exibir os resultados
table = PrettyTable(['UF', 'Contagem'])
for uf, count in uf_counts.items():
    table.add_row([uf, count])


# In[20]:


print(table)


# In[21]:


# Estatísticas descritivas das colunas numéricas
print("\nEstatísticas Descritivas:")
desc_stats = resultado.describe().transpose()
desc_table = PrettyTable(desc_stats.columns.tolist())  # Convertendo para lista
desc_table.add_row(desc_stats.iloc[0].tolist())  # Convertendo para lista
desc_table.add_row(desc_stats.iloc[1].tolist())  # Convertendo para lista
desc_table.add_row(desc_stats.iloc[3].tolist())  # Convertendo para lista
desc_table.add_row(desc_stats.iloc[7].tolist())  # Convertendo para lista
print(desc_table)


# In[ ]:


Estatísticas Descritivas:
+-----------+---------------------+---------------------+--------+----------+----------+------------+------------+
|   count   |         mean        |         std         |  min   |   25%    |   50%    |    75%     |    max     |
+-----------+---------------------+---------------------+--------+----------+----------+------------+------------+
| 1465837.0 |  21854108.878706157 |  35980197.64098091  |  8.0   | 574842.0 | 964163.0 | 83048039.0 | 83481326.0 |
| 1465837.0 |  2011.0816741561307 |  2.4122189480777307 | 2007.0 |  2009.0  |  2011.0  |   2013.0   |   2015.0   |
| 1465837.0 | 0.04808515544361344 | 0.27727765278435956 |  0.0   |   0.0    |   0.0    |    0.0     |    33.0    |
| 1465837.0 | 0.08410348490316454 | 0.37537308643144235 |  0.0   |   0.0    |   0.0    |    0.0     |    86.0    |
+-----------+---------------------+---------------------+--------+----------+----------+------------+------------+


# # Gráficos

# # 1. Gráfico de Barras Horizontais para Contagem de Acidentes por UF

# In[22]:



plt.figure(figsize=(12, 6))
ax = sns.countplot(y='uf', data=resultado, order=resultado['uf'].value_counts().index, palette='viridis')

# Removendo as linhas verticais e os números do eixo x
ax.set_xticks([])
ax.xaxis.set_ticks_position('none')

# Adicionando rótulos ao lado das barras
for p in ax.patches:
    width = p.get_width()
    ax.annotate(f'{width}', (width, p.get_y() + p.get_height() / 2.),
                ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    
    
# Definindo o título do gráfico
plt.title('Contagem de Acidentes por UF', fontsize=20, fontweight='bold')

plt.show()


# # 2. Gráfico de Pizza para Relação entre Feridos Graves e Mortos

# In[23]:


# 2. Gráfico de Pizza para Relação entre Feridos Graves e Mortos

# Calcula a soma de feridos graves e mortos
total_feridos_graves = resultado['feridos_graves'].sum()
total_mortos = resultado['mortos'].sum()

# Prepara os dados para o gráfico de pizza
dados_pizza = [total_feridos_graves, total_mortos]
rotulos = ['Feridos Graves', 'Mortos']

# Cria o gráfico de pizza
plt.figure(figsize=(8, 8))
explode = (0, 0.1)  # Explode a fatia de "Mortos" para destacá-la
plt.pie(dados_pizza, labels=rotulos, autopct=lambda p: '{:.1f}%\n({:.0f})'.format(p, p * sum(dados_pizza) / 100),
        startangle=80, explode=explode)
plt.title('Distribuição de Feridos Graves e Mortos',fontsize=16, fontweight='bold')
plt.show()


# # 3. Gráfico de Barras para Número Total de Pessoas por Tipo de Acidente

# In[24]:




plt.figure(figsize=(12, 6))
ax = sns.barplot(x='tipo_acidente', y='pessoas', data=resultado, estimator=sum, ci=None, palette='viridis', capsize=0.05, errwidth=1.5)

# Adicionando rótulos acima de cada barra
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.title('Número Total de Pessoas por Tipo de Acidente', fontsize=20, fontweight='bold')  # Título em negrito
plt.xlabel('Tipo de Acidente')
plt.ylabel('')  # Remova o rótulo do eixo y
plt.xticks(rotation=45)
plt.show()


# # Tratando a data e hora

# In[25]:


# Convertendo 'horario' para o formato de tempo
resultado['horario'] = pd.to_datetime(resultado['horario'], format='%H:%M:%S')


# In[26]:


# Extraindo hora, dia da semana e ano
resultado['hora'] = resultado['horario'].dt.hour
resultado['dia_semana'] = resultado['horario'].dt.day_name()


# # 4. Gráfico de barras Total de Mortos por Ano

# In[27]:


# Agrupando e calculando o total de mortos por hora, dia e ano
tabela_mortes = resultado.groupby(['hora', 'dia_semana', 'ano'])['mortos'].sum().reset_index(drop=True)


# In[28]:


# Ordenando a tabela pelo número de mortos em ordem decrescente
resultado = resultado.sort_values(by='mortos', ascending=False)


# In[29]:


# Agrupar o DataFrame pela coluna 'ano' e somar o número de mortos em cada ano
mortes_por_ano = resultado.groupby('ano')['mortos'].sum().reset_index()

# Criar o gráfico de barras
plt.figure(figsize=(12, 6))
ax = sns.barplot(x='ano', y='mortos', data=mortes_por_ano, palette='viridis')

# Adicionar rótulos nas barras
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.title('Número Total de Mortos por Ano', fontsize=16, fontweight='bold')
plt.xlabel('')
plt.ylabel('')
plt.show()

