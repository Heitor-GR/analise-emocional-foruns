import os
import warnings
import pandas as pd

from cleaner import limpar_texto
from classifier import ClassificadorEmocoes
from reporter import gerar_resumo, salvar_excel, gerar_grafico
from collector import coletar_avaliacoes_app

warnings.filterwarnings('ignore')

PASTA_DADOS = "analise_forum/dados"
PASTA_RESULTADOS = "analise_forum/resultados"

ARQUIVO_ENTRADA = os.path.join(PASTA_DADOS, "mensagens_forum.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_RESULTADOS, "resultados_analise.xlsx")
GRAFICO_SAIDA = os.path.join(PASTA_RESULTADOS, "distribuicao_emocoes.png")

def executar_pipeline(app_target: str = "com.duolingo", qtd_avaliacoes: int = 50):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    # 1. Coleta via Web Scraper
    coletar_avaliacoes_app(app_id=app_target, limite=qtd_avaliacoes, caminho_saida=ARQUIVO_ENTRADA)

    # 2. Leitura
    print(f"\nLendo comentários de '{ARQUIVO_ENTRADA}'...")
    df = pd.read_csv(ARQUIVO_ENTRADA)

    # 3. Limpeza
    print("Aplicando limpeza de texto...")
    df['mensagem_limpa'] = df['mensagem'].apply(limpar_texto)

    # 4. Classificação por IA
    classificador = ClassificadorEmocoes()
    emocoes, confiancas = classificador.classificar(df['mensagem_limpa'].tolist())

    df['Emocao'] = emocoes
    df['Confianca'] = confiancas

    # 5. Relatórios
    df_resumo = gerar_resumo(df)

    print("Salvando relatórios e gráficos...")
    salvar_excel(df, df_resumo, ARQUIVO_SAIDA)
    gerar_grafico(df_resumo, GRAFICO_SAIDA)
    print("\n✅ Pipeline concluída com sucesso!")

if __name__ == "__main__":
    # Altere o id do app e a quantidade como desejar
    executar_pipeline(app_target="com.duolingo", qtd_avaliacoes=40)