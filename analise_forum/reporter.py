import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def gerar_resumo(df: pd.DataFrame, coluna_emocao: str = 'Emocao') -> pd.DataFrame:
    """Gera a tabela percentual de distribuição de emoções."""
    resumo = df[coluna_emocao].value_counts(normalize=True) * 100
    df_resumo = resumo.reset_index()
    df_resumo.columns = ['Emocao', 'Porcentagem (%)']
    df_resumo['Porcentagem (%)'] = df_resumo['Porcentagem (%)'].round(1)
    return df_resumo

def salvar_excel(df_detalhado: pd.DataFrame, df_resumo: pd.DataFrame, caminho_saida: str):
    """Exporta os DataFrames para um arquivo Excel com duas abas."""
    with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
        df_detalhado.to_excel(writer, sheet_name='Analise_Detalhada', index=False)
        df_resumo.to_excel(writer, sheet_name='Resumo_Percentual', index=False)
    print(f"[Sucesso] Relatório Excel gerado em: '{caminho_saida}'")

def gerar_grafico(df_resumo: pd.DataFrame, caminho_grafico: str):
    """Gera e salva o gráfico de barras em alta resolução."""
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
    plt.savefig(caminho_grafico, dpi=300)
    plt.close()
    print(f"[Sucesso] Gráfico atualizado em: '{caminho_grafico}'")