from django.contrib import admin
from .models import Category, Supplier, Product, Stock, Movement


@admin.display(description="Stock", ordering="stock__on_hand")
def stock_on_hand(obj: Product):
    try:
        return obj.stock.on_hand
    except Stock.DoesNotExist:
        return 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25
    readonly_fields = ("created_at", "updated_at")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "contact_email", "phone", "created_at", "updated_at")
    search_fields = ("name", "contact_email", "phone")
    ordering = ("name",)
    list_per_page = 25
    readonly_fields = ("created_at", "updated_at")


class StockInline(admin.StackedInline):
    model = Stock
    extra = 0
    can_delete = False
    fields = ("on_hand",)
    verbose_name_plural = "Stock (on hand)"


class MovementInline(admin.TabularInline):
    model = Movement
    extra = 0
    can_delete = False
    fields = ("movement_type", "quantity", "reason", "created_by", "created_at")
    readonly_fields = ("movement_type", "quantity", "reason", "created_by", "created_at")
    ordering = ("-created_at",)
    verbose_name_plural = "Recent movements"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "sku", "name", "category", "default_supplier", "unit",
        "is_active", stock_on_hand, "created_at", "updated_at",
    )
    list_filter = ("is_active", "category", ("created_at", admin.DateFieldListFilter))
    search_fields = ("sku", "name")
    autocomplete_fields = ("category", "default_supplier")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
    list_select_related = ("category", "default_supplier")
    list_per_page = 25
    inlines = [StockInline, MovementInline]

    actions = ["mark_active", "mark_inactive"]

    @admin.action(description="Mark selected products as Active")
    def mark_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} product(s) marked as Active.")

    @admin.action(description="Mark selected products as Inactive")
    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} product(s) marked as Inactive.")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "on_hand")
    search_fields = ("product__name", "product__sku")
    autocomplete_fields = ("product",)
    ordering = ("product__name",)
    list_per_page = 25


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ("id", "movement_type", "product", "quantity", "reason", "created_by", "created_at")
    list_filter = ("movement_type", ("created_at", admin.DateFieldListFilter))
    search_fields = ("product__name", "product__sku", "reason", "created_by__username")
    autocomplete_fields = ("product", "created_by")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25
