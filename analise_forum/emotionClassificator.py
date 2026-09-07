import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
import warnings

warnings.filterwarnings('ignore')

print("Carregando o modelo de IA Afetiva...")
classificador = pipeline(
    "text-classification",
    model="pysentimiento/bert-pt-emotion",
    return_all_scores=False,
)

mensagens_forum = [
    "O portal acadêmico está fora do ar de novo na hora da entrega, que ódio!",
    "Achei a discussão do grupo de hoje muito produtiva e esclarecedora.",
    "Estou completamente perdido com os prazos dessa matéria...",
    "Finalmente consegui entender a lógica do projeto!",
    "Muito frustrado com a falta de retorno sobre as dúvidas do trabalho.",
    "Que notícia excelente! Adiaram a data final do projeto.",
    "Não sei se vou conseguir entregar tudo, bateu o desespero total.",
    "Ótima explicação na aula de hoje, me ajudou bastante!"
]

resultados = []
for texto in mensagens_forum:
    predicao = classificador(texto)[0]
    resultados.append({
        "Mensagem": texto,
        "Emocao": predicao["label"],
        "Confianca": predicao["score"]
    })

df = pd.DataFrame(resultados)

# 1. TABELA 1: Detalhada por mensagem
print("\n" + "="*60)
print(" TABELA DE ANALISE POR MENSAGEM ")
print("="*60)
print(df[["Mensagem", "Emocao"]].to_string(index=False))

# 2. TABELA 2: Resumo Percentual
resumo_emocoes = df['Emocao'].value_counts(normalize=True) * 100
df_resumo = resumo_emocoes.reset_index()
df_resumo.columns = ['Emocao', 'Porcentagem (%)']
df_resumo['Porcentagem (%)'] = df_resumo['Porcentagem (%)'].round(1)

print("\n" + "="*40)
print(" DISTRIBUICAO PERCENTUAL ")
print("="*40)
print(df_resumo.to_string(index=False))

# 3. GERAÇÃO DO GRÁFICO
plt.figure(figsize=(9, 5))
sns.set_theme(style="whitegrid")

ax = sns.barplot(
    x='Emocao', 
    y='Porcentagem (%)', 
    data=df_resumo, 
    palette='viridis'
)

plt.title('Distribuição Emocional no Fórum Acadêmico', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Emoção Identificada', fontsize=11)
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
plt.savefig('distribuicao_emocoes.png', dpi=300)
print("\n[Sucesso] Imagem do gráfico salva como 'distribuicao_emocoes.png'!")

plt.show()