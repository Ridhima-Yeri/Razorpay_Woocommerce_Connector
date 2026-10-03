# Agent Capabilities and Limitations

## What the Agent Can Do

The WooCommerce connector allows an Agent Studio agent to:

1. List products.
2. Retrieve a product by ID.
3. Search products by text.
4. List orders.
5. Retrieve an order by ID.
6. Search orders.
7. Retrieve inventory information for a product.

The connector is primarily designed for read-only agent workflows.

## Example Agent Tasks

An agent can answer questions such as:

- "Show me the available products."
- "Find products containing the word shirt."
- "What is the stock level of product 15?"
- "Show me recent orders."
- "Find orders matching a particular search term."
- "What is the status of order 1001?"

## What the Agent Cannot Do

The current connector does not provide operations to:

- Create products
- Update products
- Delete products
- Create orders
- Modify orders
- Cancel orders
- Refund orders
- Modify inventory
- Modify customer information
- Modify store settings

These restrictions intentionally keep the connector read-oriented.

## Data Access

The connector only accesses data available through the configured
WooCommerce REST API credentials.

The agent cannot access information outside the permissions granted to
the configured WooCommerce API key.

## Authentication

WooCommerce REST API credentials are loaded from environment variables.

Credentials must not be committed to source control.

## Rate Limiting

HTTP 429 responses are handled using retry logic.

The connector respects the `Retry-After` response header when available
and retries a limited number of times.

## Production Considerations

For production deployment, the connector should additionally use:

- Secure secret management
- HTTPS
- Centralized logging
- Monitoring and alerting
- Request tracing
- Configurable retry policies
- More granular permission scopes
- Production-grade deployment infrastructure