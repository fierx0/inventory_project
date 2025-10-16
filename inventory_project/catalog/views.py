from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Supplier, Product, Movement
from .serializers import CategorySerializer, SupplierSerializer, ProductSerializer, MovementSerializer
from .permissions import ReadOnlyOrAuthenticatedWrite
from .utils import apply_stock_movement


# --------- CRUD ViewSets ---------

class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyOrAuthenticatedWrite]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.all().order_by("name")
    serializer_class = SupplierSerializer
    search_fields = ["name", "contact_email", "phone"]


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.select_related("category", "default_supplier").all().order_by("name")
    serializer_class = ProductSerializer
    search_fields = ["name", "sku"]


# --------- Inventory Endpoints ---------

def _parse_qty(q):
    try:
        qty = int(q)
        return qty
    except Exception:
        raise ValueError("Quantity must be an integer")

def _not_found(msg="Not found"):
    return Response({"detail": msg}, status=status.HTTP_404_NOT_FOUND)

def _bad_request(msg):
    return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def receive_stock(request):
    product_id = request.data.get("product")
    qty_raw = request.data.get("quantity")
    reason = request.data.get("reason", "")

    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        return _not_found("Product does not exist")

    try:
        qty = _parse_qty(qty_raw)
        stock = apply_stock_movement(product, "RECEIVE", qty)
        movement = Movement.objects.create(
            product=product, movement_type="RECEIVE",
            quantity=qty, reason=reason, created_by=request.user
        )
        data = MovementSerializer(movement).data
        data["new_stock"] = stock.on_hand
        return Response(data, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return _bad_request(str(e))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def issue_stock(request):
    product_id = request.data.get("product")
    qty_raw = request.data.get("quantity")
    reason = request.data.get("reason", "")

    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        return _not_found("Product does not exist")

    try:
        qty = _parse_qty(qty_raw)
        stock = apply_stock_movement(product, "ISSUE", qty)
        movement = Movement.objects.create(
            product=product, movement_type="ISSUE",
            quantity=qty, reason=reason, created_by=request.user
        )
        data = MovementSerializer(movement).data
        data["new_stock"] = stock.on_hand
        return Response(data, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return _bad_request(str(e))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def adjust_stock(request):
    product_id = request.data.get("product")
    qty_raw = request.data.get("quantity")  # may be negative
    reason = request.data.get("reason", "")

    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        return _not_found("Product does not exist")

    try:
        qty = _parse_qty(qty_raw)
        stock = apply_stock_movement(product, "ADJUST", qty)
        movement = Movement.objects.create(
            product=product, movement_type="ADJUST",
            quantity=abs(qty), reason=reason, created_by=request.user
        )
        data = MovementSerializer(movement).data
        data["new_stock"] = stock.on_hand
        return Response(data, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return _bad_request(str(e))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def low_stock_report(request):
    from .models import Stock
    threshold = request.query_params.get("threshold", "5")
    try:
        th = int(threshold)
    except Exception:
        return _bad_request("threshold must be an integer")
    low = (Stock.objects
           .filter(on_hand__lt=th)
           .select_related("product")
           .order_by("product__name"))
    data = [
        {"product": s.product.name, "sku": s.product.sku, "on_hand": s.on_hand}
        for s in low
    ]
    return Response({"threshold": th, "results": data})
