import os
import warnings
import pandas as pd

from cleaner import limpar_texto
from classifier import ClassificadorEmocoes
from reporter import gerar_resumo, salvar_excel, gerar_grafico

warnings.filterwarnings('ignore')

# Definição dos diretórios isolados
PASTA_DADOS = "analise_forum/dados"
PASTA_RESULTADOS = "analise_forum/resultados"

ARQUIVO_ENTRADA = os.path.join(PASTA_DADOS, "mensagens_forum.csv")
ARQUIVO_SAIDA = os.path.join(PASTA_RESULTADOS, "resultados_analise.xlsx")
GRAFICO_SAIDA = os.path.join(PASTA_RESULTADOS, "distribuicao_emocoes.png")

def garantir_estrutura_diretorios():
    """Garante que as pastas de dados e resultados existam."""
    os.makedirs(PASTA_DADOS, exist_ok=True)
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

def garantir_csv_exemplo():
    """Gera o CSV de teste na pasta de dados caso não exista."""
    garantir_estrutura_diretorios()
    if not os.path.exists(ARQUIVO_ENTRADA):
        dados_exemplo = pd.DataFrame({
            "id_mensagem": range(1, 7),
            "mensagem": [
                "O portal <a href='link'>portal.univ.edu</a> tá travado de novo!! @suporte resolve isso por favor 😡",
                "**Excelente** a aula de hoje! Os slides ajudaram bastante. Valeu @caio_monitor 🙌✨",
                "estou   totalmente   perdido   no   trabalho...   alguém   pode   me   ajudar??? #ajuda",
                "Gente, adiaram a data de entrega para a próxima sexta!! 🎉🎉🎉 www.forum.edu/avisos @todos",
                "@maria_123 acho que vou reprovar nessa matéria... tô bem desanimado 😔",
                "Alguém sabe se o laboratório de IA vai estar aberto amanhã? `python main.py`"
            ]
        })
        dados_exemplo.to_csv(ARQUIVO_ENTRADA, index=False, encoding='utf-8')
        print(f"[Info] CSV de teste criado em: '{ARQUIVO_ENTRADA}'")

def executar_pipeline():
    garantir_csv_exemplo()

    print(f"Lendo mensagens de '{ARQUIVO_ENTRADA}'...")
    df = pd.read_csv(ARQUIVO_ENTRADA)

    print("Aplicando limpeza de texto...")
    df['mensagem_limpa'] = df['mensagem'].apply(limpar_texto)

    classificador = ClassificadorEmocoes()
    emocoes, confiancas = classificador.classificar(df['mensagem_limpa'].tolist())

    df['Emocao'] = emocoes
    df['Confianca'] = confiancas

    df_resumo = gerar_resumo(df)

    print("Salvando relatórios e visualizações na pasta de resultados...")
    salvar_excel(df, df_resumo, ARQUIVO_SAIDA)
    gerar_grafico(df_resumo, GRAFICO_SAIDA)

if __name__ == "__main__":
    executar_pipeline()