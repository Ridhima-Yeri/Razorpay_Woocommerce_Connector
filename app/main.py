from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.woo_client import WooCommerceClient


app = FastAPI(
    title="WooCommerce Agent Connector",
    description=(
        "Private connector for an Agent Studio agent to access "
        "WooCommerce products, orders and inventory."
    ),
    version="1.0.0",
)


woo_client = WooCommerceClient()


# ============================================================
# RESPONSE MODELS
# ============================================================

class HealthResponse(BaseModel):
    status: str = Field(
        examples=["ok"]
    )
    service: str = Field(
        examples=["woocommerce-agent-connector"]
    )


class Product(BaseModel):
    id: int = Field(
        examples=[15]
    )
    name: str = Field(
        examples=["Classic Cotton T-Shirt"]
    )
    price: str | None = Field(
        default=None,
        examples=["799"]
    )
    stock_quantity: int | None = Field(
        default=None,
        examples=[25]
    )
    stock_status: str | None = Field(
        default=None,
        examples=["instock"]
    )


class Order(BaseModel):
    id: int = Field(
        examples=[1001]
    )
    status: str | None = Field(
        default=None,
        examples=["processing"]
    )
    total: str | None = Field(
        default=None,
        examples=["799.00"]
    )
    currency: str | None = Field(
        default=None,
        examples=["INR"]
    )
    date_created: str | None = Field(
        default=None,
        examples=["2026-10-03T12:00:00"]
    )


class Inventory(BaseModel):
    product_id: int = Field(
        examples=[15]
    )
    name: str = Field(
        examples=["Classic Cotton T-Shirt"]
    )
    stock_quantity: int | None = Field(
        default=None,
        examples=[25]
    )
    stock_status: str | None = Field(
        default=None,
        examples=["instock"]
    )


# ============================================================
# HEALTH
# ============================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
)
def health():
    return {
        "status": "ok",
        "service": "woocommerce-agent-connector",
    }


# ============================================================
# PRODUCT ENDPOINTS
# ============================================================

@app.get(
    "/products",
    response_model=list[Product],
    summary="List products",
)
def list_products(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    per_page: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of products per page",
    ),
):
    try:
        return woo_client.list_products(
            page=page,
            per_page=per_page,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"WooCommerce request failed: {exc}",
        )


# IMPORTANT:
# /products/search MUST appear BEFORE /products/{product_id}

@app.get(
    "/products/search",
    response_model=list[Product],
    summary="Search products",
)
def search_products(
    q: str = Query(
        ...,
        min_length=1,
        description="Product search text",
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    per_page: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):
    try:
        return woo_client.search_products(
            query=q,
            page=page,
            per_page=per_page,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"WooCommerce request failed: {exc}",
        )


@app.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Get product",
)
def get_product(product_id: int):
    try:
        return woo_client.get_product(product_id)

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"WooCommerce request failed: {exc}",
        )


# ============================================================
# ORDER ENDPOINTS
# ============================================================

@app.get(
    "/orders",
    response_model=list[Order],
    summary="List orders",
)
def list_orders(
    page: int = Query(
        default=1,
        ge=1,
    ),
    per_page: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    status: str | None = Query(
        default=None,
        description="Optional WooCommerce order status",
    ),
):
    try:
        return woo_client.list_orders(
            page=page,
            per_page=per_page,
            status=status,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"WooCommerce request failed: {exc}",
        )


# IMPORTANT:
# /orders/search MUST appear BEFORE /orders/{order_id}

@app.get(
    "/orders/search",
    response_model=list[Order],
    summary="Search orders",
)
def search_orders(
    q: str = Query(
        ...,
        min_length=1,
        description="Order search text",
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    per_page: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):
    try:
        return woo_client.search_orders(
            search=q,
            page=page,
            per_page=per_page,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"WooCommerce request failed: {exc}",
        )


@app.get(
    "/orders/{order_id}",
    response_model=Order,
    summary="Get order",
)
def get_order(order_id: int):
    try:
        return woo_client.get_order(order_id)

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"WooCommerce request failed: {exc}",
        )


# ============================================================
# INVENTORY
# ============================================================

@app.get(
    "/inventory/{product_id}",
    response_model=Inventory,
    summary="Get product inventory",
)
def get_inventory(product_id: int):
    try:
        return woo_client.get_inventory(product_id)

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"WooCommerce request failed: {exc}",
        )