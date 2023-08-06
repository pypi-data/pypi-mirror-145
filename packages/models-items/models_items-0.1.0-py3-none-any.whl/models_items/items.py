from dataclasses import dataclass
from decimal import Decimal


def validate_types(obj) -> None:
    """Performs type validation on all fields that have not been assigned with None value
        Type comparison used instead of isinstance due to bool being subclass of int

    Args:
        obj (ProductItem | RankedProductItem | BrandItem): Instance of either dataclass listed

    Raises:
        TypeError: Raises if assigned value type does not match field definition in dataclass
    """
    for field_name, field_def in obj.__dataclass_fields__.items():
        attr = getattr(obj, field_name)
        actual_type = type(attr)
        if actual_type is not field_def.type and not isinstance(attr, type(None)):
            raise TypeError(
                f"Unexpected type for {field_name}: expected '{field_def.type}' but found '{actual_type}'"
            )


def validate_strings(obj) -> None:
    """Checks str fields for empty str
    Args:
        obj (ProductItem | RankedProductItem | BrandItem): Instance of either dataclass listed

    Raises:
        ValueError: Raises if empty string
    """
    for field_name, _ in obj.__dataclass_fields__.items():
        field_value = getattr(obj, field_name)
        if isinstance(field_value, str) and len(field_value.strip()) < 1:
            raise ValueError(f"{field_name} assigned empty string value")


@dataclass()
class ProductItem:
    __slots__ = [
        "code",
        "brand",
        "product_name",
        "variant",
        "retail_price",
        "on_sale",
        "current_price",
        "in_stock",
        "product_url",
    ]
    code: str
    brand: str
    product_name: str
    variant: str
    retail_price: Decimal
    on_sale: bool
    current_price: Decimal
    in_stock: bool
    product_url: str

    def __post_init__(self):
        validate_types(self)
        validate_strings(self)


@dataclass()
class RankedProductItem:
    __slots__ = [
        "code",
        "category",
        "ranking",
        "filter",
        "name",
        "rating",
        "review_count",
    ]
    code: str
    category: str
    ranking: int
    filter: str
    name: str
    rating: float
    review_count: int

    def __post_init__(self):
        validate_types(self)
        validate_strings(self)


@dataclass()
class BrandItem:
    __slots__ = ["name", "url"]
    name: str
    url: str

    def __post_init__(self):
        validate_types(self)
        validate_strings(self)
