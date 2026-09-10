import os
import warnings
import pandas as pd

from cleaner import limpar_texto
from classifier import ClassificadorEmocoes
from reporter import gerar_resumo, salvar_excel, gerar_grafico
from collector import coletar_avaliacoes_reais

warnings.filterwarnings('ignore')

PASTA_DADOS = "analise_forum/dados"
PASTA_RESULTADOS = "analise_forum/resultados"

ARQUIVO_ENTRADA = os.path.join(PASTA_DADOS, "mensagens_forum.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_RESULTADOS, "resultados_analise.xlsx")
GRAFICO_SAIDA = os.path.join(PASTA_RESULTADOS, "distribuicao_emocoes.png")

def executar_pipeline(coletar_novos_dados: bool = True, qtd_mensagens: int = 50):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    # 1. Etapa de Coleta
    if coletar_novos_dados or not os.path.exists(ARQUIVO_ENTRADA):
        coletar_avaliacoes_reais(limite=qtd_mensagens, caminho_saida=ARQUIVO_ENTRADA)

    print(f"\nLendo mensagens de '{ARQUIVO_ENTRADA}'...")
    df = pd.read_csv(ARQUIVO_ENTRADA)

    # 2. Etapa de Limpeza
    print("Aplicando limpeza de texto...")
    df['mensagem_limpa'] = df['mensagem'].apply(limpar_texto)

    # 3. Etapa de Classificação por IA
    classificador = ClassificadorEmocoes()
    emocoes, confiancas = classificador.classificar(df['mensagem_limpa'].tolist())

    df['Emocao'] = emocoes
    df['Confianca'] = confiancas

    # 4. Etapa de Relatório e Visualização
    df_resumo = gerar_resumo(df)

    print("Salvando relatórios e visualizações...")
    salvar_excel(df, df_resumo, ARQUIVO_SAIDA)
    gerar_grafico(df_resumo, GRAFICO_SAIDA)
    print("\n✅ Pipeline concluída com sucesso!")

if __name__ == "__main__":
    # Coleta 30 comentários reais e roda a pipeline
    executar_pipeline(coletar_novos_dados=True, qtd_mensagens=30)