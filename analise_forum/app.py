import os
import sys
import pandas as pd
import streamlit as st

# Garante que o Python encontre os módulos locais (cleaner, classifier, etc.)
sys.path.append(os.path.dirname(__file__))

from cleaner import limpar_texto
from classifier import ClassificadorEmocoes
from reporter import gerar_resumo, salvar_excel, gerar_grafico
from collector import coletar_avaliacoes_app

# Configuração da página Streamlit
st.set_page_config(
    page_title="Fórum & App Sentiment Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Análise Emocional de Comentários & Fóruns")
st.markdown("Extraia avaliações reais da Play Store ou fóruns e analise o clima emocional por IA.")

# Barra lateral de configurações
st.sidebar.header("⚙️ Configurações da Coleta")

app_options = {
    "Duolingo": "com.duolingo",
    "Instagram": "com.instagram.android",
    "Nubank": "com.nu.production",
    "Outro (Digitar ID)": "custom"
}

selecao_app = st.sidebar.selectbox("Escolha o App:", list(app_options.keys()))

if selecao_app == "Outro (Digitar ID)":
    app_id = st.sidebar.text_input("ID do App na Play Store:", "com.spotify.music")
else:
    app_id = app_options[selecao_app]

qtd_avaliacoes = st.sidebar.slider("Quantidade de Avaliações:", min_value=10, max_value=200, value=40, step=10)

btn_executar = st.sidebar.button("🚀 Rodar Análise", type="primary")

@st.cache_resource
def carregar_modelo():
    return ClassificadorEmocoes()

# Execução do pipeline
if btn_executar:
    pasta_base = os.path.dirname(__file__)
    pasta_dados = os.path.join(pasta_base, "dados")
    pasta_resultados = os.path.join(pasta_base, "resultados")
    
    arquivo_csv = os.path.join(pasta_dados, "mensagens_forum.csv")
    arquivo_excel = os.path.join(pasta_resultados, "resultados_analise.xlsx")
    arquivo_grafico = os.path.join(pasta_resultados, "distribuicao_emocoes.png")

    with st.spinner(" Raspando avaliações reais da Play Store..."):
        df = coletar_avaliacoes_app(app_id=app_id, limite=qtd_avaliacoes, caminho_saida=arquivo_csv)

    with st.spinner(" Sanitizando textos e executando inferência por IA..."):
        df['mensagem_limpa'] = df['mensagem'].apply(limpar_texto)
        classificador = carregar_modelo()
        emocoes, confiancas = classificador.classificar(df['mensagem_limpa'].tolist())
        
        df['Emocao'] = emocoes
        df['Confianca'] = confiancas
        df_resumo = gerar_resumo(df)

        salvar_excel(df, df_resumo, arquivo_excel)
        gerar_grafico(df_resumo, arquivo_grafico)

    st.success("✅ Análise concluída com sucesso!")

    # Métricas principais
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Comentários", len(df))
    col2.metric("Emoção Predominante", df_resumo.iloc[0]['Emocao'])
    col3.metric("Média de Confiança", f"{df['Confianca'].mean() * 100:.1f}%")

    st.divider()

    # Visualização em abas
    aba1, aba2, aba3 = st.tabs(["📊 Gráfico de Distribuição", "📄 Tabela de Dados", "📈 Resumo Percentual"])

    with aba1:
        if os.path.exists(arquivo_grafico):
            st.image(arquivo_grafico, use_container_width=True)

    with aba2:
        st.dataframe(df[['id_mensagem', 'mensagem', 'mensagem_limpa', 'Emocao', 'Confianca']], use_container_width=True)

    with aba3:
        st.dataframe(df_resumo, use_container_width=True)

    # Download do Excel
    with open(arquivo_excel, "rb") as file:
        st.download_button(
            label="📥 Baixar Relatório Excel (.xlsx)",
            data=file,
            file_name=f"analise_{app_id}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )