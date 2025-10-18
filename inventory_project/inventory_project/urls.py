from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from catalog.views import CategoryViewSet, SupplierViewSet, ProductViewSet
from catalog import views as catalog_views

# NEW: import models for counts
from catalog.models import Product, Category, Supplier, Movement
# NEW: import version (optional)
try:
    from inventory_project import __version__
except Exception:
    __version__ = "0.1.0"

router = DefaultRouter()
router.register(r'catalog/categories', CategoryViewSet, basename='category')
router.register(r'catalog/suppliers', SupplierViewSet, basename='supplier')
router.register(r'catalog/products', ProductViewSet, basename='product')

def home(_request):
    products = Product.objects.count()
    categories = Category.objects.count()
    suppliers = Supplier.objects.count()
    movements = Movement.objects.count()

    return HttpResponse(f"""
        <html>
            <head>
                <title>Inventory Management API</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background:#f9f9f9; color:#333; }}
                    h1 {{ color:#2c3e50; }}
                    .container {{ max-width: 880px; margin:auto; background:white; padding:30px; border-radius:12px;
                                  box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                    .stat-grid {{ display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; margin: 18px 0 10px; }}
                    .card {{ background:#fafafa; border-radius:10px; padding:16px; text-align:center; border:1px solid #eee; }}
                    .num {{ font-size: 28px; font-weight: 700; }}
                    a {{ color:#007BFF; text-decoration:none; font-weight:600; }}
                    a:hover {{ text-decoration:underline; }}
                    .links a {{ display:inline-block; margin:6px 10px 0 0; }}
                    .muted {{ color:#666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome to the Inventory Management API</h1>
                    <p class="muted">Version {__version__}</p>

                    <div class="stat-grid">
                        <div class="card">
                            <div class="num">{products}</div>
                            <div>Products</div>
                        </div>
                        <div class="card">
                            <div class="num">{categories}</div>
                            <div>Categories</div>
                        </div>
                        <div class="card">
                            <div class="num">{suppliers}</div>
                            <div>Suppliers</div>
                        </div>
                        <div class="card">
                            <div class="num">{movements}</div>
                            <div>Movements</div>
                        </div>
                    </div>

                    <div class="links">
                        <a href="/api/">API Root</a>
                        <a href="/api/docs/">Swagger Docs</a>
                        <a href="/api/redoc/">ReDoc</a>
                        <a href="/admin/">Admin Panel</a>
                        <a href="/api/health/">Health</a>
                    </div>

                    <p class="muted" style="margin-top:16px;">
                        Built with Django REST Framework — Capstone Project by Abdellah Idmhand
                    </p>
                </div>
            </body>
        </html>
    """)

def health(_request):
    return HttpResponse("ok")

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/token/", obtain_auth_token),
    path("api/users/", include("accounts.urls")),
    path("api/inventory/receive/", catalog_views.receive_stock),
    path("api/inventory/issue/", catalog_views.issue_stock),
    path("api/inventory/adjust/", catalog_views.adjust_stock),
    path("api/inventory/reorder/low-stock/", catalog_views.low_stock_report),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/health/", health),
]
