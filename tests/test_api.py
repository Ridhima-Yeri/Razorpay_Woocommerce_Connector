from fastapi.testclient import TestClient

from app.main import app, woo_client


client = TestClient(app)


# ============================================================
# MOCK DATA
# ============================================================

MOCK_PRODUCT = {
    "id": 15,
    "name": "Classic Cotton T-Shirt",
    "price": "799",
    "stock_quantity": 25,
    "stock_status": "instock",
}


MOCK_ORDER = {
    "id": 1001,
    "status": "processing",
    "total": "799.00",
    "currency": "INR",
    "date_created": "2026-10-03T12:00:00",
}


MOCK_INVENTORY = {
    "product_id": 15,
    "name": "Classic Cotton T-Shirt",
    "stock_quantity": 25,
    "stock_status": "instock",
}


# ============================================================
# HEALTH TEST
# ============================================================

def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "woocommerce-agent-connector"


# ============================================================
# PRODUCT TESTS
# ============================================================

def test_products_endpoint(monkeypatch):

    def mock_list_products(page=1, per_page=20):
        return [MOCK_PRODUCT]

    monkeypatch.setattr(
        woo_client,
        "list_products",
        mock_list_products,
    )

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["id"] == 15
    assert data[0]["name"] == "Classic Cotton T-Shirt"


def test_get_product(monkeypatch):

    def mock_get_product(product_id):
        return MOCK_PRODUCT

    monkeypatch.setattr(
        woo_client,
        "get_product",
        mock_get_product,
    )

    response = client.get("/products/15")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 15
    assert data["name"] == "Classic Cotton T-Shirt"


def test_product_search(monkeypatch):

    def mock_search_products(
        query,
        page=1,
        per_page=20,
    ):
        return [MOCK_PRODUCT]

    monkeypatch.setattr(
        woo_client,
        "search_products",
        mock_search_products,
    )

    response = client.get(
        "/products/search",
        params={"q": "shirt"},
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["name"] == "Classic Cotton T-Shirt"


# ============================================================
# ORDER TESTS
# ============================================================

def test_orders_endpoint(monkeypatch):

    def mock_list_orders(
        page=1,
        per_page=20,
        status=None,
    ):
        return [MOCK_ORDER]

    monkeypatch.setattr(
        woo_client,
        "list_orders",
        mock_list_orders,
    )

    response = client.get("/orders")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["id"] == 1001


def test_get_order(monkeypatch):

    def mock_get_order(order_id):
        return MOCK_ORDER

    monkeypatch.setattr(
        woo_client,
        "get_order",
        mock_get_order,
    )

    response = client.get("/orders/1001")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1001
    assert data["status"] == "processing"


def test_order_search(monkeypatch):

    def mock_search_orders(
        search,
        page=1,
        per_page=20,
    ):
        return [MOCK_ORDER]

    monkeypatch.setattr(
        woo_client,
        "search_orders",
        mock_search_orders,
    )

    response = client.get(
        "/orders/search",
        params={"q": "1001"},
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# ============================================================
# INVENTORY TEST
# ============================================================

def test_inventory_endpoint(monkeypatch):

    def mock_get_inventory(product_id):
        return MOCK_INVENTORY

    monkeypatch.setattr(
        woo_client,
        "get_inventory",
        mock_get_inventory,
    )

    response = client.get("/inventory/15")

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 15
    assert data["stock_quantity"] == 25
    assert data["stock_status"] == "instock"