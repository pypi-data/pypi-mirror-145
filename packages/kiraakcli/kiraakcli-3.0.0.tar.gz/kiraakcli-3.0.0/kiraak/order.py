import re
from typing import Generator

from kiraak.catalog import Product
from kiraak.config import FLAT_RE


class ParseFlatError(Exception):
    pass


class OrderProduct:
    def __init__(self, raw) -> None:
        self.sku = raw["sku"]
        # self.line_id = raw["line_id"]
        self.name = raw["name"]
        self.qty = float(raw["quantity"])
        self.price = float(raw["price"])
        self.mapping: Product | None = None
        self.total = self.qty*self.price

    def __str__(self) -> str:
        return self.name


class Order:
    def __init__(self, raw) -> None:
        self.order_num = raw["id"]
        self.status = raw["status"]
        self.date = raw["date_created"]
        self.note = raw["customer_note"]
        self.name = f'{raw["billing"]["first_name"]} {raw["billing"]["last_name"]}'
        self.flat = raw["billing"]["address_1"]
        res = re.match(FLAT_RE, raw["billing"]["address_1"])
        if not res:
            raise ParseFlatError(
                f"Could not parse flat from address {raw['billing_address']}"
            )
        self.flat = f'{res.group("block")}-{res.group("flat")}'
        self.phone = raw["billing"]["phone"]
        self.prods: list[OrderProduct] = [OrderProduct(x) for x in raw["line_items"]]
        self.total = sum([x.total for x in self.prods])
        self.added = False

    def __str__(self) -> str:
        return self.name

    def __iter__(self) -> Generator[OrderProduct, None, None]:
        yield from self.prods
