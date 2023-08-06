import logging
import sys
import typing as t

from kiraak.catalog import Catalog, Product
from kiraak.order import Order

logger = logging.getLogger(__name__)


class Mapping:
    def __init__(self, order: Order, catalog: Catalog) -> None:
        self.map: t.Dict[str, Product] = {}
        self.order = order
        self.catalog = catalog

    def initialize_mapping(self) -> None:
        for oproduct in self.order.prods:
            if not oproduct.mapping:
                oproduct.mapping = self.catalog.find_by_id(oproduct.sku)
        if not all([x.mapping for x in self.order.prods]):
            logger.error(
                f"Products {','.join([x.name for x in self.order.prods if not x.mapping])} not found in catalog, skipping products!"
            )
        if not all(
            [x.mapping.price == x.price for x in self.order.prods if x.mapping]
        ):
            logger.error(
                f"Products {','.join([x.name for x in self.order.prods if x.mapping.price != x.price])} do not have matching prices!"
            )
            sys.exit(1)
