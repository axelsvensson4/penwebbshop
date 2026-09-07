import sqlite3
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field

from app.core.security import hash_password
from app.database import get_database
from app.routers.auth import CurrentUser, get_current_user

router = APIRouter(prefix='/cart', tags=['cart'])
Database = Annotated[sqlite3.Connection, Depends(get_database)]
SHIPPING_ORE = 4900


class CartItemInput(BaseModel):
    product_id: int
    condition: str = Field(pattern='^(NEW|USED|WORN)$')
    quantity: int = Field(default=1, ge=1)


def cart_id(database: Database, user_id: int) -> int:
    row = database.execute('SELECT id FROM carts WHERE user_id = ?', (user_id,)).fetchone()
    if row: return int(row['id'])
    cursor = database.execute('INSERT INTO carts (user_id) VALUES (?)', (user_id,))
    database.commit()
    return int(cursor.lastrowid)


def cart_user(database: Database, request: Request, response: Response) -> CurrentUser:
    authorization = request.headers.get('authorization')
    if authorization:
        try:
            return get_current_user(database, authorization)
        except HTTPException:
            pass
    guest_id = request.cookies.get('guest_user_id')
    if guest_id and guest_id.isdigit():
        row = database.execute('SELECT id, name, username, role FROM users WHERE id = ? AND active = 1', (int(guest_id),)).fetchone()
        if row:
            return CurrentUser.model_validate(dict(row))
    username = f'guest-{secrets.token_urlsafe(12)}'
    cursor = database.execute(
        'INSERT INTO users (name, username, password_hash, role) VALUES (?, ?, ?, ?)',
        ('', username, hash_password(secrets.token_urlsafe(32)), 'USER'),
    )
    database.commit()
    user = CurrentUser(id=int(cursor.lastrowid), name='', username=username, role='USER')
    response.set_cookie('guest_user_id', str(user.id), httponly=True, samesite='lax', max_age=60 * 60 * 24 * 30)
    return user


@router.get('')
def get_cart(database: Database, request: Request, response: Response) -> dict[str, object]:
    user = cart_user(database, request, response)
    rows = database.execute('''SELECT cart_line_items.id, cart_line_items.product_id, cart_line_items.quantity, cart_line_items.condition, products.name, products.price_ore, products.image_url
        FROM carts JOIN cart_line_items ON cart_line_items.cart_id = carts.id JOIN products ON products.id = product_id WHERE carts.user_id = ?''', (user.id,)).fetchall()
    items = [dict(row) for row in rows]
    subtotal_ore = sum(int(item['price_ore']) * int(item['quantity']) for item in items)
    return {
        'items': items,
        'subtotal_ore': subtotal_ore,
        'shipping_ore': SHIPPING_ORE,
        'total_ore': subtotal_ore + SHIPPING_ORE,
    }


@router.post('/items')
def add_item(data: CartItemInput, database: Database, request: Request, response: Response) -> dict[str, int]:
    user = cart_user(database, request, response)
    if database.execute('SELECT 1 FROM products WHERE id = ?', (data.product_id,)).fetchone() is None: raise HTTPException(404, 'Produkten hittades inte.')
    current_cart = cart_id(database, user.id)
    database.execute('''INSERT INTO cart_line_items (cart_id, product_id, quantity, condition) VALUES (?, ?, ?, ?)
        ON CONFLICT(cart_id, product_id, condition) DO UPDATE SET quantity = cart_line_items.quantity + excluded.quantity''', (current_cart, data.product_id, data.quantity, data.condition))
    database.commit()
    return {'cart_id': current_cart}


@router.patch('/items/{item_id}')
def update_item(item_id: int, data: CartItemInput, database: Database, request: Request, response: Response) -> None:
    user = cart_user(database, request, response)
    cursor = database.execute('UPDATE cart_line_items SET quantity = ?, condition = ? WHERE id = ? AND cart_id IN (SELECT id FROM carts WHERE user_id = ?)', (data.quantity, data.condition, item_id, user.id))
    database.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail='Kundvagnsraden hittades inte.')


@router.delete('/items/{item_id}', status_code=204)
def delete_item(item_id: int, database: Database, request: Request, response: Response) -> None:
    user = cart_user(database, request, response)
    cursor = database.execute(
        'DELETE FROM cart_line_items WHERE id = ? AND cart_id IN (SELECT id FROM carts WHERE user_id = ?)',
        (item_id, user.id),
    )
    database.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail='Kundvagnsraden hittades inte.')


@router.delete('')
def clear_cart(database: Database, request: Request, response: Response) -> None:
    user = cart_user(database, request, response)
    database.execute('DELETE FROM carts WHERE user_id = ?', (user.id,)); database.commit()


@router.post('/checkout')
def checkout_cart(database: Database, request: Request, response: Response) -> dict[str, int]:
    user = cart_user(database, request, response)
    cart = database.execute('SELECT id FROM carts WHERE user_id = ?', (user.id,)).fetchone()
    if cart is None:
        raise HTTPException(status_code=400, detail='Kundvagnen är tom.')
    item_count = database.execute(
        'SELECT COUNT(*) AS count FROM cart_line_items WHERE cart_id = ?',
        (cart['id'],),
    ).fetchone()['count']
    if item_count == 0:
        raise HTTPException(status_code=400, detail='Kundvagnen är tom.')
    items = database.execute(
        '''SELECT cart_line_items.product_id, cart_line_items.quantity, cart_line_items.condition,
                  products.name, products.price_ore
           FROM cart_line_items
           JOIN products ON products.id = cart_line_items.product_id
           WHERE cart_line_items.cart_id = ?''',
        (cart['id'],),
    ).fetchall()
    order = database.execute(
        "INSERT INTO orders (user_id, status) VALUES (?, 'PENDING')",
        (user.id,),
    )
    order_id = int(order.lastrowid)
    database.executemany(
        '''INSERT INTO order_items (order_id, product_id, product_name, price_ore, quantity, condition)
           VALUES (?, ?, ?, ?, ?, ?)''',
        [
            (order_id, item['product_id'], item['name'], item['price_ore'], item['quantity'], item['condition'])
            for item in items
        ],
    )
    database.execute('DELETE FROM cart_line_items WHERE cart_id = ?', (cart['id'],))
    database.execute('DELETE FROM carts WHERE id = ?', (cart['id'],))
    database.commit()
    # Bara gästbeställningar behöver en tillfällig koppling till ett framtida konto.
    # En inloggad användares order sparas redan direkt på det riktiga kontot.
    if request.cookies.get('guest_user_id') == str(user.id):
        response.set_cookie('pending_order_id', str(order_id), httponly=True, samesite='lax')
    else:
        response.delete_cookie('pending_order_id')
    return {'order_id': order_id}


@router.delete('/checkout/{order_id}/claim', status_code=204)
def cancel_order_claim(order_id: int, response: Response) -> None:
    response.delete_cookie('pending_order_id')
