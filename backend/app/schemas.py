from decimal import Decimal, ROUND_HALF_UP
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator

PRODUCT_CATEGORIES = (
    'Lyxiga',
    'Traditionella',
    'Fjäderpenna',
    'För astronauter',
    'Limited Edition',
)


class Product(BaseModel):
    id: int
    name: str
    slug: str | None = None
    summary: str | None = None
    description: str | None = None
    price_ore: int = Field(ge=0)
    compare_at_price_ore: int | None = Field(default=None, ge=0)
    currency: str = 'SEK'
    image_url: str | None = None
    is_available: bool = True
    is_outlet: bool = False
    availability: str = 'IN_STOCK'
    stock_quantity: int = Field(default=0, ge=0)
    condition: str = 'NEW'
    featured: bool = False
    category: str | None = None
    average_rating: float = 0
    review_count: int = 0


class Category(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None


class FaqItem(BaseModel):
    id: int
    question: str
    answer: str


class ProductType(StrEnum):
    STANDARD = 'STANDARD'
    OUTLET = 'OUTLET'


class Availability(StrEnum):
    IN_STOCK = 'IN_STOCK'
    LOW_STOCK = 'LOW_STOCK'
    OUT_OF_STOCK = 'OUT_OF_STOCK'


class ProductCondition(StrEnum):
    NEW = 'NEW'
    USED = 'USED'
    WORN = 'WORN'


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    short_description: str = Field(max_length=240)
    description: str | None = Field(default=None, max_length=5000)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    currency: str = Field(default='SEK', min_length=3, max_length=3)
    category: str = Field(min_length=1, max_length=80)
    product_type: ProductType = ProductType.STANDARD
    availability: Availability = Availability.IN_STOCK
    active: bool = True
    condition: ProductCondition = ProductCondition.NEW
    featured: bool = False
    stock_quantity: int = Field(default=0, ge=0)

    @field_validator('currency')
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()

    @field_validator('category')
    @classmethod
    def validate_category(cls, value: str) -> str:
        category = value.strip()
        if category not in PRODUCT_CATEGORIES:
            raise ValueError('Ogiltig produktkategori.')
        return category

    def price_in_ore(self) -> int:
        return int((self.price * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


class AdminProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    short_description: str
    description: str
    price_ore: int
    currency: str
    category: str
    product_type: ProductType
    availability: Availability
    active: bool
    image_url: str | None = None
    condition: ProductCondition = ProductCondition.NEW
    featured: bool = False
    stock_quantity: int = Field(default=0, ge=0)


class ReviewTemplate(BaseModel):
    id: int
    title: str
    name: str
    age: int
    rating: int
    comment: str
    active: bool
