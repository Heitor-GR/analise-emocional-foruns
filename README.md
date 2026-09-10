
# 📊 Fórum & App Sentiment Analysis Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Hugging Face](<https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-yellow?style=for-the-badge>)
![Pandas](<https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas>)
![Seaborn](<https://img.shields.io/badge/Seaborn-Data%20Viz-3776AB?style=for-the-badge>)
![OpenPyXL](<https://img.shields.io/badge/OpenPyXL-Excel%20Export-217346?style=for-the-badge>)

[PT-BR] Pipeline modular e aplicação web em Python para extração de avaliações da Google Play Store, limpeza estrita de texto, classificação multi-classe de emoções por IA e geração de relatórios estatísticos (Excel/PNG) para fóruns e apps.

[EN] A modular Python pipeline and web app for extracting Google Play Store reviews, strict text pre-processing, AI-driven multi-class emotion classification, and statistical reporting (Excel/PNG) for forums and mobile apps.

---

## 🎯 Objetivo / Objective

* **PT-BR:** Mapear o clima emocional (ex: *joy*, *anger*, *sadness*, *surprise*, *disgust*, *fear*) em interações de fóruns e avaliações de aplicativos, permitindo a extração de dados via Play Store ou CSV, sanitização de ruídos e visualização interativa via Dashboard Web ou relatórios em HD.
* **EN:** Map emotional climate across forum interactions and app reviews, supporting data ingestion via Play Store scraping or CSV files, text noise cleaning, and visualization through an interactive web dashboard or HD reports.

---

## 🛠️ Stack Tecnológica / Tech Stack

* **Language:** Python 3.12+
* **Web Framework:** Streamlit
* **Scraping / Ingestão:** `google-play-scraper`
* **NLP Model:** `pysentimiento/bert-pt-emotion` (BERT fine-tuned para português)
* **Pre-processing:** Expressões Regulares (`re`) com remoção de URLs, e-mails, menções, hashtags, HTML, emojis e pontuações, preservando a carga semântica do texto.
* **Data Manipulation & Export:** Pandas & OpenPyXL
* **Visualization:** Seaborn & Matplotlib (gráficos HD com paleta semântica por emoção)
* **Version Control:** Git & GitHub

---

## ⚙️ Fluxo da Pipeline / Pipeline Workflow

1. **Ingestão & Scraping (`collector.py`):** Permite ler arquivos CSV locais ou realizar a raspagem em tempo real de avaliações da Google Play Store por `app_id`.
2. **Pré-processamento (`cleaner.py`):** Aplica sanitização via Regex para isolar o texto bruto.
3. **Classificação por IA (`classifier.py`):** Realiza a inferência em lote utilizando o modelo *Transformer* (`pysentimiento`) para definir a emoção e o grau de confiança.
4. **Relatórios HD (`reporter.py`):** Salva a planilha detalhada com resumo percentual em `resultados_analise.xlsx` e o gráfico estilizado em alta resolução (300 DPI) com cores semânticas em `distribuicao_emocoes.png`.
5. **Dashboard Web (`app.py`):** Interface interativa em Streamlit para raspagem, análise ao vivo, filtros por emoção e download dos relatórios.

---

## 📁 Estrutura do Projeto / Project Structure

```text
analise-emocional-foruns/
├── analise_forum/
│   ├── dados/
│   │   └── mensagens_forum.csv       # Dataset de entrada padrão
│   ├── resultados/
│   │   ├── resultados_analise.xlsx   # Relatório Excel (Detalhes + Resumo)
│   │   └── distribuicao_emocoes.png  # Gráfico gerado em alta resolução (300 DPI)
│   ├── app.py                        # Interface Web Interativa (Streamlit)
│   ├── cleaner.py                    # Sanitização estrita de texto
│   ├── classifier.py                 # Interface com o modelo Hugging Face
│   ├── collector.py                  # Scraper de avaliações da Play Store
│   ├── reporter.py                   # Gerador de relatórios Excel e gráficos HD
│   └── main.py                       # Script orquestrador via CLI
├── .gitignore
├── requirements.txt                  # Lista de dependências do projeto
└── README.md
```
