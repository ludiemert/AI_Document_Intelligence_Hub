# AI Document Intelligence Hub

Projeto de IA + ML + automacao + dados para processar documentos empresariais, comecando por invoices.

## Objetivo Do Projeto

Criar um sistema que le documentos, extrai dados, valida informacoes, calcula risco, salva resultados e gera relatorios de negocio.

Fluxo futuro completo:

```text
Document
↓
OCR reads document text
↓
Python extracts fields
↓
Python validates fields
↓
Python creates risk score
↓
Python saves results in CSV / database
↓
Pandas analyzes the saved data
↓
Flask shows dashboard and charts on a web page
```

## Fluxo Atual Do Projeto

```text
sample_documents/*.txt
↓
invoice_analyzer.py
↓
services/
↓
reports/invoice_results.csv
↓
invoice_data_analysis.py
↓
reports CSV + JSON + charts
```

## Arquivos Python

```text
invoice_analyzer.py
```

Processa invoices, extrai campos, valida dados e cria `reports/invoice_results.csv`.

```text
invoice_data_analysis.py
```

Le `invoice_results.csv`, analisa com Pandas, cria relatorios, JSON, graficos e recomendacoes.

## Arquivos De Dados

```text
reports/invoice_results.csv
```

Dados detalhados de cada invoice.

```text
reports/invoice_summary.csv
```

Resumo geral do processamento.

```text
reports/invoice_summary.json
```

Resumo para futura API/web dashboard.

```text
reports/invoice_monthly_summary.csv
```

Resumo mensal.

```text
reports/invoice_monthly_status_summary.csv
```

Resumo mensal por status.

## Regra De Risco

```text
Missing field -> +15 risk points for each missing field
High total amount above 5000 -> +25 risk points
Risk 0 -> approved
Risk 1 to 49 -> needs_review
Risk 50 to 100 -> high_risk
```

## Conceitos Aprendidos

```text
CSV is good for learning.
SQLite is good for a small app.
PostgreSQL is good for real companies.
Data warehouse is good for big BI.
Parquet is good for big data files.
```

## Funcoes E Responsabilidades

```text
extract_invoice_fields() -> extracts invoice data
validate_invoice() -> checks business rules
show_result() -> shows one invoice result
show_summary() -> shows final summary
main() -> controls the workflow
```

Em ingles A2:

```text
One function has one job.
main() controls the program flow.
Services store reusable functions.
```

## Estrutura Atual Com Services

```text
services/
├── document_loader.py
├── extractor.py
├── validator.py
├── reporter.py
└── csv_exporter.py
```

```text
invoice_analyzer.py -> controls the workflow
services/ -> stores reusable functions
```

## Proxima Estrutura Para Analise

```text
services/
├── analysis_loader.py
├── analytics.py
├── recommendations.py
├── chart_builder.py
└── report_exporter.py
```

## Mercado De TI

Este projeto toca areas como:

```text
Data Analyst
Automation Developer
Junior Python Developer
Business Intelligence
AI/ML Future
RPA / Operations Automation
```

Frase para portfolio:

```text
Built an intelligent document automation system that processes invoices, detects missing fields and risk, generates monthly business reports, and provides data-driven recommendations.
```

## Proximos Passos

```text
1. Separar invoice_data_analysis.py em services
2. Criar Flask backend
3. Criar pagina web com dashboard
4. Adicionar SQLite
5. Adicionar upload de documentos
6. Adicionar OCR
7. Adicionar Machine Learning
```
_____________________
Path precisa ser importado antes de ser usado.
Imports ficam no topo.
Constantes vêm depois dos imports.
Funções vêm depois.
main() fica no final.

Import first.
Use after.
The service loads the data.
The main file controls the flow.
___________________
Metrics are numbers.
Recommendations are advice.
The app uses numbers to create advice.
_____________
services/summaries.py creates summary tables. Summary means short report.
The summary file creates report tables.
The main file calls the summary functions.
____________
