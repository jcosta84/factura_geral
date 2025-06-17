import pandas as pd
import streamlit as st
import io

st.set_page_config(page_title="Conversão de dados Script Faturação",
                   layout="wide",
                   page_icon=":bar_chart:")

# Cabeçalho original
colunas = ['BOA IND', 'EMP ID', 'UNIDADE', 'PRODUTO', 'DT PROC', 'DT FACT', 'NR FACT',
           'CLI ID', 'CLI CONTA', 'CIL', 'TP FACT', 'TP CLI', 'COD TARIFA', 'VAL TOT',
           'CONCEITO', 'QTDE', 'VALOR']

# Tabelas auxiliares
unidade = pd.DataFrame([
    ['10201000', 'Praia'], ['10202000', 'São Domingos'], ['10203000', 'Santa Catarina'],
    ['10204000', 'Tarrafal'], ['10205000', 'Calheta'], ['10206000', 'Santa Cruz'],
    ['10701000', 'Mosteiros'], ['10702000', 'São Filipe'], ['10801000', 'Maio'],
    ['10901000', 'Brava'], ['10101000', 'Mindelo'], ['10301000', 'SAL'],
    ['10401000', 'BOAVISTA'], ['10501000', 'VILA DA RIBEIRA BRAVA'],
    ['10601000', 'R.GRANDE - N.S.Rosário'], ['10602000', 'PORTO NOVO - S.João Baptista'],
    ['10603000', 'PAUL - S.António das Pombas'], ['10502000', 'Tarrafal S.Nicolau'],
    ['10000000', 'Electra SUL']
], columns=['UNIDADE', 'Unidade'])
unidade['UNIDADE'] = unidade['UNIDADE'].astype(int)

regiao = pd.DataFrame([
    ['Praia', 'SUL'], ['São Domingos', 'SUL'], ['Santa Catarina', 'SUL'], ['Tarrafal', 'SUL'],
    ['Calheta', 'SUL'], ['Santa Cruz', 'SUL'], ['Mosteiros', 'SUL'], ['São Filipe', 'SUL'],
    ['Maio', 'SUL'], ['Brava', 'SUL'], ['Mindelo', 'NORTE'], ['SAL', 'NORTE'], ['BOAVISTA', 'NORTE'],
    ['VILA DA RIBEIRA BRAVA', 'NORTE'], ['R.GRANDE - N.S.Rosário', 'NORTE'],
    ['PORTO NOVO - S.João Baptista', 'NORTE'], ['PAUL - S.António das Pombas', 'NORTE'],
    ['Tarrafal S.Nicolau', 'NORTE']
], columns=['Unidade', 'Região'])

produto = pd.DataFrame([
    ['EB', 'Baixa Tensão'], ['EE', 'Baixa Tensão Especial'],
    ['EM', 'Media Tensão'], ['AG', 'Agua']
], columns=['PRODUTO', 'Produto'])

tip_client = pd.DataFrame([
    ['72', 'Empresa Publica'], ['82', 'Colectivos'], ['93', 'Industriais'], ['94', 'Construção'],
    ['73', 'Estado-Patrimonio'], ['91', 'Domésticos'], ['92', 'Comércio, Industria, Agricul.'],
    ['21', 'Consumos Próprios'], ['31', 'Autarquias'], ['51', 'Instituições'],
    ['71', 'Estado-Tesouro'], ['XX', 'Clientes Senhas de Água']
], columns=['TP CLI', 'Tipo_Cliente'])

tp_fact = pd.DataFrame([
    ['11', 'Em Ciclo Leitura'], ['12', 'Em Ciclo Estimativa'], ['22', 'Baixa Voluntária'],
    ['23', 'Baixa por Dívida'], ['24', 'Alterações Contratuais'], ['28', 'Baixa Forçada'],
    ['29', 'Substit. Modif.'], ['30', 'Substituição'], ['33', 'Acerto de Cobrança'],
    ['39', 'Facturação Diversa'], ['99', 'Lig Relig CompPg']
], columns=['TP FACT', 'Tipo_Factura'])

tarifa = pd.DataFrame([
    ['A1', 'Tarifa Água I'], ['A2', 'Tarifa Água II'], ['A3', 'Tarifa Água III B'],
    ['A4', 'Tarifa Água III A'], ['AD', 'ADA'], ['AP', 'Água Praia'], ['B4', 'Autotanques II'],
    ['CD', 'Central Dessalinizadora'], ['CP', 'Consumos Proprios'], ['R4', 'Autotanques I (Social)'],
    ['SA', 'Senhas de Água'], ['XX', 'Venda de Água Avulso'], ['AV', 'Tarifa Avença'],
    ['CE', 'Caixa de Escada'], ['D1', 'Tarifa D'], ['D11', 'Tarifa D'], ['D2', 'Tarifa D-S. Nicolau'],
    ['D3', 'Tarifa D-Social-S. Nicolau'], ['D4', 'Tarifa D - Maio'], ['D5', 'Tarifa D - Social - Maio'],
    ['DS', 'Tarifa D - Social'], ['IP', 'Iluminação Publica'], ['LM', 'Ligação Provisória - MONO'],
    ['LP', 'Ligação Provisória'], ['LT', 'Ligação Provisória - TRI'],
    ['LU', 'Ligação Provisória - MONO URG'], ['S1', 'Tarifa Social'], ['SF', 'Semáfores'],
    ['T1', 'Trabalhador Electra-S. Nicolau'], ['T2', 'Trab. Electra Is.RTC-S.Nicolau'],
    ['T3', 'Trabalhador Electra - Maio'], ['T4', 'Trab. Electra Is. RTC - Maio'],
    ['TB', 'Trabalhador Electra'], ['TI', 'Trab. Electra Isento RTC'], ['TU', 'Ligação Provisória - TRI URG'],
    ['TBP', 'Trabalhador Partilhado'], ['TBB', 'Trab. Beneficiário']
], columns=['COD TARIFA', 'Tarifa'])

# Função principal
@st.cache_data
def carregar_facturacao(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    df = pd.read_csv(io.StringIO(content), sep='\t', names=colunas)

    df = pd.merge(df, unidade, on='UNIDADE', how='left')
    df = pd.merge(df, regiao, on='Unidade', how='left')
    df = pd.merge(df, produto, on='PRODUTO', how='left')

    df['TP CLI'] = df['TP CLI'].astype(str).str.strip()
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

# Upload do ficheiro
uploaded_file = st.file_uploader("Escolha um arquivo", type=["txt"])

if uploaded_file is not None:
    try:
        fact5 = carregar_facturacao(uploaded_file)

        st.write("Pré-visualização dos dados tratados:")
        st.dataframe(fact5.head(), use_container_width=True)

        # Filtro por Região
        st.sidebar.header("Filtrar Região:")
        reg = st.sidebar.multiselect("Filtrar Região", options=fact5['Região'].unique())
        geral_selection2 = fact5.query("`Região` == @reg") if reg else fact5

        st.dataframe(geral_selection2, use_container_width=True)

        @st.cache_data
        def convert_df2(df):
            return df.to_csv(sep=';', decimal=',').encode('utf-8-sig')

        csv = convert_df2(geral_selection2)

        st.download_button(
            label="Download Facturação",
            data=csv,
            file_name='Facturação.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Erro ao processar o ficheiro: {e}")
