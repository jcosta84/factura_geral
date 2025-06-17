import pandas as pd
import streamlit as st
import plotly.express as px
import io
from io import StringIO

st.set_page_config(page_title="Conversão de dados - Script Facturação",
                   layout="wide",
                   page_icon=":bar_chart:")

# Cabeçalho
colunas = ['BOA IND', 'EMP ID', 'UNIDADE', 'PRODUTO', 'DT PROC', 'DT FACT', 'NR FACT', 'CLI ID', 'CLI CONTA', 'CIL',
           'TP FACT', 'TP CLI', 'COD TARIFA', 'VAL TOT', 'CONCEITO', 'QTDE', 'VALOR']

# Tabela Unidade
unidade = pd.DataFrame([
    ['10201000', 'Praia'], ['10202000', 'São Domingos'], ['10203000', 'Santa Catarina'], ['10204000', 'Tarrafal'],
    ['10205000', 'Calheta'], ['10206000', 'Santa Cruz'], ['10701000', 'Mosteiros'], ['10702000', 'São Filipe'],
    ['10801000', 'Maio'], ['10901000', 'Brava'], ['10101000', 'Mindelo'], ['10301000', 'SAL'], ['10401000', 'BOAVISTA'],
    ['10501000', 'VILA DA RIBEIRA BRAVA'], ['10601000', 'R.GRANDE - N.S.Rosário'],
    ['10602000', 'PORTO NOVO - S.João Baptista'], ['10603000', 'PAUL - S.António das Pombas'],
    ['10502000', 'Tarrafal S.Nicolau'], ['10000000', 'Electra SUL']
], columns=['UNIDADE', 'Unidade'])
unidade['UNIDADE'] = unidade['UNIDADE'].astype(int)

# Região
regiao = pd.DataFrame([
    ['Praia', 'SUL'], ['São Domingos', 'SUL'], ['Santa Catarina', 'SUL'], ['Tarrafal', 'SUL'], ['Calheta', 'SUL'],
    ['Santa Cruz', 'SUL'], ['Mosteiros', 'SUL'], ['São Filipe', 'SUL'], ['Maio', 'SUL'], ['Brava', 'SUL'],
    ['Mindelo', 'NORTE'], ['SAL', 'NORTE'], ['BOAVISTA', 'NORTE'], ['VILA DA RIBEIRA BRAVA', 'NORTE'],
    ['R.GRANDE - N.S.Rosário', 'NORTE'], ['PORTO NOVO - S.João Baptista', 'NORTE'],
    ['PAUL - S.António das Pombas', 'NORTE'], ['Tarrafal S.Nicolau', 'NORTE']
], columns=['Unidade', 'Região'])

# Produto
produto = pd.DataFrame([
    ['EB', 'Baixa Tensão'], ['EE', 'Baixa Tensão Especial'], ['EM', 'Media Tensão'], ['AG', 'Agua']
], columns=['PRODUTO', 'Produto'])

# Tipo Cliente
tip_client = pd.DataFrame([
    ['72', 'Empresa Publica'], ['82', 'Colectivos'], ['93', 'Industriais'], ['94', 'Construção'],
    ['73', 'Estado-Patrimonio'], ['91', 'Domésticos'], ['92', 'Comércio, Industria, Agricul.'],
    ['21', 'Consumos Próprios'], ['31', 'Autarquias'], ['51', 'Instituições'], ['71', 'Estado-Tesouro'],
    ['XX', 'Clientes Senhas de Água']
], columns=['TP CLI', 'Tipo_Cliente'])

# Tipo Factura
tp_fact = pd.DataFrame([
    ['11', 'Em Ciclo Leitura'], ['12', 'Em Ciclo Estimativa'], ['22', 'Baixa Voluntária'], ['23', 'Baixa por Dívida'],
    ['24', 'Alterações Contratuais'], ['28', 'Baixa Forçada'], ['29', 'Substit. Modif.'], ['30', 'Substituição'],
    ['33', 'Acerto de Cobrança'], ['39', 'Facturação Diversa'], ['99', 'Lig Relig CompPg']
], columns=['TP FACT', 'Tipo_Factura'])

# Tarifa
tarifa = pd.DataFrame([
    ['A1', 'Tarifa Água I'], ['A2', 'Tarifa Água II'], ['A3', 'Tarifa Água III B'], ['A4', 'Tarifa Água III A'],
    ['AD', 'ADA'], ['AP', 'Água Praia'], ['B4', 'Autotanques II'], ['CD', 'Central Dessalinizadora'],
    ['CP', 'Consumos Proprios'], ['R4', 'Autotanques I (Social)'], ['SA', 'Senhas de Água'],
    ['XX', 'Venda de Água Avulso'], ['AV', 'Tarifa Avença'], ['CE', 'Caixa de Escada'],
    ['D1', 'Tarifa D'], ['D11', 'Tarifa D'], ['D2', 'Tarifa D-S. Nicolau'], ['D3', 'Tarifa D-Social-S. Nicolau'],
    ['D4', 'Tarifa D - Maio'], ['D5', 'Tarifa D - Social - Maio'], ['DS', 'Tarifa D - Social'],
    ['IP', 'Iluminação Publica'], ['LM', 'Ligação Provisória - MONO'], ['LP', 'Ligação Provisória'],
    ['LT', 'Ligação Provisória - TRI'], ['LU', 'Ligação Provisória - MONO URG'], ['S1', 'Tarifa Social'],
    ['SF', 'Semáfores'], ['T1', 'Trabalhador Electra-S. Nicolau'], ['T2', 'Trab. Electra Is.RTC-S.Nicolau'],
    ['T3', 'Trabalhador Electra - Maio'], ['T4', 'Trab. Electra Is. RTC - Maio'], ['TB', 'Trabalhador Electra'],
    ['TI', 'Trab. Electra Isento RTC'], ['TU', 'Ligação Provisória - TRI URG'], ['TBP', 'Trabalhador Partilhado'],
    ['TBB', 'Trab. Beneficiário']
], columns=['COD TARIFA', 'Tarifa'])

# Função de carregamento
@st.cache_data
def carregar_facturacao(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    df = pd.read_csv(io.StringIO(content), sep='\t', names=colunas)
    
    df = pd.merge(df, unidade, on='UNIDADE', how='left')
    df = pd.merge(df, regiao, on='Unidade', how='left')
    df = pd.merge(df, produto, on='PRODUTO', how='left')
    df['TP CLI'] = df['TP CLI'].astype(str)
    df = pd.merge(df, tip_client, on='TP CLI', how='left')
    df = pd.merge(df, tp_fact, on='TP FACT', how='left')
    df = pd.merge(df, tarifa, on='COD TARIFA', how='left')

    df = df[['EMP ID', 'Unidade', 'Região', 'Produto', 'DT PROC', 'DT FACT', 'NR FACT',
             'CLI ID', 'CLI CONTA', 'CIL', 'Tipo_Factura', 'Tipo_Cliente', 'Tarifa',
             'VAL TOT', 'CONCEITO', 'QTDE', 'VALOR']]

    df['DT PROC'] = pd.to_datetime(df['DT PROC'], format='%Y%m%d', errors='coerce')
    df['DT FACT'] = pd.to_datetime(df['DT FACT'], format='%Y%m%d', errors='coerce')
    df['DT PROC'] = df['DT PROC'].dt.strftime('%d-%m-%Y')
    df['DT FACT'] = df['DT FACT'].dt.strftime('%d-%m-%Y')
    df['NR FACT'] = df['NR FACT'].astype(str)

    return df

# Upload
uploaded_file = st.file_uploader("Escolha um arquivo de facturação (.txt)", type=["txt"])

if uploaded_file:
    fact5 = carregar_facturacao(uploaded_file)
    fact5['DT FACT dt'] = pd.to_datetime(fact5['DT FACT'], format='%d-%m-%Y', errors='coerce')

    # Sidebar - Filtros
    st.sidebar.header("Filtros")

    reg = st.sidebar.multiselect("Região", options=fact5['Região'].unique())
    clientes = st.sidebar.multiselect("Cliente (CLI ID)", options=fact5['CLI ID'].unique())
    produtos = st.sidebar.multiselect("Produto", options=fact5['Produto'].unique())

    data_min = fact5['DT FACT dt'].min()
    data_max = fact5['DT FACT dt'].max()
    data_inicial, data_final = st.sidebar.date_input("Data de Facturação", [data_min, data_max],
                                                      min_value=data_min, max_value=data_max)

    # Aplicar filtros
    df_filtrado = fact5.copy()
    if reg: df_filtrado = df_filtrado[df_filtrado['Região'].isin(reg)]
    if clientes: df_filtrado = df_filtrado[df_filtrado['CLI ID'].isin(clientes)]
    if produtos: df_filtrado = df_filtrado[df_filtrado['Produto'].isin(produtos)]
    df_filtrado = df_filtrado[
        (df_filtrado['DT FACT dt'] >= pd.to_datetime(data_inicial)) &
        (df_filtrado['DT FACT dt'] <= pd.to_datetime(data_final))
    ]

    # Abas
    tab1, tab2 = st.tabs(["📋 Tabela", "📊 Gráfico"])

    with tab1:
        st.dataframe(df_filtrado, use_container_width=True)

        @st.cache_data
        def convert_df2(df):
            return df.to_csv(sep=';', decimal=',').encode('utf-8-sig')

        csv = convert_df2(df_filtrado)

        st.download_button("⬇️ Download CSV", data=csv, file_name='Facturação.csv', mime='text/csv')

    with tab2:
        grafico = df_filtrado.groupby('Região')['VAL TOT'].sum().reset_index()
        fig = px.bar(grafico, x='Região', y='VAL TOT', title="Total Facturado por Região", color='Região')
        st.plotly_chart(fig, use_container_width=True)
