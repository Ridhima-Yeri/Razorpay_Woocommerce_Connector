import time 
import httpx

from app.config import (
    WOOCOMMERCE_URL,
    WOOCOMMERCE_CONSUMER_KEY,
    WOOCOMMERCE_CONSUMER_SECRET,
)


class WooCommerceClient:
    def __init__(self):
        self.base_url = (
            f"{WOOCOMMERCE_URL.rstrip('/')}/wp-json/wc/v3"
        )

        self.client = httpx.Client(
            timeout=20.0
        )

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        max_retries = 3

        for attempt in range(max_retries):
            params = kwargs.pop("params", {}).copy()

            try:
                response = self.client.request(
                    method,
                    url,
                    params=params,
                    auth=(
                        WOOCOMMERCE_CONSUMER_KEY,
                        WOOCOMMERCE_CONSUMER_SECRET,
                    ),
                    **kwargs,
                )
            except httpx.HTTPError as exc:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"WooCommerce request failed: {exc}") from exc

            if response.status_code == 401:
                raise RuntimeError(
                    "WooCommerce authentication failed. "
                    "Check WOOCOMMERCE_URL, WOOCOMMERCE_CONSUMER_KEY, and "
                    "WOOCOMMERCE_CONSUMER_SECRET in your .env file. "
                    "Also ensure the request is not sending the keys in the URL."
                )

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait_seconds = float(retry_after)
                    except ValueError:
                        wait_seconds = 2
                else:
                    wait_seconds = 2 ** attempt

                if attempt < max_retries - 1:
                    time.sleep(wait_seconds)
                    continue

            response.raise_for_status()
            return response.json()

        raise RuntimeError(
            "WooCommerce request failed after maximum retries."
        )

    #Products detail
    def list_products(
        self,
        page: int = 1,
        per_page: int = 20,
    ):
        return self._request(
            "GET",
            "products",
            params={
                "page": page,
                "per_page": per_page,
            },
        )

    def get_product(self, product_id: int):
        return self._request(
            "GET",
            f"products/{product_id}",
        )

    def search_products(
        self,
        query: str,
        page: int = 1,
        per_page: int = 20,
    ):
        return self._request(
            "GET",
            "products",
            params={
                "search": query,
                "page": page,
                "per_page": per_page,
            },
        )

    #Order details
    def list_orders(
        self,
        page: int = 1,
        per_page: int = 20,
        status: str | None = None,
    ):
        params = {
            "page": page,
            "per_page": per_page,
        }

        if status:
            params["status"] = status

        return self._request(
            "GET",
            "orders",
            params=params,
        )

    def get_order(self, order_id: int):
        return self._request(
            "GET",
            f"orders/{order_id}",
        )

    def search_orders(
        self,
        search: str,
        page: int = 1,
        per_page: int = 20,
    ):
        return self._request(
            "GET",
            "orders",
            params={
                "search": search,
                "page": page,
                "per_page": per_page,
            },
        )

    def get_inventory(self, product_id: int):
        product = self.get_product(product_id)

        return {
            "product_id": product.get("id"),
            "name": product.get("name"),
            "stock_quantity": product.get("stock_quantity"),
            "stock_status": product.get("stock_status"),
        }