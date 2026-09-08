import os
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from transformers import pipeline

warnings.filterwarnings('ignore')

# Caminhos dos arquivos
ARQUIVO_ENTRADA = "analise_forum/mensagens_forum.csv"
ARQUIVO_SAIDA = "analise_forum/resultados_analise.xlsx"
GRAFICO_SAIDA = "analise_forum/distribuicao_emocoes.png"

# 1. Criar CSV de exemplo caso nao exista
if not os.path.exists(ARQUIVO_ENTRADA):
    dados_exemplo = pd.DataFrame({
        "id_mensagem": range(1, 9),
        "mensagem": [
            "O portal acadêmico está fora do ar de novo na hora da entrega, que ódio!",
            "Achei a discussão do grupo de hoje muito produtiva e esclarecedora.",
            "Estou completamente perdido com os prazos dessa matéria...",
            "Finalmente consegui entender a lógica do projeto!",
            "Muito frustrado com a falta de retorno sobre as dúvidas do trabalho.",
            "Que notícia excelente! Adiaram a data final do projeto.",
            "Não sei se vou conseguir entregar tudo, bateu o desespero total.",
            "Ótima explicação na aula de hoje, me ajudou bastante!"
        ]
    })
    # Garantir que a pasta analise_forum existe
    os.makedirs("analise_forum", exist_ok=True)
    dados_exemplo.to_csv(ARQUIVO_ENTRADA, index=False, encoding='utf-8')
    print(f"[Info] CSV de teste criado em: '{ARQUIVO_ENTRADA}'")

# 2. Carregar o Modelo de IA de EMOÇÕES
print("Carregando o modelo de IA de Emoções (pysentimiento/robertuito-emotion-pt)...")
classificador = pipeline(
    "text-classification",
    model="pysentimiento/bert-pt-emotion",
    return_all_scores=False,
)

# 3. Leitura dos dados do CSV
print(f"Lendo mensagens de '{ARQUIVO_ENTRADA}'...")
df_dados = pd.read_csv(ARQUIVO_ENTRADA)

# 4. Processamento em lote
mensagens = df_dados['mensagem'].tolist()
predicoes = classificador(mensagens)

df_dados['Emocao'] = [p['label'] for p in predicoes]
df_dados['Confianca'] = [round(p['score'], 4) for p in predicoes]

# 5. Tabela de Resumo Percentual de Emoções
resumo = df_dados['Emocao'].value_counts(normalize=True) * 100
df_resumo = resumo.reset_index()
df_resumo.columns = ['Emocao', 'Porcentagem (%)']
df_resumo['Porcentagem (%)'] = df_resumo['Porcentagem (%)'].round(1)

# 6. Salvar em Excel com duas abas (Detalhado + Resumo)
with pd.ExcelWriter(ARQUIVO_SAIDA, engine='openpyxl') as writer:
    df_dados.to_excel(writer, sheet_name='Analise_Detalhada', index=False)
    df_resumo.to_excel(writer, sheet_name='Resumo_Percentual', index=False)

print(f"[Sucesso] Relatório Excel gerado em: '{ARQUIVO_SAIDA}'")

# 7. Gerar e salvar gráfico de barras
plt.figure(figsize=(9, 5))
sns.set_theme(style="whitegrid")

ax = sns.barplot(
    x='Emocao', 
    y='Porcentagem (%)', 
    data=df_resumo, 
    palette='viridis'
)

plt.title('Distribuição de Emoções no Fórum Acadêmico', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Emoção Detectada', fontsize=11)
plt.ylabel('Proporção (%)', fontsize=11)
plt.ylim(0, max(df_resumo['Porcentagem (%)']) + 15)

for p in ax.patches:
    altura = p.get_height()
    if altura > 0:
        ax.annotate(f'{altura:.1f}%', 
                    (p.get_x() + p.get_width() / 2., altura), 
                    ha='center', va='center', 
                    xytext=(0, 6), 
                    textcoords='offset points',
                    fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(GRAFICO_SAIDA, dpi=300)
print(f"[Sucesso] Gráfico atualizado em: '{GRAFICO_SAIDA}'")
