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
O controlador é o arquivo que organiza o fluxo, mas não faz todo o trabalho sozinho.

Temos dois controladores principais:

invoice_analyzer.py
invoice_data_analysis.py

The controller controls the flow.
It calls service functions.
It does not do every job alone.
_____________________

invoice_analyzer.py
Responsabilidade:

ler documentos .txt
extrair dados
validar invoices
salvar invoice_results.csv

Fluxo:

sample_documents/*.txt
↓
load_invoice_texts()
↓
extract_invoice_fields()
↓
validate_invoice()
↓
show_result()
↓
show_summary()
↓
save_results_to_csv()

____________________________

invoice_data_analysis.py
Responsabilidade:

ler invoice_results.csv
analisar com Pandas
gerar resumo, JSON, gráficos e recomendação

Fluxo:
reports/invoice_results.csv
↓
load_invoice_data()
↓
add_date_columns()
↓
calculate_status_counts()
↓
calculate_business_metrics()
↓
create_recommendation()
↓
create_monthly_summary()
↓
create_monthly_status_summary()
↓
save reports
↓
create charts
________________________________________

services/document_loader.py
Função:
load_invoice_texts()

O que faz:

lê arquivos .txt da pasta sample_documents
também lê subpastas com rglob
retorna texto + caminho do arquivo
Em inglês A2:

It loads invoice text files.
It returns text and source file path.
___________________________________

services/extractor.py
Função:
extract_invoice_fields()

O que faz:

pega texto cru da invoice
encontra invoice_number, supplier, dates, total, currency, VAT
transforma texto em dicionário
Em inglês A2:

It extracts fields from invoice text.
It creates organized data.
_________________________________________
services/validator.py
Função:
validate_invoice()

O que faz:

verifica campos obrigatórios
calcula risk_score
define status
cria reasons
Status:

approved
needs_review
high_risk
Em inglês A2:

It checks invoice data.
It returns status, risk score, and reasons.

__________________________________________________

services/reporter.py
Funções:
show_result()
show_summary()

O que faz:

mostra resultado no terminal
mostra resumo final do processamento
Em inglês A2:

It prints results in the terminal.
______________________________________________

services/csv_exporter.py
Função:
save_results_to_csv()

O que faz:

salva invoices processadas em reports/invoice_results.csv
usa separador ; para abrir bem no Excel
Em inglês A2:

It saves processed invoices to CSV.

______________________________________

services/analysis_loader.py
Funções:

load_invoice_data()
add_date_columns()
O que faz:

lê invoice_results.csv com Pandas
cria invoice_year e invoice_month
Em inglês A2:

It loads CSV data.
It adds year and month columns.
_____________________________________________________
services/analytics.py
Funções:

show_invoice_data()
calculate_status_counts()
calculate_business_metrics()
O que faz:

mostra tabela
conta status
calcula total amount, average risk e percentage review
Em inglês A2:

It calculates business numbers.
______________________________________________

services/recommendations.py
Função:

create_recommendation()
O que faz:

usa métricas para gerar uma sugestão empresarial
Exemplo:

More than 50% of invoices need review...
Em inglês A2:

It creates business advice from metrics.
___________________________________________________

services/summaries.py
Funções:

create_monthly_summary()
create_monthly_status_summary()
O que faz:

cria resumo mensal
cria resumo mensal por status
Em inglês A2:

It creates monthly report tables.
________________________________________________
services/report_exporter.py
Funções:

save_monthly_reports()
save_summary_files()
O que faz:

salva CSVs de resumo
salva invoice_summary.json
Em inglês A2:

It saves report files.
CSV is for tables.
JSON is for web apps.
_________________________________
services/chart_builder.py
Funções:

create_status_chart()
create_risk_score_chart()
create_monthly_status_chart()
O que faz:

cria imagens PNG dos gráficos
salva em reports/
Em inglês A2:

It creates chart images.
Charts help users see the data.
________________________________________________

controllers -> controlam o fluxo
services -> fazem trabalhos específicos
sample_documents -> entrada
reports -> saída
____________________________________________

No nosso projeto:

Create -> salvar uma invoice processada no banco
Read -> buscar invoices para relatório/dashboard
Update -> alterar status de uma invoice
Delete -> remover uma invoice errada ou duplicada

linha atual: TXT -> Python -> CSV -> Pandas -> JSON -> Charts
___________________________________
