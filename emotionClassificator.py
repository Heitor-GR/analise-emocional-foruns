import pandas as pd
from transformers import pipeline
import warnings

#ocultar avisos tecnicos para manter o terminal limpo
warnings.filterwarnings("ignore")

print("Carregando modelo de classificação de emoções...")
#usa um modelo ja treinado para entender emoçoes em portugues

classificador_emocoes = pipeline(
    "text-classification",
    model="pysentimiento/bert-pt-emotion",
    return_all_scores=False,
)

#textos simulando extrações de um forum escolar ou plataforma academica
mensagens_forum = [
    "Estou muito feliz com o resultado do meu trabalho!",
    "Sinto-me triste por não ter conseguido a nota que esperava.",
    "Estou com medo de não conseguir entregar o projeto a tempo.",
    "Estou com raiva do professor por não ter explicado bem a matéria.",
    "Estou surpreso com a quantidade de informações que aprendi hoje.",
    "O portal acadêmico está fora do ar de novo na hora da entrega, que ódio!",
    "Achei a discussão do grupo de hoje muito produtiva e esclarecedora.",
    "Estou completamente perdido com os prazos dessa matéria...",
    "Finalmente consegui entender a lógica do projeto!"
    ]

resultados = []
print("Analisando as mensagens do Forum...\n")

for texto in mensagens_forum:
    predicao = classificador_emocoes(texto)[0]
    resultados.append(
        {
            "texto": texto,
            "emoção": predicao["label"],
            "confianca": f"{round(predicao['score'] * 100, 1)}%"
        }
    )

#exibe o resultado de forma organizada em tabela
df = pd.DataFrame(resultados)
print(df.to_string(index=False))