import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import streamlit as st
import requests
import io

# Título do Dashboard
st.title('Resumo de Informações de Projetos de Assentamento de Reforma Agrária (PR)')

# URL do arquivo Excel no repositório GitHub
url = 'https://raw.githubusercontent.com/TheLastEnvoy/dashboard-streamlit/main/info_PAsPR.xlsx'  # Substitua pelo caminho correto do seu arquivo no GitHub

# Fazendo o download do arquivo do repositório
res = requests.get(url)
res.raise_for_status()

# Lendo o arquivo com Pandas
dados = pd.read_excel(io.BytesIO(res.content))

# Substituindo valores não numéricos por NaN
dados.replace('-', pd.NA, inplace=True)

# Selecionando apenas as colunas desejadas
colunas_desejadas = [
    'Código do Projeto/Nome do Projeto',
    'Município Sede',
    'Área (ha)',
    'Nº de Famílias (capac.)',
    'Famílias Assent.'
]

# Convertendo todas as colunas para numérico (float) quando possível
for coluna in colunas_desejadas[2:]:  # A partir da terceira coluna até o final
    dados[coluna] = pd.to_numeric(dados[coluna], errors='coerce')  # Converter para numérico

# Imputando valores nos NaNs (substituindo por zeros neste caso)
imputer = SimpleImputer(strategy='constant', fill_value=0)
dados_imputados = pd.DataFrame(imputer.fit_transform(dados[colunas_desejadas[2:]]))

# Aplicando PCA para redução de dimensionalidade para visualização
pca = PCA(n_components=2)
dados_reduzidos = pca.fit_transform(dados_imputados)

# Obtendo componentes principais
componentes_principais = pd.DataFrame(data=dados_reduzidos, columns=['Componente 1', 'Componente 2'])

# Adicionando componentes principais ao DataFrame original
dados_com_pca = pd.concat([dados[colunas_desejadas], componentes_principais], axis=1)

# Gráfico de dispersão com componentes principais
fig = px.scatter(
    dados_com_pca,
    x='Famílias Assent.',  # Famílias Assent. no eixo X
    y='Área (ha)',  # Área (ha) no eixo Y
    color='Município Sede',  # Cor determinada por Município Sede
    hover_data=['Código do Projeto/Nome do Projeto'],  # Informação ao passar o mouse sobre as bolinhas
    title='Gráfico de dispersão com PCA - área X famílias assentadas'
)
st.plotly_chart(fig)
