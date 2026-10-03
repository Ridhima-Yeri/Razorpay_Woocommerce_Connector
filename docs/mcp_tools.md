# MCP Tool Specification

This connector exposes WooCommerce functionality as agent-friendly tools.

## Authentication

The connector authenticates with WooCommerce using a WooCommerce REST API
consumer key and consumer secret.

Credentials are loaded from environment variables and are never included
in tool responses.

## Tool 1: list_products

### Purpose
List products available in the WooCommerce store.

### Input

- `page`: integer, default 1
- `per_page`: integer, default 20, maximum 100

### Endpoint

GET `/products`

### Example

```json
{
  "page": 1,
  "per_page": 20
}