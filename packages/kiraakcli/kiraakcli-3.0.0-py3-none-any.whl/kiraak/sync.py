from datetime import datetime
import logging
import math
from sqlite3 import Date
import time
from typing import Generator
import os
import json
# import open


from rich import print_json
from woocommerce import API

from kiraak import console
from kiraak.api import get_catalog, login
from kiraak.catalog import Catalog
from kiraak.config import Auth
from kiraak import wc_api

logger = logging.getLogger(__name__)

class WC_Product:
    def __init__(self, raw_json) -> None:
        self.id = raw_json["id"]
        self.name = raw_json["name"]
        self.status = raw_json["status"]
        self.old_status = raw_json["status"]
        self.description = raw_json["description"]
        self.sku = raw_json["sku"]
        self.price = None
        if raw_json["price"]:
            self.price = int(raw_json["price"])
            self.old_price = int(raw_json["price"])
        else:
            logger.error(f"Product {self.name!r} has no price!")
        self.old_name = raw_json["name"]

class WC_Products:
    def __init__(self, raw_json: dict) -> None:
        self.prods = list(filter(lambda x: x.price, [WC_Product(x) for x in raw_json]))

    def update_prods(self, catalog: Catalog):
        for prod in self.prods:
            if cprod := catalog.find_by_id(prod.sku):
                prod.status = "publish"
                prod.price = int(cprod.price)
                prod.name = f"{cprod.name} {cprod.desc} {cprod.quantity}" 
            else:
                prod.status = "draft"

    def find_by_sku(self, sku):
        return next((x for x in self.prods if x.sku == sku), None)

    @property
    def updated_prods(self) -> Generator[WC_Product, None, None]:
        return iter(filter(lambda x: x.old_price != x.price or x.status != x.old_status, self.prods))

    def __iter__(self) -> Generator[WC_Product, None, None]:
        return iter(self.prods)


def sync():
    # Get and print catalog
    logger.info("Fetching catalog...")
    catalog = Catalog(get_catalog())
    logger.info(f"Recieved catalog (id {catalog.id}) with {len(catalog.products)} products")

    catalog.print_table(console)

    logger.info("Fetching existing WooCommerce Products...")
    prods = []
    i = 1
    while new_prods := wc_api.get("products", json={"page": i, "per_page": 100}).json():
        logger.info(f"Fetching page {i}")
        i += 1
        try:
            if new_prods["data"]["status"] != 200:
                logger.error(new_prods["message"])
        except (KeyError, TypeError):
            pass
        prods.extend(new_prods)

    logger.info(f"Received {len(prods)} existing WooCommerce Products")
    woocommerce_products = WC_Products(prods)
    woocommerce_products.update_prods(catalog)
    for prod in catalog:
        if not woocommerce_products.find_by_sku(prod.product_id):
            logger.warning(f"Product not found in WooCommerce: {prod.name} {prod.desc} {prod.quantity} ({prod.product_id})")
    
    num_prods_status_changed = 0
    num_prods_price_changed = 0
    num_prods_name_changed = 0
    prods_to_update = []
    for x in woocommerce_products:
        prods_to_update.append(
            {
                "id": x.id,
                "status": x.status,
                "regular_price": x.price,
                "name": x.name,
            }
        )
        if (x.status != x.old_status):
            num_prods_status_changed +=1
        if (x.price != x.old_price):
            num_prods_price_changed +=1 
        if (x.name != x.old_name):
            num_prods_name_changed += 1        
    logger.info(f"Syncing {len(prods_to_update)} products...")
    logger.info(f"changed status of {num_prods_status_changed} products in Woo Commerce")
    logger.info(f"changed price of {num_prods_price_changed} products in Woo Commerce")
    logger.info(f"changed name of {num_prods_name_changed} products in Woo Commerce")

    for i in range(math.ceil(len(prods_to_update)/100)):
        logger.info(f"Syncing batch {i + 1}")
        data = {
            "update": prods_to_update[i*100: (i + 1)*100]
        }
        for prod in woocommerce_products.updated_prods:
            logger.info(
                f"Updating [bold]{prod.name}[/] ({prod.old_status!r} -> {prod.status!r}) (₹{prod.old_price!r} -> ₹{prod.price!r})",
                extra={"markup": True}
            )
        returned = wc_api.post("products/batch", data=data).json()
    logger.info("Synced!")

def main(once, time_gap):
    logger.info(f"Logging in as {Auth.MOBILE}")
    partner_info = login(Auth.MOBILE, Auth.PASSWORD)
    logger.info(
        f"Logged in as {partner_info['partnerName']} @ {partner_info['partnerBrand']}"
    )

    sync()
    while not once:
        time.sleep(time_gap)
        sync()
    
    
if __name__ == "__main__":
    main()
