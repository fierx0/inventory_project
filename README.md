# Simple Inventory Management API (Single Location)

Django REST API to manage **Categories**, **Suppliers**, **Products**, and **Inventory Movements** (Receive/Issue/Adjust) with a **Low-Stock** report.

## Live (local)
- Homepage: `http://127.0.0.1:8000/`
- API Root: `http://127.0.0.1:8000/api/`
- Swagger: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`

## Features
- CRUD: categories, suppliers, products
- Token auth (public GETs, writes require auth)
- Stock tracking with movements
- Prevent negative stock on issue
- Low-stock report (`threshold` query param)
- Swagger/OpenAPI docs
- Clean Django admin with inlines and stock column

## Quickstart
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
