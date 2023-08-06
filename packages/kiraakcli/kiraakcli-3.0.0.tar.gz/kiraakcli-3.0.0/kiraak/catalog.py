from typing import Generator
from rich.table import Table


class Product:
    def __init__(self, raw) -> None:
        self.id = raw["_id"]
        self.product_id = raw["productId"]["_id"]
        self.name = raw["productId"]["productName"]
        self.desc = raw["productId"]["productDescription"]
        self.price = float(raw["productPrice"])
        self.quantity = raw["productBaseQuantity"]
        self.stock = raw["productAvailability"] == "instock"
        self.__repr__ = self.__str__

    def __str__(self) -> str:
        return f"{self.name} {self.desc} {self.quantity}"


class Catalog:
    """Represents the entire catalog"""

    def __init__(self, raw: dict) -> None:
        self.id = raw["_id"]
        self.products = [Product(x) for x in raw["productList"]]

    def find_by_id(self, id) -> Product:
        try:
            return next(filter(lambda x: x.product_id == id, self.products))
        except:
            return None

    def print_table(self, console) -> None:
        tbl = Table(
            "Product ID",
            "Product Name",
            "Description",
            "Price",
            "Base quantity",
            "In Stock?",
        )
        for product in self:
            tbl.add_row(
                product.product_id,
                product.name,
                product.desc,
                f"₹ {product.price}",
                product.quantity,
                str(product.stock),
            )
        console.print(tbl)

    def __iter__(self) -> Generator[Product, None, None]:
        yield from self.products

    def __len__(self) -> int:
        return len(self.products)
