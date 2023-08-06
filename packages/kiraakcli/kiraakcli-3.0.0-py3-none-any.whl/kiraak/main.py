"""Processing of json file and adding orders"""
from datetime import datetime
import json
import logging
from pathlib import Path

from kiraak import console, wc_api
from kiraak.add_orders import add_order
from kiraak.api import get_catalog, login
from kiraak.catalog import Catalog
from kiraak.config import Auth
from kiraak.order import Order

logger = logging.getLogger(__name__)

PENDING = "pending"
PROCESSED = "processed"

def fetch_catalog(console):
    # Get and print catalog
    logger.info("Fetching catalog...")
    catalog = Catalog(get_catalog())
    logger.info(f"Recieved catalog (id {catalog.id})")
    catalog.print_table(console)
    return catalog


def add_order_from_file(file: Path, catalog) -> None:
    """Process files, adds orders"""

    # Process json file
    logger.info(f"Processing {file}")
    with open(file, "r") as file_obj:
        current_order = Order(json.load(file_obj))

    logger.info(f"Adding order {current_order} ")
    add_order(current_order, catalog)
    if current_order.added:
        logger.info(f"Added order for customer {current_order.name} !")
        file.rename(file.parent.parent / PROCESSED / file.name)

# Function to get all orders from Woocommerce:
def main():
    # Login
    logger.info(f"Logging in as {Auth.MOBILE}")
    partner_info = login(Auth.MOBILE, Auth.PASSWORD)
    logger.info(
        f"Logged in as {partner_info['partnerName']} @ {partner_info['partnerBrand']}"
    )

    current_month = datetime.today().strftime('%B')
    month_dir = Path(current_month)
    month_dir.mkdir(exist_ok=True)
    current_month_pending = month_dir / PENDING
    current_month_pending.mkdir(exist_ok=True)
    current_month_processed = month_dir / PROCESSED
    current_month_processed.mkdir(exist_ok=True)

    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    logger.info(f"Getting WC orders after {now.strftime('%c')}")
    orders = wc_api.get("orders", json={
        "after": now.isoformat(),
        "per_page": 100
    }).json()
    logger.info(f"Received {len(orders)} orders")

    processed_order_ids = [int(x.name.rstrip(".json")) for x in current_month_processed.glob("*")]
    for order in orders:
        if order['id'] in processed_order_ids:
            continue
        filename = current_month_pending / f"{order['id']}.json"
        logger.info(f"Creating file {filename} for order")

        with open(filename,'w') as order_file:
            json.dump(order, order_file)        

    catalog = fetch_catalog(console)    

    for file in current_month_pending.glob("*"):
        add_order_from_file(file.absolute(),catalog)
