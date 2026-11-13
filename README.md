# Intelligent Communication Management System

A Python + Streamlit application that classifies incoming institutional emails/requests, estimates priority, routes requests to departments, suggests template responses, tracks status in SQLite, and exports operational reports.

## Features
- Add requests manually or import a CSV file.
- Automatic category classification:
  - Event-related
  - Alumni communication
  - General enquiry
  - Media and publicity
  - Technical support
- Rule-based priority detection: Low, Medium, High.
- Department routing based on category.
- Predefined editable response suggestions.
- SQLite request tracking with Pending, In Progress and Resolved statuses.
- Dashboard KPIs and CSV reports.

## Tech stack
Python, Streamlit, SQLite, Pandas.

## Setup (Windows)
1. Extract the ZIP folder.
2. Open the extracted folder in VS Code.
3. Open the terminal in this folder.
4. Create and activate a virtual environment:

```bash
python -m venv venv
venv\\Scripts\\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the app:

```bash
streamlit run app.py
```

The application opens in your browser. The SQLite database `communication_requests.db` is created automatically on first run.

## CSV format
The CSV must include `subject` and `message`. Optional columns: `sender`, `email`.

Example:

```csv
sender,email,subject,message
Aarav,aarav@example.com,Workshop registration,Please share the workshop registration link
Meera,meera@example.com,Portal login issue,The student portal is not working urgently
```

A sample file is available at `data/sample_requests.csv`.

## How classification works
The initial version uses a transparent keyword-based classifier. Keywords are stored in `src/classifier.py` and can be customised for the organisation. Priority is estimated using urgency terms. Review suggestions before sending; the application does not send emails automatically.

## Project structure

```text
Intelligent_Communication_Management_System/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_requests.csv
└── src/
    ├── __init__.py
    ├── classifier.py
    ├── database.py
    └── reporting.py
```

## Important note
This is a functional academic prototype. Classification and priority are rule-based, not a trained machine-learning model. For production use, connect an authorised email API, add authentication and audit logs, and validate routing rules with the organisation.
