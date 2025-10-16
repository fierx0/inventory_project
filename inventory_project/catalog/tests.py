from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from catalog.models import Category, Supplier, Product, Stock, Movement


class InventoryApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass1234")
        self.client = APIClient()
        self.category = Category.objects.create(name="Cables")
        self.supplier = Supplier.objects.create(name="Acme Ltd")
        self.product = Product.objects.create(
            sku="USB-001", name="USB Cable 1m", category=self.category, default_supplier=self.supplier
        )
        # ensure stock exists (signal should create it)
        Stock.objects.get_or_create(product=self.product)

    def auth(self):
        self.client.force_authenticate(user=self.user)

    def test_public_product_list(self):
        resp = self.client.get("/api/catalog/products/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(resp.data, list) or "results" in resp.data)

    def test_write_requires_auth(self):
        resp = self.client.post("/api/catalog/categories/", {"name": "Adapters"}, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.auth()
        resp2 = self.client.post("/api/catalog/categories/", {"name": "Adapters"}, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)

    def test_receive_and_issue_updates_stock(self):
        self.auth()
        # Receive 10
        r1 = self.client.post("/api/inventory/receive/", {"product": self.product.id, "quantity": 10})
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock.on_hand, 10)
        # Issue 4
        r2 = self.client.post("/api/inventory/issue/", {"product": self.product.id, "quantity": 4})
        self.assertEqual(r2.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock.on_hand, 6)

    def test_issue_more_than_available_is_blocked(self):
        self.auth()
        # stock currently 0
        r = self.client.post("/api/inventory/issue/", {"product": self.product.id, "quantity": 1})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient stock", str(r.data))
