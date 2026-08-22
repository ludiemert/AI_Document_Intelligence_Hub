# AI Document Intelligence Hub

AI Document Intelligence Hub is a business automation project built with Python, Flask, SQLite, OCR, JavaScript, and Chart.js.

The system processes invoice documents, extracts business data, validates invoice rules, calculates risk scores, stores results in SQLite, and shows insights in a web dashboard.

---

## Project Goal

The goal of this project is to simulate a real business document automation system.

The app helps a finance or operations team:

- Upload invoice documents
- Extract invoice fields
- Validate required information
- Detect business risks
- Save invoice history in SQLite
- Show dashboard metrics
- Generate BI reports
- Process image invoices using OCR

---

## Current Project Flow

```text
User uploads invoice
↓
Flask receives the file
↓
OCR/Text reader reads the document
↓
Python extracts invoice fields
↓
Python validates business rules
↓
Python calculates risk score
↓
SQLite stores invoice data
↓
Dashboard shows charts, alerts, and tables
↓
BI Reports exports CSV and JSON files
```

---

## Main Technologies

```text
Python
Flask
SQLite
Pandas
JavaScript
Chart.js
HTML
CSS
Tesseract OCR
pytesseract
Pillow
```

---

## Main Features

```text
TXT invoice upload
Image invoice OCR upload
Invoice field extraction
Invoice validation
Risk score calculation
SQLite database storage
Dashboard with filters
Dynamic charts with Chart.js
Risk alerts
Top risk invoices
Invoice detail page
BI Reports page
CSV and JSON export
Architecture explanation page
Source type tracking: txt or ocr_image
```

---

## Risk Rules

```text
Missing field -> +15 risk points
High total amount above 5000 -> +25 risk points
Overdue due date -> +30 risk points

Risk 0 -> approved
Risk 1 to 49 -> needs_review
Risk 50 to 100 -> high_risk
```

---

## Project Structure

```text
AI_Document_Intelligence_Hub/
├── app.py
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
├── frontend/
│   ├── index.html
│   ├── upload.html
│   ├── reports.html
│   ├── architecture.html
│   ├── invoice_detail.html
│   ├── app.js
│   └── styles.css
├── data/
│   └── invoices.db
├── uploads/
├── reports/
├── archive/
└── README.md
```

---

## What Each Main Part Does

```text
app.py
Starts the Flask app and registers routes.

routes/
Controls web pages and API routes.

services/
Stores reusable business logic.

frontend/
Stores HTML, CSS, and JavaScript files.

data/
Stores the SQLite database.

uploads/
Stores uploaded documents and OCR text files.

reports/
Stores exported CSV and JSON reports.

archive/
Stores old learning files, test reports, and old project outputs.
```

---

## SQLite Database

The project uses SQLite as the application database.

The main table is:

```text
invoices
```

Important columns:

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

`source_type` shows where the invoice came from:

```text
txt -> text upload
ocr_image -> image processed by OCR
```

---

## Dashboard

The dashboard shows:

```text
Total invoices
Approved invoices
Needs review invoices
High risk invoices
Average risk score
Total invoice amount
Needs review percentage
Business recommendations
Risk alerts
Top risk invoices
Invoice details table
```

The dashboard also has filters by:

```text
Year
Month
```

---

## BI Reports

The BI Reports page exports business reports from SQLite.

Available exports:

```text
Full invoice CSV
Full invoice JSON
Monthly summary
Yearly summary
Risk summary
```

Reports can be filtered by:

```text
Year
Month
```

---

## OCR Layer

The OCR layer prepares the project for real document automation.

Current OCR flow:

```text
Image invoice
↓
pytesseract reads text
↓
text_cleaner.py cleans OCR text
↓
extractor.py extracts invoice fields
↓
validator.py checks risk
↓
SQLite stores the result
```

Example:

```text
invoice_014.jpg
↓
invoice_014_ocr.txt
↓
SQLite record with source_type = ocr_image
```

---

## Architecture Page

The project includes an architecture page explaining:

```text
System status
Data flow
Project structure
Interview explanation
```

This helps explain the project clearly in interviews.

---

## Learning Notes

Important concepts learned during this project:

```text
One function has one job.
main app starts Flask.
Routes control web pages.
Services store reusable logic.
SQLite stores real app data.
CSV is good for reports.
JSON is good for web/API data.
OCR converts images into text.
The source changes, but the processing logic stays the same.
```

A2 English explanation:

```text
The app reads invoices.
The app extracts data.
The app checks risk.
The app saves data in SQLite.
The dashboard shows business results.
OCR helps the app read image invoices.
```

---

## Portfolio Description

```text
Built an AI-powered document automation system using Python, Flask, SQLite, OCR, JavaScript and Chart.js to process invoice documents, extract business data, detect risks, store records, generate reports, and display business insights in a dashboard.
```

Short A2 version:

```text
I built a document automation app.
It reads invoice files.
It extracts data and checks risk.
It saves invoices in SQLite.
It shows charts and reports in a dashboard.
```

---

## How To Run

```powershell
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000/
```

---

## Main Pages

```text
Dashboard
http://127.0.0.1:5000/

Upload Invoice
http://127.0.0.1:5000/upload

BI Reports
http://127.0.0.1:5000/reports

Architecture
http://127.0.0.1:5000/architecture
```

---

## Project Status

```text
MVP portfolio version: almost complete
TXT upload: done
Image OCR upload: done
SQLite: done
Dashboard: done
BI Reports: done
Architecture page: done
PDF OCR: pending
Authentication/login: future
Docker: future
Machine Learning classification: future
```

---

## Future Improvements

```text
Add PDF OCR
Add document classification with Machine Learning
Add authentication/login
Add Docker
Add automated tests
Deploy online
Use PostgreSQL for production
Add user roles
Add audit logs
```