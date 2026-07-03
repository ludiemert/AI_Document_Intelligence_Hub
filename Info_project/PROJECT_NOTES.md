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

CSV is good for tables.
JSON is good for web apps.
The dashboard can read JSON.
__________________________________

JSON needs simple values.
Date becomes text.
This helps the web read the data.
________________________________

Toda vez adicionar a chamada no controlador, mas a função o service.
_________________________________________

Sempre:  Rodar Pipeline
Rode na ordem:

python invoice_analyzer.py
python invoice_data_analysis.py
_____________
The app reads many years.
The app creates one report per year.
The yearly chart compares years.
_____________________
The app reads invoices from many years.
The app creates yearly reports.
The chart compares invoice amount by year.
The business recommendation changes with the data.
_________________________

Amount shows money volume.
Risk shows document quality.
Both are important for business.

The app compares yearly amount.
The app compares yearly risk.
This helps business decisions.

_______________________________________

Já temos o backend/data pipeline gerando:

reports/invoice_summary.json
reports/business_recommendations.json
reports/status_counts.png
reports/risk_scores.png
reports/monthly_status_counts.png
reports/yearly/yearly_invoice_amount.png
reports/yearly/yearly_average_risk.png
__________________________________
Fluxo futuro:
Python creates JSON/charts
↓
Frontend reads JSON/charts
↓
Dashboard shows metrics
↓
Later Flask connects everything
______________________

The frontend shows the data.
The JSON gives data to the dashboard.
Flask will connect backend and frontend later.
___________________

Python creates JSON/charts
↓
Frontend reads JSON/charts
↓
Dashboard shows metrics
↓
Later Flask connects everything

________________

The frontend shows the data.
The JSON gives data to the dashboard.
Flask will connect backend and frontend later.
__________________________

Start front
Use um servidor local. Na raiz do projeto:

python -m http.server 8000

Depois abra no navegador: http://localhost:8000/frontend/

_____________________________________________

HTML has IDs
JavaScript finds IDs
JavaScript reads JSON
JavaScript updates the page

JavaScript reads JSON data.
JavaScript updates HTML text.
The dashboard becomes automatic.

_______________________________________________
estilo:

Nome Visual

AI Document Intelligence Hub
Conceito

Smart business automation dashboard
Paleta

Dark navy: #111827
Deep teal: #0F766E
Soft cyan: #E0F2FE
Success green: #16A34A
Warning amber: #F59E0B
Risk red: #DC2626
Light background: #F8FAFC
Card white: #FFFFFF
Text dark: #1F2937
Text muted: #64748B
Por Que Essa Paleta

navy -> tecnologia e empresa
teal -> automação e inteligência
green -> aprovado
amber -> revisão
red -> risco
light background -> dashboard limpo
Em inglês A2:

The colors show business and technology.
Green means approved.
Amber means review.
Red means risk.
________________________________

Edge
Opção 1: Print De Uma Área = Use: Windows + Shift + S

Chrome
1. Ctrl + Shift + I
2. Ctrl + Shift + P
3. Digitar screenshot
4. Clicar em Capture full size screenshot
Capturar captura de tela em tamanho completo


_______________________________

PNG chart = static
HTML/JS chart = dynamic
Dynamic chart updates with filters
Em inglês A2:
JavaScript creates the bars.
The bars use filtered data.
The chart changes when filters change.
__________________________________________

JavaScript creates chart bars.
The chart uses filtered invoices.
The chart changes when filters change.

_________________________

HTML/CSS/JS puro:
bom para aprender a lógica
sem dependência externa
mais código manual
menos visual profissional

Chart.js:
visual mais profissional
código de gráfico mais organizado
fácil criar bar, line, pie
usa uma biblioteca externa
precisa aprender a estrutura do Chart.js
___________________________________________

Regra simples para lembrar:
Online -> CDN
Offline -> vendor/chart.umd.min.js
Nunca os dois ao mesmo tempo agora.
E sim: se chart.umd.min.js estiver vazio e você usar só ele, o navegador vai dizer algo como:
Chart is not defined

Usar online agora:
https://cdn.jsdelivr.net/npm/chart.js

Usar offline depois:
vendor/chart.umd.min.js
________________________________________

TXT -> Python -> CSV/JSON -> Pandas -> reports -> Frontend -> Chart.js

_____________________________

<!-- This chart shows the average risk score by year. -->
<!-- Chart.js updates this chart when filters change. -->
<article class="chart-card dashboard-section general-section yearly-section">
    <h2>Yearly Average Risk</h2>

    <!-- This canvas is used by Chart.js. -->
    <canvas id="yearly-risk-chart"></canvas>
</article>

Então a lógica fica assim:
general-section -> aparece em General
monthly-section -> aparece em Monthly
yearly-section  -> aparece em Yearly
________________________________

canvas é para desenhar coisas visuais, como:
bar chart
line chart
pie chart
visual graph

Chart / gráfico -> canvas
Text / cards / alerts / table -> div, section, p, table
____________________________________________

protótipo profissional do dashboard usando JSON. Quando entrar Flask, a lógica muda assim:
Agora:
HTML + JS lê reports/invoice_results.json

Depois com Flask:
HTML + JS chama API Flask
/api/invoices
/api/summary
/api/risk-alerts
______________________________

app.py  -> backend Flask, roda no Python
app.js  -> frontend JavaScript, roda no navegador

app.py = servidor
app.js = interação da página

Python / Flask
app.py
↓
manda index.html para o navegador
↓
index.html carrega styles.css e app.js
↓
app.js chama a API Flask e atualiza dashboard
_____________________
open Flask
4. Rode o backend:
python app.py
5. Abra no navegador:
http://127.0.0.1:5000
_______________________________________

app.js
↓
calls /api/invoices
↓
Flask app.py reads reports/invoice_results.json
↓
Flask returns JSON
↓
frontend updates dashboard
________________
Agora o fluxo correto é:
frontend/app.js
↓
GET /api/invoices
↓
Flask app.py
↓
reports/invoice_results.json
↓
dashboard
______________________________

o endereço principal passa a ser:
http://127.0.0.1:5000/
Esse é o endereço do Flask backend.
O antigo:
http://localhost:8000/frontend/
era do servidor simples do Python:
python -m http.server 8000

A lógica nova é:
http://127.0.0.1:5000/
↓
Flask abre o dashboard
↓
Flask entrega CSS e JS
↓
app.js chama /api/invoices
↓
Flask entrega os dados
______________

para rodar o projeto:
python app.py
E abrir:
http://127.0.0.1:5000/

_______________________

Antes: localhost:8000/frontend/ -> front estático
Agora: 127.0.0.1:5000 -> Flask + API + dashboard
__________________
favicon.svg

A = AI
azul escuro = enterprise / tech
verde = data / intelligence
amarelo = alert / risk

_____________________________
Miniobjetivo:
Clicar em Top Risk Invoices
abrir página Flask com detalhes da invoice

Esse passo é bem alinhado com mercado, porque ensina:
Flask routes
dynamic URL
backend data lookup
template rendering
frontend-backend navigation

Em inglês A2:
The dashboard shows many invoices.
The detail page shows one invoice.
Flask finds the invoice by invoice number.
_______________________________
1. app.py -> criar rota /invoice/<invoice_number>
2. frontend/invoice_detail.html -> criar página de detalhe
3. app.js -> trocar clique para abrir rota Flask
_________________
