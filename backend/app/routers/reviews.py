import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.database import get_database
from app.routers.auth import CurrentUser, get_current_user

router = APIRouter(tags=['reviews'])
Database = Annotated[sqlite3.Connection, Depends(get_database)]


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    title: str = Field(min_length=1, max_length=120)
    comment: str = Field(min_length=1, max_length=1000)


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int | None = None
    rating: int
    comment: str
    author_name: str
    review_title: str
    product_name: str | None = None
    created_at: str


@router.post('/products/{product_id}/reviews', response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(product_id: int, data: ReviewCreate, database: Database, user: Annotated[CurrentUser, Depends(get_current_user)]) -> ReviewResponse:
    if database.execute('SELECT 1 FROM products WHERE id = ?', (product_id,)).fetchone() is None:
        raise HTTPException(status_code=404, detail='Produkten hittades inte.')
    cursor = database.execute(
        '''INSERT INTO product_reviews
           (product_id, user_id, rating, comment, author_name, review_title, status, verified_purchase)
           VALUES (?, ?, ?, ?, ?, ?, 'PUBLISHED', 0)''',
        (product_id, user.id, data.rating, data.comment.strip(), user.name, data.title.strip()),
    )
    database.commit()
    row = database.execute('SELECT id, product_id, user_id, rating, comment, author_name, review_title, created_at FROM product_reviews WHERE id = ?', (cursor.lastrowid,)).fetchone()
    return ReviewResponse.model_validate(dict(row))


@router.get('/products/{product_id}/reviews', response_model=list[ReviewResponse])
def list_product_reviews(product_id: int, database: Database) -> list[ReviewResponse]:
    rows = database.execute(
        "SELECT id, product_id, user_id, rating, comment, author_name, review_title, created_at FROM product_reviews WHERE product_id = ? AND status = 'PUBLISHED' ORDER BY created_at DESC",
        (product_id,),
    ).fetchall()
    return [ReviewResponse.model_validate(dict(row)) for row in rows]


@router.get('/reviews/me', response_model=list[ReviewResponse])
def my_reviews(database: Database, user: Annotated[CurrentUser, Depends(get_current_user)]) -> list[ReviewResponse]:
    rows = database.execute(
        '''SELECT product_reviews.id, product_reviews.product_id, product_reviews.user_id,
                  product_reviews.rating, product_reviews.comment, product_reviews.author_name,
                  product_reviews.review_title, product_reviews.created_at,
                  products.name AS product_name
           FROM product_reviews JOIN products ON products.id = product_reviews.product_id
           WHERE product_reviews.user_id = ? ORDER BY product_reviews.created_at DESC''',
        (user.id,),
    ).fetchall()
    return [ReviewResponse.model_validate(dict(row)) for row in rows]


@router.delete('/products/{product_id}/reviews/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    product_id: int,
    review_id: int,
    database: Database,
    user: Annotated[CurrentUser, Depends(get_current_user)],
) -> None:
    review = database.execute(
        'SELECT product_id, user_id FROM product_reviews WHERE id = ?',
        (review_id,),
    ).fetchone()
    if review is None or review['product_id'] != product_id:
        raise HTTPException(status_code=404, detail='Recensionen hittades inte.')
    if review['user_id'] != user.id:
        raise HTTPException(status_code=403, detail='Du kan bara radera dina egna recensioner.')
    database.execute('DELETE FROM product_reviews WHERE id = ?', (review_id,))
    database.commit()


@router.get('/orders/me')
def my_orders(database: Database, user: Annotated[CurrentUser, Depends(get_current_user)]) -> list[dict[str, object]]:
    rows = database.execute('SELECT id, status, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user.id,)).fetchall()
    orders = []
    for row in rows:
        order = dict(row)
        items = database.execute(
            '''SELECT id, product_id, product_name, price_ore, quantity, condition
               FROM order_items WHERE order_id = ? ORDER BY id''',
            (order['id'],),
        ).fetchall()
        order['items'] = [dict(item) for item in items]
        orders.append(order)
    return orders
