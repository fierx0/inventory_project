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


POST http://127.0.0.1:8000/api/users/register/

Body → raw → JSON

{
  "username": "hunter",
  "email": "hunter1@gmail.com",
  "password": "Hunter@01"
}
POST http://127.0.0.1:8000/api/auth/token/
POST http://127.0.0.1:8000/api/catalog/products/
Body → JSON:
{
  "sku": "USB-002",
  "name": "USB Cable 2m",
  "category": 2,
  "unit": "pcs",
  "default_supplier": 1,
  "is_active": true
}

POST http://127.0.0.1:8000/api/inventory/receive/

{
  "product": 1,
  "quantity": 15,
  "reason": "Restocking warehouse"
}