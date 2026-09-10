# 📊 Fórum Sentiment & Emotion Analysis Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Hugging Face](<https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-yellow?style=for-the-badge>)
![Pandas](<https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas>)
![Seaborn](<https://img.shields.io/badge/Seaborn-Data%20Viz-3776AB?style=for-the-badge>)
![OpenPyXL](<https://img.shields.io/badge/OpenPyXL-Excel%20Export-217346?style=for-the-badge>)

[PT-BR] Pipeline modular automatizada em Python para limpeza estrita de texto, classificação multi-classe de emoções por IA e geração de relatórios estatísticos (Excel/PNG) para fóruns acadêmicos e comunidades.

[EN] A modular, automated Python pipeline for strict text cleaning, AI-driven multi-class emotion classification, and statistical reporting (Excel/PNG) tailored for academic and community forums.

---

## 🎯 Objetivo / Objective

* **PT-BR:** Mapear o clima emocional (ex: raiva, admiração, frustração, desespero, alegria) em interações de fórum, aplicando sanitização completa de texto para extrair dados brutos e gerando relatórios visuais e tabulares para apoio à tomada de decisão.
* **EN:** Map emotional climate (e.g., anger, admiration, disappointment, joy) in forum interactions through strict text sanitization, producing visual and tabular reports for data-driven decisions.

---

## 🛠️ Stack Tecnológica / Tech Stack

* **Language:** Python 3.12+
* **NLP Model:** `pysentimiento/bert-pt-emotion` (BERT fine-tuned for Portuguese multi-class emotion classification)
* **Pre-processing:** Sanitização via Expressões Regulares (`re`) com remoção de URLs, e-mails, menções (`@usuario`), hashtags (`#tag`), HTML, Markdown, emojis, pontuação e números — preservando exclusivamente o texto bruto e a acentuação em português.
* **Data Manipulation & Export:** Pandas & OpenPyXL
* **Visualization:** Seaborn & Matplotlib
* **Version Control:** Git & GitHub

---

## ⚙️ Fluxo da Pipeline / Pipeline Workflow

1. **Auto-setup & Ingestão:** Identifica ou cria o dataset inicial de teste na pasta `analise_forum/dados/mensagens_forum.csv`.
2. **Pré-processamento (`cleaner.py`):** Aplica limpeza estrita via Regex para remover qualquer ruído visual, símbolos ou pontuações, isolando o texto bruto.
3. **Classificação por IA (`classifier.py`):** Realiza a inferência em lote utilizando o modelo *Transformer* para rotular emoções e calcular a confiança.
4. **Relatórios & Visualização (`reporter.py`):** Salva a planilha detalhada com resumo percentual em `analise_forum/resultados/resultados_analise.xlsx` e o gráfico estatístico em `analise_forum/resultados/distribuicao_emocoes.png`.

---

## 📁 Estrutura do Projeto / Project Structure

```text
analise-emocional-foruns/
├── analise_forum/
│   ├── dados/
│   │   └── mensagens_forum.csv       # Dataset de entrada
│   ├── resultados/
│   │   ├── resultados_analise.xlsx   # Relatório Excel (Detalhes + Resumo)
│   │   └── distribuicao_emocoes.png  # Gráfico gerado em alta resolução
│   ├── cleaner.py                    # Sanitização e limpeza estrita de texto
│   ├── classifier.py                 # Interface com o modelo Hugging Face
│   ├── reporter.py                   # Geração de planilhas Excel e gráficos
│   └── main.py                       # Script orquestrador principal
├── .gitignore
├── requirements.txt                  # Lista de dependências do projeto
└── README.md
```

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
