import os
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from transformers import pipeline
import re

def limpar_texto(texto: str) ->str:
    if not isinstance(texto, str):
        return ""
    """
    Função para limpar o texto removendo URLs, menções, hashtags e caracteres especiais.
    """
    # 1. Remover URLs (http, https, www)
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    
    # 2. Remover menções a usuários (@usuario)
    texto = re.sub(r'@\w+', '', texto)
    
    # 3. Remover tags HTML ou marcadores de formatação Markdown (*, #)
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'[*#_`~]', '', texto)
    
    # 4. Normalizar múltiplos espaços em branco e quebras de linha
    texto = re.sub(r'\s+', ' ', texto).strip()

    # 5. Remover emojis e caracteres especiais
    texto = re.sub(r'[^\w\s.,!?;:]', '', texto)
    
    return texto

warnings.filterwarnings('ignore')

# Caminhos dos arquivos
ARQUIVO_ENTRADA = "analise_forum/mensagens_forum.csv"
ARQUIVO_SAIDA = "analise_forum/resultados_analise.xlsx"
GRAFICO_SAIDA = "analise_forum/distribuicao_emocoes.png"

mensagens_teste = [
            "O portal acadêmico está fora do ar de novo na hora da entrega, que ódio!",
            "Achei a discussão do grupo de hoje muito produtiva e esclarecedora.",
            "Estou completamente perdido com os prazos dessa matéria...",
            "O portal <a href='link'>portal.univ.edu</a> tá travado de novo!! @suporte resolve isso por favor, preciso entregar o TP 😡 https://erro.com/404",
            "**Excelente** a aula de hoje! Os slides sobre *Processamento de Linguagem Natural* ajudaram bastante a esclarecer as dúvidas. Valeu @caio_monitor 🙌✨",
            "estou   totalmente   perdido   no   trabalho...   alguém   pode   me   ajudar???    não entendi o enunciado da questão 3 #ajuda",
            "Gente, adiaram a data de entrega para a próxima sexta!! 🎉🎉🎉 Vejam o aviso oficial em www.forum.edu/avisos_oficiais @todos",
            "@maria_123 acho que vou reprovar nessa matéria... tirei nota muito baixa no teste e tô bem desanimado 😔",
            "Alguém sabe se o laboratório de IA vai estar aberto amanhã à tarde? Preciso testar um script `python main.py` lá."

        ]



# 1. Criar CSV de exemplo caso nao exista
if not os.path.exists(ARQUIVO_ENTRADA):
    dados_exemplo = pd.DataFrame({
        "id_mensagem": range(1, len(mensagens_teste) + 1),
        "mensagem": mensagens_teste
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

# 4. Pré-processamento e Processamento em Lote
print("Aplicando limpeza de texto...")
df_dados['mensagem_limpa'] = df_dados['mensagem'].apply(limpar_texto)

# Passa a versão LIMPA para a IA analisar
mensagens_para_classificar = df_dados['mensagem_limpa'].tolist()
predicoes = classificador(mensagens_para_classificar)

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
