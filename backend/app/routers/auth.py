import sqlite3
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, Request, Response, status
from pydantic import BaseModel, Field

import jwt

from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.database import get_database

router = APIRouter(prefix='/auth', tags=['auth'])
Database = Annotated[sqlite3.Connection, Depends(get_database)]


class LoginInput(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class CurrentUser(BaseModel):
    id: int
    name: str
    username: str
    role: str
    email: str = ''
    address: str = ''
    postal_code: str = ''
    city: str = ''


class LoginResponse(BaseModel):
    token: str
    user: CurrentUser


class RegisterInput(LoginInput):
    name: str = Field(min_length=1, max_length=120)
    claim_order_id: int | None = Field(default=None, ge=1)


class ProfileUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(max_length=254)
    address: str = Field(max_length=200)
    postal_code: str = Field(max_length=20)
    city: str = Field(max_length=120)


def get_current_user(database: Database, authorization: Annotated[str | None, Header()] = None, access_token: Annotated[str | None, Cookie()] = None) -> CurrentUser:
    token = authorization.removeprefix('Bearer ') if authorization and authorization.startswith('Bearer ') else access_token
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Inloggning krävs.')
    try:
        payload = decode_access_token(token)
        if payload.get('type') != 'access': raise ValueError
        user_id = int(str(payload['sub']))
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ogiltig eller utgången token.')
    row = database.execute('SELECT id, name, username, role, email, address, postal_code, city FROM users WHERE id = ? AND active = 1', (user_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Ogiltig session.')
    return CurrentUser.model_validate(dict(row))


def require_admin(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    if user.role != 'ADMIN':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Administratörsbehörighet krävs.')
    return user


def merge_guest_cart(database: sqlite3.Connection, guest_user_id: int, user_id: int) -> None:
    if guest_user_id == user_id:
        return
    guest_cart = database.execute('SELECT id FROM carts WHERE user_id = ?', (guest_user_id,)).fetchone()
    if guest_cart is None:
        return
    user_cart = database.execute('SELECT id FROM carts WHERE user_id = ?', (user_id,)).fetchone()
    if user_cart is None:
        cursor = database.execute('INSERT INTO carts (user_id) VALUES (?)', (user_id,))
        user_cart_id = int(cursor.lastrowid)
    else:
        user_cart_id = int(user_cart['id'])
    guest_items = database.execute(
        'SELECT product_id, quantity, condition FROM cart_line_items WHERE cart_id = ?',
        (guest_cart['id'],),
    ).fetchall()
    for item in guest_items:
        database.execute(
            '''INSERT INTO cart_line_items (cart_id, product_id, quantity, condition)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(cart_id, product_id, condition)
               DO UPDATE SET quantity = cart_line_items.quantity + excluded.quantity''',
            (user_cart_id, item['product_id'], item['quantity'], item['condition']),
        )
    database.execute('DELETE FROM cart_line_items WHERE cart_id = ?', (guest_cart['id'],))
    database.execute('DELETE FROM carts WHERE id = ?', (guest_cart['id'],))
    database.commit()


def claim_guest_order(database: sqlite3.Connection, guest_user_id: int, user_id: int, order_id: int) -> None:
    order = database.execute(
        'SELECT id FROM orders WHERE id = ? AND user_id = ?',
        (order_id, guest_user_id),
    ).fetchone()
    if order is None:
        raise HTTPException(status_code=404, detail='Beställningen kunde inte kopplas till kontot.')
    database.execute('UPDATE orders SET user_id = ? WHERE id = ?', (user_id, order_id))
    database.commit()


@router.post('/login', response_model=LoginResponse)
def login(data: LoginInput, database: Database, request: Request, response: Response) -> LoginResponse:
    row = database.execute('SELECT * FROM users WHERE username = ? AND active = 1', (data.username,)).fetchone()
    if row is None or not verify_password(data.password, row['password_hash']):
        raise HTTPException(status_code=401, detail='Fel användarnamn eller lösenord.')
    token = create_access_token(int(row['id']), str(row['role']))
    guest_user_id = request.cookies.get('guest_user_id')
    if guest_user_id and guest_user_id.isdigit():
        merge_guest_cart(database, int(guest_user_id), int(row['id']))
        response.delete_cookie('guest_user_id')
    response.set_cookie('access_token', token, httponly=True, samesite='lax', max_age=30 * 60)
    return LoginResponse(token=token, user=CurrentUser.model_validate(dict(row)))


@router.post('/register', response_model=LoginResponse, status_code=201)
def register(data: RegisterInput, database: Database, request: Request, response: Response) -> LoginResponse:
    if database.execute('SELECT 1 FROM users WHERE username = ?', (data.username,)).fetchone():
        raise HTTPException(status_code=409, detail='Användarnamnet är redan upptaget.')
    guest_user_id = request.cookies.get('guest_user_id')
    if data.claim_order_id is not None:
        pending_order_id = request.cookies.get('pending_order_id')
        if (
            not guest_user_id
            or not guest_user_id.isdigit()
            or pending_order_id != str(data.claim_order_id)
        ):
            raise HTTPException(status_code=403, detail='Beställningen kan inte kopplas till detta konto.')
        order = database.execute(
            'SELECT 1 FROM orders WHERE id = ? AND user_id = ?',
            (data.claim_order_id, int(guest_user_id)),
        ).fetchone()
        if order is None:
            raise HTTPException(status_code=404, detail='Beställningen kunde inte kopplas till kontot.')
    cursor = database.execute(
        'INSERT INTO users (name, username, password_hash, role) VALUES (?, ?, ?, ?)',
        (data.name.strip(), data.username.strip(), hash_password(data.password), 'USER'),
    )
    database.commit()
    result = login(LoginInput(username=data.username, password=data.password), database, request, response)
    if data.claim_order_id is not None:
        claim_guest_order(database, int(guest_user_id), result.user.id, data.claim_order_id)
        response.delete_cookie('pending_order_id')
    return result


@router.post('/logout', status_code=204)
def logout(response: Response) -> None:
    response.delete_cookie('access_token')


@router.get('/me', response_model=CurrentUser)
def me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    return user


@router.patch('/me', response_model=CurrentUser)
def update_me(data: ProfileUpdate, database: Database, user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    database.execute(
        'UPDATE users SET name = ?, email = ?, address = ?, postal_code = ?, city = ? WHERE id = ?',
        (data.name.strip(), data.email.strip(), data.address.strip(), data.postal_code.strip(), data.city.strip(), user.id),
    )
    database.commit()
    return CurrentUser(
        id=user.id,
        name=data.name.strip(),
        username=user.username,
        role=user.role,
        email=data.email.strip(),
        address=data.address.strip(),
        postal_code=data.postal_code.strip(),
        city=data.city.strip(),
    )
