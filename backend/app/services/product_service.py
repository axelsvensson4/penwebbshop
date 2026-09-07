import re
import sqlite3

from app.repositories.product_repository import ProductRepository
from app.schemas import AdminProductResponse, ProductCreate


def slugify(value: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')
    return slug or 'produkt'


class ProductService:
    def __init__(self, database: sqlite3.Connection):
        self.repository = ProductRepository(database)

    def create_product(self, data: ProductCreate) -> AdminProductResponse:
        base_slug = slugify(data.name)
        slug = base_slug
        suffix = 2
        while self.repository.slug_exists(slug):
            slug = f'{base_slug}-{suffix}'
            suffix += 1

        row = self.repository.create({
            'name': data.name.strip(), 'slug': slug, 'short_description': data.short_description.strip(),
            'description': '.' if data.description is None else data.description.strip(), 'price_ore': data.price_in_ore(), 'currency': data.currency,
            'is_available': data.availability != 'OUT_OF_STOCK', 'is_outlet': data.product_type == 'OUTLET',
            'product_type': data.product_type, 'availability': data.availability, 'active': data.active,
            'condition': data.condition, 'featured': data.featured, 'stock_quantity': data.stock_quantity,
        })
        category_id = self.repository.find_or_create_category(data.category)
        self.repository.assign_category(int(row['id']), category_id)
        return AdminProductResponse.model_validate(dict(self.repository.get_by_id(int(row['id']))))

    def add_image(self, product_id: int, file_name: str, alt_text: str | None) -> AdminProductResponse:
        self.repository.get_by_id(product_id)
        self.repository.add_image(product_id, file_name, alt_text)
        return AdminProductResponse.model_validate(dict(self.repository.get_by_id(product_id)))

    def get_product(self, product_id: int) -> AdminProductResponse:
        return AdminProductResponse.model_validate(dict(self.repository.get_by_id(product_id)))

    def update_product(self, product_id: int, data: ProductCreate) -> AdminProductResponse:
        self.repository.get_by_id(product_id)
        self.repository.update(product_id, {
            'name': data.name.strip(), 'short_description': data.short_description.strip(),
            'description': '.' if data.description is None else data.description.strip(), 'price_ore': data.price_in_ore(), 'currency': data.currency,
            'is_available': data.availability != 'OUT_OF_STOCK', 'is_outlet': data.product_type == 'OUTLET',
            'product_type': data.product_type, 'availability': data.availability, 'active': data.active,
            'condition': data.condition, 'featured': data.featured, 'stock_quantity': data.stock_quantity,
        })
        category_id = self.repository.find_or_create_category(data.category)
        self.repository.assign_category(product_id, category_id)
        return self.get_product(product_id)
