from rest_framework import serializers
from .models import Category, Supplier, Product, Movement


# -----------------------------
# Category Serializer
# -----------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


# -----------------------------
# Supplier Serializer
# -----------------------------
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


# -----------------------------
# Product Serializer
# -----------------------------
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    supplier_name = serializers.ReadOnlyField(source="default_supplier.name")
    stock_on_hand = serializers.ReadOnlyField(source="stock.on_hand")  # show current stock

    class Meta:
        model = Product
        fields = [
            "id", "sku", "name", "category", "category_name",
            "unit", "default_supplier", "supplier_name",
            "is_active", "stock_on_hand",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "stock_on_hand"]


# -----------------------------
# Movement Serializer
# -----------------------------
class MovementSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    user = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Movement
        fields = [
            "id",
            "product",
            "product_name",
            "movement_type",
            "quantity",
            "reason",
            "user",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]
