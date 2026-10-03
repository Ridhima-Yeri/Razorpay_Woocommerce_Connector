# WooCommerce Agent Connector

A private WooCommerce connector designed to expose read-oriented WooCommerce capabilities to an Agent Studio agent.

## Features

The connector provides APIs for:

* Listing products
* Getting a product by ID
* Searching products
* Listing orders
* Getting an order by ID
* Searching orders
* Getting product inventory
* Health checking
* Rate-limit handling and retries

## Project Structure

```text
razorpay_Woocommerce_Connector/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── woo_client.py
│   └── config.py
│
├── docs/
│   ├── mcp_tools.md
│   └── agent_capabilities.md
│
├── tests/
│   └── test_api.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── pytest.ini
```

## Requirements

* Python 3.11+
* WooCommerce store with REST API access
* WooCommerce REST API consumer key
* WooCommerce REST API consumer secret

## Installation

Create and activate a virtual environment:

```bash
python -m venv myenv
```

Windows:

```cmd
myenv\Scripts\activate
```

Install dependencies:

```cmd
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```text
WOOCOMMERCE_URL=http://localhost:8881
WOOCOMMERCE_CONSUMER_KEY=your_consumer_key
WOOCOMMERCE_CONSUMER_SECRET=your_consumer_secret
```

Do not commit `.env` or any credentials to source control.

## Running the Connector

Start the FastAPI application:

```cmd
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Available Endpoints

### Health

```text
GET /health
```

### Products

```text
GET /products
GET /products/{product_id}
GET /products/search
```

### Orders

```text
GET /orders
GET /orders/{order_id}
GET /orders/search
```

### Inventory

```text
GET /inventory/{product_id}
```

## Running Tests

Run:

```cmd
pytest -v
```

The test suite uses mocked WooCommerce responses for API-layer testing, so the tests do not require live WooCommerce data.

## Authentication

The connector authenticates with WooCommerce using the configured REST API consumer key and consumer secret.

Credentials are loaded from environment variables and are not returned by the connector.

## Rate Limiting

The connector handles HTTP 429 responses.

When a rate limit response is received, the connector:

1. Checks the `Retry-After` header.
2. Waits for the specified duration when available.
3. Uses exponential backoff when the header is unavailable.
4. Retries up to three times.

## Limitations

The current implementation is read-oriented.

It does not support:

* Creating products
* Updating products
* Deleting products
* Creating orders
* Updating orders
* Cancelling orders
* Refunds
* Inventory modification
* Customer modification
* Store configuration changes

The connector also assumes that the configured WooCommerce credentials have permission to access the requested resources.

## Production Considerations

For production deployment, the connector should use:

* HTTPS
* Secure secret management
* Monitoring and logging
* Request tracing
* Production-grade deployment
* More granular permission management
* Configurable retry policies

## Assignment Scope

This implementation uses publicly accessible WooCommerce REST API functionality and does not bypass access controls or access private data outside the configured merchant account.

## Local environment note: 
The connector is configured to authenticate against WooCommerce using environment-provided REST API credentials. In my local WooCommerce environment, authenticated REST requests currently return HTTP 401 despite valid credentials; the connector's authentication and error-handling logic is implemented accordingly.
