import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_resumo(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula a proporção e percentual de cada emoção."""
    df_resumo = df['Emocao'].value_counts(normalize=True).reset_index()
    df_resumo.columns = ['Emocao', 'Proporcao']
    df_resumo['Percentual'] = (df_resumo['Proporcao'] * 100).round(1)
    return df_resumo

def salvar_excel(df: pd.DataFrame, df_resumo: pd.DataFrame, caminho_saida: str):
    """Salva os resultados em uma planilha Excel com duas abas."""
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with pd.ExcelWriter(caminho_saida, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Detalhado', index=False)
        df_resumo.to_excel(writer, sheet_name='Resumo_Percentual', index=False)

def gerar_grafico(df_resumo: pd.DataFrame, caminho_saida: str):
    """Gera um gráfico de barras estilizado e de alta resolução."""
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    # Palette de cores semânticas para cada emoção
    CORES_EMOCOES = {
        # Emoções Básicas & Primárias
        'joy': '#10b981',           # Verde esmeralda
        'sadness': '#2563eb',       # Azul royal
        'anger': '#dc2626',         # Vermelho vivo
        'surprise': '#f59e0b',      # Amarelo âmbar
        'disgust': '#ea580c',       # Laranja queimado
        'fear': '#7c3aed',          # Roxo violeta
        'neutral': '#64748b',       # Cinza neutro
        'others': '#64748b',        # Cinza neutro


        # Emoções Expandidas
        'admiration': '#06b6d4',    # Ciano
        'amusement': '#84cc16',     # Verde lima
        'annoyance': '#f43f5e',     # Rosa carmim
        'approval': '#14b8a6',      # Verde água / Teal
        'caring': '#ec4899',        # Rosa magenta
        'confusion': '#a855f7',     # Violeta claro
        'curiosity': '#0284c7',     # Azul céu
        'desire': '#be123c',        # Vermelho vinho
        'disappointment': '#6b7280',# Cinza azulado
        'disapproval': '#b91c1c',   # Vermelho escuro
        'embarrassment': '#f97316', # Laranja vivo
        'excitement': '#eab308',    # Amarelo ouro
        'gratitude': '#059669',     # Verde folha
        'love': '#e11d48',          # Rosa rubi
        'pride': '#8b5cf6',         # Roxo elétrico
        'relief': '#3b82f6',        # Azul claro
        'remorse': '#4b5563'        # Cinza escuro
    
    }
    
    # Define as cores baseadas nas emoções presentes no resultado
    palette = [CORES_EMOCOES.get(str(e).lower(), '#34495e') for e in df_resumo['Emocao']]

    # Configuração da figura e tema
    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)

    # Plotagem das barras
    bars = sns.barplot(
        data=df_resumo,
        x='Emocao',
        y='Percentual',
        palette=palette,
        ax=ax,
        width=0.5
    )

    # Adiciona rótulo numérico (ex: 45.0%) acima de cada barra
    for p in bars.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(
                f'{height:.1f}%',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                fontsize=10, fontweight='bold',
                color='#2c3e50',
                xytext=(0, 5),
                textcoords='offset points'
            )

    # Títulos e Rótulos
    ax.set_title("Distribuição Emocional das Mensagens", fontsize=14, fontweight='bold', pad=18, color='#2c3e50')
    ax.set_xlabel("Emoção Detectada", fontsize=10, fontweight='bold', color='#7f8c8d', labelpad=10)
    ax.set_ylabel("Percentual (%)", fontsize=10, fontweight='bold', color='#7f8c8d', labelpad=10)
    
    # Margem superior para não cortar o texto dos percentuais
    max_val = df_resumo['Percentual'].max() if not df_resumo.empty else 100
    ax.set_ylim(0, max_val * 1.2)

    # Refinamento visual (remove bordas desnecessárias e adiciona grid suave)
    sns.despine(top=True, right=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.4, color='#bdc3c7')
    ax.set_axisbelow(True)

    # Salva em alta resolução
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')
    plt.close()