import os

from dotenv import load_dotenv

load_dotenv()


WOOCOMMERCE_URL = os.getenv("WOOCOMMERCE_URL")
WOOCOMMERCE_CONSUMER_KEY = os.getenv("WOOCOMMERCE_CONSUMER_KEY")
WOOCOMMERCE_CONSUMER_SECRET = os.getenv("WOOCOMMERCE_CONSUMER_SECRET")


if not WOOCOMMERCE_URL:
    raise ValueError("WOOCOMMERCE_URL is not configured")

if not WOOCOMMERCE_CONSUMER_KEY:
    raise ValueError("WOOCOMMERCE_CONSUMER_KEY is not configured")

if not WOOCOMMERCE_CONSUMER_SECRET:
    raise ValueError("WOOCOMMERCE_CONSUMER_SECRET is not configured")

print("WooCommerce URL:", WOOCOMMERCE_URL)
print("Consumer Key loaded:", bool(WOOCOMMERCE_CONSUMER_KEY))
print("Consumer Secret loaded:", bool(WOOCOMMERCE_CONSUMER_SECRET))