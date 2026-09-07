import sqlite3
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.database import get_database
from app.schemas import AdminProductResponse, ProductCreate, ReviewTemplate
from app.services.product_service import ProductService
from app.routers.auth import require_admin

router = APIRouter(prefix='/admin/products', tags=['admin products'])
Database = Annotated[sqlite3.Connection, Depends(get_database)]
UPLOAD_DIRECTORY = Path(__file__).resolve().parent.parent / 'uploads' / 'products'
MAX_IMAGE_BYTES = 5 * 1024 * 1024


@router.post('', response_model=AdminProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, database: Database, _: Annotated[object, Depends(require_admin)]) -> AdminProductResponse:
    """Demo-route: måste skyddas med ADMIN-behörighet före produktion."""
    return ProductService(database).create_product(data)


@router.get('', response_model=list[AdminProductResponse])
def list_admin_products(database: Database, _: Annotated[object, Depends(require_admin)]) -> list[AdminProductResponse]:
    rows = database.execute('''SELECT products.id, products.name, products.slug, products.short_description,
        products.description, products.price_ore, products.currency, categories.name AS category,
        products.product_type, products.availability, products.active, products.image_url, products.condition, products.featured, products.stock_quantity
        FROM products LEFT JOIN product_categories ON product_categories.product_id = products.id
        LEFT JOIN categories ON categories.id = product_categories.category_id ORDER BY products.id DESC''').fetchall()
    return [AdminProductResponse.model_validate(dict(row)) for row in rows]


@router.get('/{product_id}', response_model=AdminProductResponse)
def get_admin_product(product_id: int, database: Database, _: Annotated[object, Depends(require_admin)]) -> AdminProductResponse:
    try:
        return ProductService(database).get_product(product_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.put('/{product_id}', response_model=AdminProductResponse)
def update_product(product_id: int, data: ProductCreate, database: Database, _: Annotated[object, Depends(require_admin)]) -> AdminProductResponse:
    try:
        return ProductService(database).update_product(product_id, data)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete('/{product_id}', status_code=204)
def delete_product(product_id: int, database: Database, _: Annotated[object, Depends(require_admin)]) -> None:
    database.execute('DELETE FROM cart_line_items WHERE product_id = ?', (product_id,))
    database.execute('DELETE FROM product_reviews WHERE product_id = ?', (product_id,))
    database.execute('DELETE FROM product_images WHERE product_id = ?', (product_id,))
    database.execute('DELETE FROM product_categories WHERE product_id = ?', (product_id,))
    database.execute('DELETE FROM products WHERE id = ?', (product_id,))
    database.commit()


@router.get('/review-templates', response_model=list[ReviewTemplate])
def list_review_templates(database: Database, _: Annotated[object, Depends(require_admin)]) -> list[ReviewTemplate]:
    rows = database.execute(
        '''SELECT id, title, name, age, rating, comment, active
           FROM review_templates WHERE active = 1 ORDER BY id'''
    ).fetchall()
    return [ReviewTemplate.model_validate(dict(row)) for row in rows]


@router.post('/{product_id}/image', response_model=AdminProductResponse)
async def upload_product_image(
    product_id: int,
    database: Database,
    request: Request,
    alt_text: str | None = None,
    _: Annotated[object, Depends(require_admin)] = None,
) -> AdminProductResponse:
    payload = await request.body()
    extension = '.jpg' if payload.startswith(b'\xff\xd8\xff') else None
    if payload.startswith(b'\x89PNG\r\n\x1a\n'):
        extension = '.png'
    if payload.startswith(b'RIFF') and payload[8:12] == b'WEBP':
        extension = '.webp'
    allowed_mime_types = {'image/jpeg', 'image/png', 'image/webp'}
    if request.headers.get('content-type') not in allowed_mime_types or len(payload) > MAX_IMAGE_BYTES or extension is None:
        raise HTTPException(status_code=422, detail='Bilden måste vara JPG, PNG eller WebP och högst 5 MB.')

    file_name = f'{uuid4().hex}{extension}'
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    (UPLOAD_DIRECTORY / file_name).write_bytes(payload)
    try:
        return ProductService(database).add_image(product_id, file_name, alt_text)
    except LookupError as error:
        (UPLOAD_DIRECTORY / file_name).unlink(missing_ok=True)
        raise HTTPException(status_code=404, detail=str(error)) from error
