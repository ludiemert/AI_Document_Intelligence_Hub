# AI Document Intelligence Hub - Project Notes

Este arquivo guarda minhas anotações de aprendizado sobre o projeto **AI Document Intelligence Hub**.

O objetivo é documentar como o projeto foi crescendo, quais tecnologias foram usadas, o que cada parte faz e como explicar esse sistema em entrevistas ou no portfólio.

---

## Project Idea

O projeto é um sistema de automação inteligente para documentos empresariais, começando por invoices.

Ele recebe documentos, extrai dados, valida informações, calcula risco, salva em banco de dados e mostra os resultados em um dashboard web.

Em inglês A2:

```text
The app reads invoices.
The app extracts invoice data.
The app checks business rules.
The app saves data in SQLite.
The dashboard shows charts and reports.
```

---

## Current Main Flow

```text
User uploads invoice
↓
Flask receives the file
↓
OCR/Text Reader gets text
↓
Extractor gets invoice fields
↓
Validator checks business rules
↓
SQLite saves invoice data
↓
API sends data to JavaScript
↓
Dashboard shows cards, charts, alerts, and table
↓
BI Reports exports CSV and JSON files
```

---

## Project Evolution

## Phase 1 - Simple Python

No começo, o projeto processava textos de invoices dentro do Python.

Aprendizado:

```text
Python functions
Dictionaries
Field extraction
Risk validation
Console output
```

Arquivo principal da fase inicial:

```text
invoice_analyzer.py
```

Fluxo antigo:

```text
raw invoice text
↓
extracted fields
↓
validation result
↓
summary report
```

---

## Phase 2 - CSV And Pandas

Depois, o projeto começou a salvar resultados em CSV e analisar com Pandas.

Fluxo antigo:

```text
invoice_analyzer.py
↓
reports/invoice_results.csv
↓
invoice_data_analysis.py
↓
summary CSV
↓
JSON
↓
charts
```

Aprendizado:

```text
CSV stores table data.
Pandas reads CSV files.
Pandas calculates metrics.
JSON is useful for web apps and APIs.
Charts help business analysis.
```

Importante:

```text
CSV was the first learning step.
Now SQLite is the main data source.
CSV and JSON are now export reports.
```

---

## Phase 3 - Flask Dashboard

Depois, o projeto ganhou uma interface web com Flask.

Fluxo:

```text
Flask
↓
HTML
↓
CSS
↓
JavaScript
↓
Dashboard
```

Aprendizado:

```text
Flask creates web routes.
HTML creates the page structure.
CSS creates the visual style.
JavaScript updates the dashboard.
Chart.js creates dynamic charts.
```

---

## Main Routes

```text
/                -> dashboard
/api/invoices    -> invoice data API
/upload          -> upload invoice page
/reports         -> BI reports page
/architecture    -> project architecture page
/invoice/<id>    -> invoice detail page
```

---

## Current Project Structure

```text
AI_Document_Intelligence_Hub/
├── app.py
├── data/
│   └── invoices.db
├── frontend/
│   ├── index.html
│   ├── upload.html
│   ├── reports.html
│   ├── architecture.html
│   ├── invoice_detail.html
│   ├── styles.css
│   ├── app.js
│   └── favicon.svg
├── routes/
│   ├── dashboard_routes.py
│   ├── upload_routes.py
│   ├── report_routes.py
│   └── architecture_routes.py
├── services/
│   ├── database.py
│   ├── invoice_repository.py
│   ├── invoice_processor.py
│   ├── extractor.py
│   ├── validator.py
│   ├── ocr_reader.py
│   ├── text_cleaner.py
│   └── exporter.py
├── uploads/
├── reports/
├── sample_documents/
├── archive/
├── README.md
└── Info_project/
    └── PROJECT_NOTES.md
```

---

## What Each Main File Does

## app.py

```text
app.py starts the Flask app.
It registers the route files.
It does not do all work alone.
```

Em português:

O `app.py` é o ponto de entrada do sistema. Ele inicia o Flask e registra as rotas separadas.

---

## routes/dashboard_routes.py

Responsável por:

```text
dashboard page
API /api/invoices
invoice detail page
```

Em inglês A2:

```text
Dashboard routes show the main app.
The API sends invoice data to JavaScript.
The detail page shows one invoice.
```

---

## routes/upload_routes.py

Responsável por:

```text
upload page
TXT upload
image upload
OCR processing
file validation
success/error messages
```

Em inglês A2:

```text
Upload routes receive files.
TXT files are processed directly.
Image files go through OCR.
Wrong files show an error message.
```

---

## routes/report_routes.py

Responsável por:

```text
BI Reports page
generate reports
download CSV
download JSON
download monthly summary
download yearly summary
download risk summary
```

Em inglês A2:

```text
Report routes export business data.
The user can download CSV and JSON reports.
```

---

## routes/architecture_routes.py

Responsável por:

```text
project architecture page
system status
data flow
project structure explanation
```

Essa página ajuda muito para portfólio e entrevista.

---

## Services

## services/database.py

Cria e conecta com o banco SQLite.

```text
SQLite stores invoice data.
The database file is data/invoices.db.
```

---

## services/invoice_repository.py

Lê e salva invoices no SQLite.

Responsável por:

```text
load all invoices
find one invoice
save invoice
```

Em inglês A2:

```text
The repository reads database data.
The repository saves invoice data.
```

---

## services/invoice_processor.py

Processa uma invoice depois que o texto já existe.

Fluxo:

```text
invoice text
↓
extract fields
↓
validate invoice
↓
create invoice data
↓
save into SQLite
```

---

## services/extractor.py

Extrai campos do texto da invoice.

Campos principais:

```text
invoice_number
supplier_name
invoice_date
due_date
total_amount
currency
vat_number
```

Em inglês A2:

```text
The extractor gets fields from text.
It finds invoice number, supplier, date, amount, and VAT number.
```

---

## services/validator.py

Aplica regras de negócio e calcula risco.

Regras atuais:

```text
Missing field -> +15 risk points
Due date overdue -> +30 risk points
High total amount above 5000 -> +25 risk points

Risk 0 -> approved
Risk 1 to 49 -> needs_review
Risk 50 to 100 -> high_risk
```

---

## services/ocr_reader.py

Lê texto de arquivos.

Hoje:

```text
TXT file -> reads text directly
Image file -> uses OCR
PDF file -> prepared for future OCR
```

Em inglês A2:

```text
OCR reads text from images.
The app uses pytesseract and Pillow.
```

---

## services/text_cleaner.py

Limpa textos vindos do OCR.

Exemplos:

```text
2026-3-26 -> 2026-03-26
1E... -> IE...
extra blank lines -> removed
```

Isso melhora a qualidade do texto antes da extração dos campos.

---

## services/exporter.py

Gera relatórios a partir do SQLite.

Arquivos possíveis:

```text
invoices_YEAR_MONTH.csv
invoices_YEAR_MONTH.json
monthly_summary_YEAR_MONTH.csv
yearly_summary_YEAR_MONTH.csv
risk_summary_YEAR_MONTH.csv
```

Em inglês A2:

```text
The exporter creates business reports.
Reports can be CSV or JSON.
```

---

## SQLite Database

O banco principal é:

```text
data/invoices.db
```

Tabela principal:

```text
invoices
```

Campos importantes:

```text
invoice_number
supplier_name
invoice_date
due_date
total_amount
currency
vat_number
status
risk_score
reasons
source_file
source_type
```

---

## source_type

O campo `source_type` mostra a origem da invoice.

Valores atuais:

```text
txt
ocr_image
```

Explicação:

```text
txt -> invoice came from a text file
ocr_image -> invoice came from an image processed by OCR
```

Em português:

Esse campo é importante porque mostra rastreabilidade. A empresa consegue saber se a invoice veio de um arquivo de texto ou de uma imagem lida por OCR.

---

## SQL Query For Checking Data

Consulta útil no Beekeeper Studio:

```sql
SELECT
    invoice_number,
    invoice_date,
    total_amount,
    status,
    risk_score,
    source_type,
    source_file
FROM invoices
ORDER BY invoice_date, invoice_number;
```

O que esse comando faz:

```text
SELECT chooses the columns.
FROM chooses the table.
ORDER BY sorts the result.
```

---

## Dashboard

O dashboard mostra:

```text
Total Invoices
Approved
Needs Review
High Risk
Average Risk
Total Amount
Needs Review %
Business Recommendation
Yearly Recommendation
Charts
Risk Alerts
Top Risk Invoices
Invoice Details Table
```

---

## Average Risk

`Average Risk` não é dinheiro e não é porcentagem.

Ele é a média dos pontos de risco das invoices.

Exemplo:

```text
Invoice 1 risk = 30
Invoice 2 risk = 0
Invoice 3 risk = 25

Average Risk = average of all risk scores
```

Em inglês A2:

```text
Average Risk is not money.
Average Risk is not percent.
It is the average risk score.
```

---

## Dashboard Charts

O dashboard usa Chart.js.

Gráficos atuais:

```text
Status Counts
Risk Score By Invoice
Yearly Invoice Amount
Yearly Average Risk
```

Aprendizado:

```text
Charts use data from the API.
The API reads from SQLite.
JavaScript updates charts when filters change.
```

---

## BI Reports Page

Página:

```text
/reports
```

Essa página permite:

```text
filter by year
filter by month
generate reports
download CSV
download JSON
download summaries
```

Relatórios:

```text
Full Invoice CSV
Full Invoice JSON
Monthly Summary
Yearly Summary
Risk Summary
```

---

## Upload Page

Página:

```text
/upload
```

Fluxo TXT:

```text
User uploads TXT
↓
Flask reads text
↓
Extractor gets fields
↓
Validator checks risk
↓
SQLite saves invoice
↓
Dashboard updates
```

Fluxo Image OCR:

```text
User uploads JPG/PNG
↓
Flask saves image
↓
OCR reads text
↓
Text cleaner fixes OCR text
↓
Extractor gets fields
↓
Validator checks risk
↓
SQLite saves invoice
↓
Dashboard updates
```

PDF:

```text
PDF OCR is pending.
The project is prepared for future PDF OCR.
```

---

## Architecture Page

Página:

```text
/architecture
```

Essa página explica:

```text
system status
data flow
project structure
interview explanation
```

Ela é importante porque mostra que o projeto não é só visual. Ele tem arquitetura, fluxo de dados e separação de responsabilidades.

---

## Important Commands

Start Flask app:

```powershell
python app.py
```

Open dashboard:

```text
http://127.0.0.1:5000/
```

Open BI Reports:

```text
http://127.0.0.1:5000/reports
```

Open Upload:

```text
http://127.0.0.1:5000/upload
```

Open Architecture:

```text
http://127.0.0.1:5000/architecture
```

---

## Old Learning Commands

Esses comandos foram importantes no começo do projeto, mas agora são parte da fase antiga de aprendizado:

```powershell
python invoice_analyzer.py
python invoice_data_analysis.py
python -m services.database_importer
```

Hoje o fluxo principal é:

```powershell
python app.py
```

---

## CSV vs SQLite

Aprendizado importante:

```text
CSV is good for learning.
SQLite is good for a small app.
PostgreSQL is good for real companies.
Data warehouse is good for big BI.
Parquet is good for big data files.
```

No projeto atual:

```text
SQLite is the main database.
CSV and JSON are export reports.
```

---

## File Cleanup Strategy

Não apagar arquivos direto no começo.

Estratégia segura:

```text
Do not delete first.
Move old files to archive.
Test the app.
Delete later if everything works.
```

Pastas de limpeza:

```text
archive/old_reports/
archive/old_upload_tests/
archive/legacy_learning_files/
```

---

## What This Project Shows To Companies

Este projeto mostra conhecimento em:

```text
Python
Flask
SQLite
OCR
Pandas-style reporting
JavaScript
Chart.js
HTML
CSS
Business automation
Data validation
BI reports
API
Dashboard
Project architecture
```

Áreas relacionadas:

```text
Automation Developer
Junior Python Developer
Data Analyst
BI Analyst
RPA Developer
IT Trainee
AI/ML Junior path
Operations Automation
```

---

## Portfolio Explanation

Frase curta em inglês:

```text
I built an AI-powered document automation system using Python, Flask, SQLite, OCR, and JavaScript. The system processes invoices, extracts business data, validates risks, stores results in a database, and generates dashboards and BI reports.
```

Versão A2:

```text
I built a document automation app.
It reads invoices.
It extracts data.
It checks risk.
It saves data in SQLite.
It shows charts and reports.
```

---

## Interview Explanation

```text
This project started as a simple Python invoice analyzer. Then I improved it step by step with CSV reports, Pandas-style analysis, Flask, SQLite, OCR, Chart.js, upload pages, BI reports, and architecture documentation.

I used AI to accelerate development, but I understand the flow, the files, the database, the routes, the services, and how the system works.
```

---

## AI-Native Professional Explanation

```text
I used AI to accelerate the project, but I understand the workflow.
I know how the files connect.
I know how to test the app.
I know how to explain the architecture.
I can change and improve the system.
```

---

## Current Project Status

```text
MVP professional version: almost complete
Dashboard: done
SQLite: done
TXT upload: done
Image OCR: done
BI reports: done
Architecture page: done
source_type tracking: done
PDF OCR: future improvement
ML classification: future improvement
Login/authentication: future improvement
Docker: future improvement
```

---

## Future Improvements

Next possible improvements:

```text
PDF OCR
Document classification with Machine Learning
Login system
User roles
Docker
PostgreSQL
Cloud deployment
Automated tests
Better API documentation
Dashboard pagination
Search invoices
Edit invoice status
Delete invoice
Audit log
```

---

## Final Learning Summary

Em inglês A2:

```text
One function has one job.
Services store reusable logic.
Routes control web pages.
SQLite stores data.
OCR reads image text.
JavaScript updates the dashboard.
Charts show business results.
Reports help business decisions.
```

Em português:

Este projeto me ajudou a entender como conectar automação, dados, banco de dados, OCR, backend, frontend, API, dashboard e relatórios em um sistema real.