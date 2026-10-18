# Beneficiary Manager

A small Django web app for registering and managing beneficiaries of a community programme, with the data-quality checks that programme teams need: validated IDs and phone numbers, duplicate detection, bulk CSV import with a per-row error report, and Excel export.

I built it as a portfolio project based on the kind of work I did as a Data & Information Officer, where keeping a beneficiary database accurate, complete and free of duplicates was a daily task. All data in this repo is fictional.

## Features

- **Registry**: add, edit, search (name / ID / phone) and filter by status.
- **Validation**: ID numbers must be 9 digits; phone numbers must be valid Palestinian mobile formats (`05XXXXXXXX`, `+9705XXXXXXXX`).
- **Duplicate detection**: flags records that share a phone number, or the same name in the same district (case and spacing ignored).
- **CSV import**: valid rows are saved, invalid rows are listed with their CSV line number and the reason, and IDs that already exist are skipped instead of duplicated.
- **Excel export**: one click to `.xlsx`.
- **Dashboard**: households registered, people reached, breakdown by status and district, number of possible duplicate groups.
- **Django admin** with search and filters.

## Tech

Python 3.12+, Django 5.2, SQLite, openpyxl. 14 automated tests.

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (source .venv/bin/activate on Linux/macOS)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Open http://127.0.0.1:8000/ and try **Import CSV** with `sample_data.csv`. It contains fictional records, one duplicate phone number and one row with an invalid ID, so you can see the error report and the duplicates page working.

## Tests

```bash
python manage.py test
```

They cover the validators, duplicate detection, CSV import (good rows, bad rows, existing IDs, invalid status), the views, and the Excel export.

## Project layout

```
config/            Django project settings and root URLs
registry/
  models.py        Beneficiary model
  validators.py    ID and phone validation
  services.py      duplicate detection, CSV import, Excel export
  views.py         dashboard, list, edit, duplicates, import, export
  templates/       HTML templates
  tests.py         test suite
sample_data.csv    fictional demo data
```

## Possible next steps

Login and per-user permissions, an audit log of edits, Arabic interface, deployment with PostgreSQL.
