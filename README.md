📊 Fórum Sentiment & Emotion Analysis Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Hugging Face](<https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-yellow?style=for-the-badge>)
![Pandas](<https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas>)
![Seaborn](<https://img.shields.io/badge/Seaborn-Data%20Viz-3776AB?style=for-the-badge>)
![OpenPyXL](<https://img.shields.io/badge/OpenPyXL-Excel%20Export-217346?style=for-the-badge>)

[PT-BR] Pipeline automatizada em Python para limpeza de texto, classificação multi-classe de emoções e geração de relatórios estatísticos (Excel/PNG) em fóruns acadêmicos e comunidades, utilizando modelos *Transformers* ajustados para o português.

[EN] An automated Python pipeline for text pre-processing, multi-class emotion classification, and statistical reporting (Excel/PNG) in academic and community forums, leveraging fine-tuned Portuguese *Transformer* models.

---

## 🎯 Objetivo / Objective

* **PT-BR:** Mapear o clima emocional (ex: raiva, admiração, frustração, desespero, alegria) em interações de fórum, aplicando remoção de ruídos de texto e gerando relatórios tabulares e visuais para apoio à tomada de decisão.
* **EN:** Map emotional climate (e.g., anger, admiration, disappointment, joy) in forum interactions, applying text noise cleaning and generating tabular and visual reports for data-driven decisions.

---

## 🛠️ Stack Tecnológica / Tech Stack

* **Language:** Python 3.12+
* **NLP Model:** `pysentimiento/bert-pt-emotion` (BERT fine-tuned for Portuguese multi-class emotion classification)
* **Pre-processing:** Regular Expressions (`re`) para sanitização de URLs, tags HTML, Markdown e menções (`@usuario`), preservando pontuação expressiva e emojis.
* **Data Manipulation & Export:** Pandas & OpenPyXL
* **Visualization:** Seaborn & Matplotlib
* **Version Control:** Git & GitHub

---

## ⚙️ Fluxo da Pipeline / Pipeline Workflow

1. **Auto-setup & Ingestão:** Identifica ou gera dados de exemplo com ruídos de formatação em `analise_forum/mensagens_forum.csv`.
2. **Pré-processamento (Limpeza):** Sanitiza links, tags, marcadores Markdown e menções sem perder a carga emotiva e semântica do texto.
3. **Classificação por IA:** Realiza inferência em lote via modelo *Transformer* para identificar a emoção predominante e o grau de confiança.
4. **Relatório Excel:** Exporta o arquivo `resultados_analise.xlsx` contendo abas para **Análise Detalhada** e **Resumo Percentual**.
5. **Visualização Gráfica:** Gera e salva o gráfico de distribuição percentual de emoções em alta resolução (`distribuicao_emocoes.png`).

---

## 📁 Estrutura do Projeto / Project Structure

```text
analise-emocional-foruns/
├── analise_forum/
│   ├── emotionClassificator.py   # Script principal da pipeline
│   ├── mensagens_forum.csv       # Dataset de entrada
│   ├── resultados_analise.xlsx   # Relatório detalhado em Excel
│   └── distribuicao_emocoes.png  # Gráfico gerado em alta resolução
├── .gitignore
└── README.md
```
