# AI Document Intelligence Hub

Projeto de IA + automação + dados para processar documentos empresariais, começando por invoices.

Este projeto está sendo construído passo a passo para aprender como um sistema real pode evoluir de arquivos simples para uma aplicação web com banco de dados, dashboard, análise de risco e futuramente OCR e Machine Learning.

---

## Objetivo Do Projeto

Criar um sistema que lê documentos empresariais, extrai dados importantes, valida informações, calcula risco, salva os resultados e mostra tudo em um dashboard web.

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

---

## Fluxo Atual Do Projeto

Hoje o projeto já evoluiu para um fluxo mais profissional:

```text
Upload .txt
↓
Flask receives the file
↓
Python reads invoice text
↓
Python extracts invoice fields
↓
Python validates invoice data
↓
Python calculates risk score
↓
Python saves data into SQLite
↓
Flask API sends data to frontend
↓
Dashboard updates automatically
```

Em inglês A2:

```text
The user uploads an invoice.
Flask receives the file.
Python processes the invoice.
SQLite saves the data.
The dashboard shows the result.
```

---

## Fases Do Projeto

### Fase 1: Python + TXT

Começamos com invoices em formato `.txt`.

O objetivo era entender a lógica principal:

```text
Raw invoice text
↓
Extract fields
↓
Validate data
↓
Create risk score
↓
Show result
```

### Fase 2: CSV + Pandas

Depois salvamos os resultados em CSV.

O CSV ajudou no aprendizado de:

```text
Data export
Excel reports
Pandas analysis
Business metrics
```

Fluxo da fase:

```text
.txt invoices
↓
invoice_analyzer.py
↓
reports/invoice_results.csv
↓
invoice_data_analysis.py
↓
Pandas reports
```

### Fase 3: JSON + Dashboard

Depois criamos JSON para conectar os dados com o frontend.

O JSON ajudou a preparar o projeto para web/API:

```text
CSV / Pandas
↓
JSON files
↓
JavaScript reads data
↓
Dashboard shows metrics and charts
```

### Fase 4: Flask API

Depois criamos Flask para transformar o projeto em uma aplicação web real.

Fluxo:

```text
Flask backend
↓
API route
↓
Frontend dashboard
```

Rotas importantes:

```text
/              -> dashboard
/api/invoices  -> invoice data as JSON
/invoice/<id>  -> invoice detail page
/upload        -> upload invoice page
```

### Fase 5: SQLite

Depois adicionamos SQLite como banco de dados.

Agora o dashboard não depende mais diretamente dos CSVs.

Fluxo atual:

```text
SQLite database
↓
Flask API
↓
JavaScript frontend
↓
Dashboard
```

Em inglês A2:

```text
SQLite is the main database.
The dashboard reads data from SQLite.
CSV files are now reports.
```

### Fase 6: Upload Pelo Sistema Web

Agora começamos a fazer upload de invoices pela própria aplicação.

Fluxo:

```text
Upload .txt
↓
Flask saves file
↓
Python processes invoice
↓
SQLite stores invoice
↓
Dashboard updates
```

---

## Estrutura De Pastas

```text
AI_Document_Intelligence_Hub/
├── app.py
├── data/
│   └── invoices.db
├── frontend/
│   ├── index.html
│   ├── invoice_detail.html
│   ├── upload.html
│   ├── styles.css
│   ├── app.js
│   └── favicon.svg
├── reports/
│   ├── invoice_results.csv
│   ├── invoice_results.json
│   ├── invoice_summary.csv
│   ├── invoice_summary.json
│   ├── business_recommendations.json
│   ├── invoice_monthly_summary.csv
│   └── invoice_monthly_status_summary.csv
├── sample_documents/
├── services/
└── uploads/
```

---

## Papel De Cada Pasta

### `sample_documents/`

Pasta usada no começo do projeto para guardar invoices de exemplo.

```text
sample_documents = old learning/test files
```

### `uploads/`

Pasta usada pelo sistema web.

Quando o usuário faz upload de uma invoice, o arquivo deve ser salvo aqui.

```text
uploads = files sent by the web app
```

No futuro, ela pode ficar organizada assim:

```text
uploads/
└── 2027/
    └── 02/
        └── invoice_006.txt
```

### `reports/`

Pasta de relatórios e exportações.

Guarda arquivos CSV, JSON e imagens de gráficos.

```text
reports = exported reports
```

### `data/`

Pasta do banco SQLite.

```text
data/invoices.db = main database
```

---

## CSV, JSON, SQLite E Dashboard

### CSV

CSV foi usado para aprender exportação, Pandas e relatórios.

Hoje o CSV continua útil para:

```text
Excel reports
Pandas analysis
BI exports
Simple backup
Business documentation
```

Mas o CSV não é mais a fonte principal do dashboard.

### JSON

JSON foi usado para conectar dados com frontend.

Hoje o JSON ainda pode ser útil para:

```text
APIs
Frontend data
Reports
External systems
```

### SQLite

SQLite é agora a fonte principal dos dados do dashboard.

```text
SQLite = system memory
CSV = exported report
JSON = web/API format
Dashboard = visual interface
```

### Dashboard

O dashboard lê os dados pela API Flask.

```text
SQLite
↓
Flask API
↓
JavaScript
↓
Dashboard
```

---

## Arquivos Python Principais

### `app.py`

Controla a aplicação Flask.

Responsabilidades:

```text
show dashboard
show upload page
receive uploaded invoice
return API data
show invoice detail page
```

Em inglês A2:

```text
app.py controls the web app.
It receives browser requests.
It sends pages and data.
```

### `invoice_analyzer.py`

Foi o primeiro controlador do projeto.

Responsabilidades:

```text
read .txt invoices
extract fields
validate invoices
create CSV report
```

Hoje ele continua importante para aprendizado e testes, mas o fluxo profissional está indo para Flask + SQLite.

### `invoice_data_analysis.py`

Analisa dados com Pandas e gera relatórios.

Responsabilidades:

```text
read invoice results
calculate metrics
create monthly summary
create yearly summary
create recommendations
create charts
export reports
```

### `services/database.py`

Cria conexão com SQLite e cria a tabela `invoices`.

```text
database.py manages the database structure.
```

### `services/database_importer.py`

Importa dados antigos de JSON/CSV para SQLite.

Foi importante na transição:

```text
old reports
↓
SQLite database
```

### `services/invoice_repository.py`

Busca dados no SQLite para o Flask.

Responsabilidades:

```text
load all invoices
find one invoice by invoice number
```

### `services/invoice_processor.py`

Processa uma invoice enviada pelo upload.

Responsabilidades:

```text
receive invoice text
extract fields
validate invoice
save invoice into SQLite
```

### `services/extractor.py`

Extrai informações do texto da invoice.

Exemplos de campos:

```text
invoice_number
supplier_name
invoice_date
due_date
total_amount
currency
vat_number
```

### `services/validator.py`

Aplica regras de negócio e risco.

Responsabilidades:

```text
check missing fields
check overdue date
check high amount
calculate risk score
define status
```

---

## Regras De Risco

```text
Missing field -> +15 risk points for each missing field
High total amount above 5000 -> +25 risk points
Due date overdue -> +30 risk points

Risk 0 -> approved
Risk 1 to 49 -> needs_review
Risk 50 to 100 -> high_risk
```

Em inglês A2:

```text
Risk score shows invoice risk.
A low score is good.
A high score needs review.
```

---

## Status Da Invoice

```text
approved
needs_review
high_risk
```

Significado:

```text
approved -> invoice is OK
needs_review -> finance team should check it
high_risk -> invoice has serious risk
```

---

## Dashboard Atual

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
Status Counts chart
Risk Score by Invoice chart
Yearly Invoice Amount chart
Yearly Average Risk chart
Risk Alerts
Top Risk Invoices
Invoice Details table
```

Também existe uma página de detalhe:

```text
/invoice/<invoice_number>
```

Exemplo:

```text
/invoice/INV-2026-001
```

---

## Conceitos Aprendidos

```text
Python functions
Flask routes
HTML pages
CSS styling
JavaScript DOM
Chart.js charts
CSV files
JSON files
Pandas analysis
SQLite database
SQL queries
Upload forms
Business rules
Risk score
Dashboard metrics
Project structure
Services architecture
```

---

## Conceitos De Mercado

Este projeto toca áreas como:

```text
Data Analyst
Automation Developer
Junior Python Developer
Business Intelligence
AI/ML Future
RPA / Operations Automation
Backend with Flask
Data Automation
```

Frase para portfólio:

```text
Built an intelligent document automation system that processes invoices, detects missing fields and risks, stores results in SQLite, and provides a Flask dashboard with business metrics, charts, alerts, and invoice detail pages.
```

Versão A2:

```text
I built a document automation app.
The app reads invoices.
It extracts data.
It checks risks.
It saves data in SQLite.
It shows a business dashboard.
```

---

## Próximos Passos

```text
1. Improve upload validation
2. Save uploaded files by year and month
3. Show success/error messages after upload
4. Add export reports from SQLite
5. Add PDF/image upload
6. Add OCR
7. Add document classification with Machine Learning
8. Add authentication/login
9. Add Docker
10. Prepare GitHub README and portfolio explanation
```

---

## Ideia Importante

O projeto começou simples de propósito.

```text
Simple first.
Professional later.
```

Primeiro aprendemos a lógica com TXT e CSV.

Depois evoluímos para Flask, API, SQLite e dashboard.

Isso é parecido com o mundo real: projetos crescem por fases.

Em inglês A2:

```text
The project grows step by step.
Each step teaches one new concept.
The system is becoming more professional.
```


mais informacoes

Isso conecta bem com mercado:
SQL
Data export
Automation
Business reports
BI

____________________________________________

1. Clique Export Reports
2. Veja mensagem verde
3. Clique Download CSV
4. Veja se o navegador baixa o arquivo
5. Clique Download JSON
6. Veja se o navegador baixa o arquivo

_____________________________

/                       -> dashboard principal
/upload                 -> upload invoice
/invoice/<number>       -> detalhe da invoice
/reports                -> página BI Reports
/export                 -> gera todos os relatórios
/download/csv           -> baixa invoice export completo
/download/json          -> baixa invoice JSON completo
/download/monthly       -> baixa monthly summary
/download/yearly        -> baixa yearly summary
/download/risk          -> baixa risk summary

________________________________

BI Reports page
↓
User chooses Year / Month
↓
Click Generate Report
↓
Flask receives year/month
↓
SQLite filters invoices
↓
CSV/JSON are generated only with selected data

_____________________________________________

Fechamos esta fase:
Dashboard
↓
BI Reports page
↓
Year/Month filters
↓
Generate filtered reports
↓
Download detailed CSV/JSON
↓
Download monthly/yearly/risk summaries
Agora vamos para a próxima grande etapa:
PDF/image upload + OCR preparation

_____________________________________

Agora vamos preparar o sistema para aceitar:
.txt
.pdf
.png
.jpg
.jpeg
Mas no primeiro passo, não vamos fazer OCR ainda. Vamos só:
1. Permitir upload desses formatos
2. Identificar o tipo do arquivo
3. Se for .txt, processa como já faz hoje
4. Se for PDF/image, salva na pasta correta
5. Mostra mensagem: OCR will be added in the next step

_____________________________________________

Upload file
↓
Detect file type
↓
TXT -> read text directly
PDF/Image -> future OCR
↓
Process extracted text
↓
SQLite
↓
Dashboard

_______________________________________________________

C:\Users\user\Downloads\AI_Document_Intelligence_Hub\app.py

Se o usuário tentar subir .exe, .docx, .zip etc.
↓
Flask bloqueia
↓
Mostra mensagem vermelha
↓
Não salva o arquivo
↓
Não processa no SQLite

Arquivo errado
↓
fica em /upload
↓
mostra mensagem vermelha ali mesmo
↓
não volta para dashboard
____________________________

Para PDF/imagem isso vai dar erro, porque PDF/imagem não é texto puro.
Então agora vamos ensinar o sistema:
Se for .txt:
    lê texto
    extrai campos
    valida
    salva no SQLite

Se for .pdf / .png / .jpg / .jpeg:
    salva em uploads/pending_ocr
    mostra mensagem:
    "File uploaded successfully. OCR processing will be added next."

    _______________________
TXT correto
↓
processa
↓
salva no SQLite

TXT com campo faltando
↓
não processa
↓
não salva
↓
mostra erro na tela upload

PDF/image
↓
não processa ainda
↓
vai para pending OCR

________________________

.txt é texto puro. O Python consegue fazer:
invoice_text = uploaded_file.read().decode("utf-8")
Mas um .pdf, .png, .jpg é arquivo binário/visual. Antes de validar campos, precisamos transformar imagem/PDF em texto:
PDF/image
↓
OCR
↓
text
↓
extract fields
↓
validate fields

__________________
OCR significa:
Optical Character Recognition
Em português:
Reconhecimento Óptico de Caracteres
Ou seja: OCR é a tecnologia que transforma imagem/PDF visual em texto.
______________________________

uma imagem é só pixels:
photo_invoice.jpg
Python não vê texto ali diretamente. Ele vê imagem. O OCR faz esta ponte:
pixels -> text
Ferramentas OCR Comuns
No nosso projeto, opções gratuitas:
Tesseract OCR
pytesseract
OpenCV
pdf2image
Pillow

O papel de cada uma:
Tesseract = motor que reconhece letras
pytesseract = Python conversa com Tesseract
OpenCV = limpa/melhora imagem antes do OCR
pdf2image = transforma PDF em imagem
Pillow = abre/manipula imagens
No Mercado De TI
Isso é muito usado em empresas para:
invoices
contracts
receipts
delivery notes
bank documents
HR forms
compliance documents

Frase para explicar em entrevista:
I added an OCR layer to convert PDF and image documents into text before extraction, validation, risk scoring, and database storage.
Em inglês A2:
OCR reads text from images.
The app uses OCR before extracting invoice fields.
After OCR, the app can validate and save the invoice.
__________________________________

arquitetura pronta:
upload
↓
ocr_reader.py
↓
text
↓
extractor.py
↓
validator.py
↓
SQLite

_____________________________
app.py = controla as rotas Flask
ocr_reader.py = lê texto dos arquivos
extractor.py = extrai campos
validator.py = valida regras
database = salva dados

_______________________________

OCR com Tesseract tem 2 partes:
1. Programa Tesseract instalado no Windows
2. Biblioteca Python pytesseract instalada no ambiente

pip show pytesseract
OR
pip install pytesseract pillow

next step
tesseract --version
pip show pytesseract
pip show pillow
__________________________________

teste => python -m services.ocr_reader

_________________
comando SQL beekeeper Studio para ver a linha da coluna
SELECT
    invoice_number,
    supplier_name,
    invoice_date,
    due_date,
    total_amount,
    currency,
    vat_number,
    status,
    risk_score,
    source_file
FROM invoices
WHERE invoice_number = 'INV-2026-014';
________________
alterar a tabela

ALTER TABLE invoices
ADD COLUMN source_type TEXT DEFAULT 'txt';

This adds a new column.
The column saves the invoice source type.
Old invoices receive txt as default.
Passo 2: conferir se criou
Depois rode:
SELECT
    invoice_number,
    source_file,
    source_type
FROM invoices
ORDER BY invoice_number;

___________________________________________

alterar arquivo SQL table
UPDATE invoices
SET source_type = 'ocr_image'
WHERE invoice_number = 'INV-2026-014';
____________________________
check
SELECT
    invoice_number,
    source_file,
    source_type
FROM invoices
WHERE invoice_number = 'INV-2026-014';
___________________________

como estar para ver os invoices

testar em 3 lugares.
1. Beekeeper / SQLite
Rode:
SELECT
    invoice_number,
    invoice_date,
    total_amount,
    status,
    risk_score,
    source_file,
    source_type
FROM invoices
WHERE invoice_number = 'INV-2027-015';
Resultado esperado se foi imagem/OCR:
source_type = ocr_image
E o source_file deve estar parecido com:
uploads\2027\...\invoice_015_ocr.txt
2. Pasta uploads
Veja se foi criado um arquivo .txt do OCR dentro da pasta do ano/mês:
C:\Users\user\Downloads\AI_Document_Intelligence_Hub\uploads\2027\...\invoice_015_ocr.txt
Esse arquivo é importante porque mostra:
image -> OCR text -> saved text file
3. Página de detalhe
Clique na invoice INV-2027-015, se ela aparecer na tabela ou gráfico. A página detalhe deve abrir. Por enquanto talvez ainda não mostre source_type, porque esse é nosso próximo passo visual.

__________________________________
if -> first option
elif -> second option
elif -> third option
else -> safety option
________________________
arquitetura será separar rotas:
app.py -> starts Flask
dashboard_routes.py -> dashboard, API, invoice detail
upload_routes.py -> upload, TXT, image OCR
report_routes.py -> BI reports, export, downloads
services/ -> business logic
SQLite -> data storage

app.py starts the app.
Routes control pages.
Services do the work.
Database saves data.
_________________________________________
O __init__.py pode ficar vazio. Ele só diz para o Python:
routes is a Python package.
______________________
O Que É Blueprint
Pensa assim:
Blueprint = folder/group of routes
Ou em inglês A2:
A blueprint is a group of routes.
Flask app uses the blueprint.

___________________

app.py starts Flask.
dashboard_routes.py controls dashboard routes.
register_blueprint connects app.py with dashboard_routes.py.
We remove old routes from app.py to avoid duplicate routes.

____________________

o arquivo report_routes.py vai cuidar de:
/reports
/export
/download/csv
/download/json
/download/monthly
/download/yearly
/download/risk

_______________________________________
A página Architecture mostraria o caminho que os dados fazem.
Exemplo:
User uploads invoice
↓
Flask receives file
↓
OCR/Text reader extracts text
↓
Extractor finds fields
↓
Validator checks risk
↓
SQLite saves invoice
↓
Dashboard shows charts
↓
BI Reports exports CSV/JSON

__________________
This is my system flow.
The upload route receives documents.
The OCR service reads images.
The extractor gets invoice fields.
The validator calculates risk.
SQLite stores the data.
The dashboard reads the API.
_________________________________

Project Structure
app.py -> starts Flask
routes/ -> controls pages
services/ -> business logic
data/invoices.db -> database
frontend/ -> web interface
uploads/ -> uploaded files
reports/ -> exported files
O Que Você Aprende Com Isso
Você aprende a explicar:
Architecture
Data flow
Backend responsibility
Frontend responsibility
Database role
OCR pipeline
Em inglês A2:
This page explains how the app works.
The user uploads a document.
Python reads and validates the invoice.
SQLite saves the data.
The dashboard shows results.
Não é só “enfeite”. É documentação visual dentro do sistema. Para portfólio, isso fica muito profissional.

_______________________________________________

@dashboard_bp.route("/architecture")
Cria o endereço:
http://127.0.0.1:5000/architecture
def architecture_page():
Cria a função que controla essa página.
return render_template("architecture.html")
Manda o Flask abrir o arquivo:
frontend/architecture.html
Em inglês A2:
This route opens the architecture page.
The page explains the system flow.


___________________________
System Status -> mostra o que funciona
Data Flow -> mostra o caminho dos dados
Project Structure -> mostra as pastas/arquivos
Interview Explanation -> frase para entrevista
_____________________________
