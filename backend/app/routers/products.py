import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.database import get_database
from app.schemas import Product

router = APIRouter(prefix='/products', tags=['products'])
Database = Annotated[sqlite3.Connection, Depends(get_database)]


@router.get('', response_model=list[Product])
def list_products(
    database: Database,
    category: str | None = None,
    search: str | None = None,
    outlet: bool | None = None,
    featured: bool | None = None,
    available_only: bool = True,
    limit: int = Query(default=24, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[Product]:
    """Produktlista för shop- och outletsidorna."""
    conditions: list[str] = []
    values: list[str | int] = []

    if category:
        conditions.append('categories.slug = ?')
        values.append(category)
    if search:
        conditions.append('(products.name LIKE ? OR products.summary LIKE ? OR products.description LIKE ?)')
        search_term = f'%{search.strip()}%'
        values.extend((search_term, search_term, search_term))
    if outlet is not None:
        conditions.append('products.is_outlet = ?')
        values.append(int(outlet))
    if featured is not None:
        conditions.append('products.featured = ?')
        values.append(int(featured))
    if available_only:
        conditions.append("products.is_available = 1 AND products.availability != 'OUT_OF_STOCK'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ''
    rows = database.execute(
        f'''SELECT DISTINCT products.id, products.name, products.slug, products.summary,
                   products.description, products.price_ore, products.compare_at_price_ore,
                   products.currency, products.image_url, products.is_available, products.is_outlet, products.availability, products.condition, products.featured, products.stock_quantity,
                   MAX(categories.slug) AS category,
                   COALESCE(AVG(product_reviews.rating), 0) AS average_rating, COUNT(product_reviews.id) AS review_count
            FROM products
            LEFT JOIN product_categories ON product_categories.product_id = products.id
            LEFT JOIN categories ON categories.id = product_categories.category_id
            LEFT JOIN product_reviews ON product_reviews.product_id = products.id
            {where_clause}
            GROUP BY products.id ORDER BY products.id
            LIMIT ? OFFSET ?''',
        [*values, limit, offset],
    ).fetchall()
    return [Product.model_validate(dict(row)) for row in rows]


@router.get('/{product_id}', response_model=Product)
def get_product(product_id: int, database: Database) -> Product:
    row = database.execute(
        '''SELECT products.id, name, slug, summary, description, price_ore, compare_at_price_ore,
                  currency, image_url, is_available, is_outlet, availability, condition, featured, stock_quantity,
                  COALESCE(AVG(product_reviews.rating), 0) AS average_rating, COUNT(product_reviews.id) AS review_count
           FROM products LEFT JOIN product_reviews ON product_reviews.product_id = products.id
           WHERE products.id = ? GROUP BY products.id''',
        (product_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail='Produkten hittades inte.')
    return Product.model_validate(dict(row))
