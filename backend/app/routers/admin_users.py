import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.database import get_database
from app.routers.auth import CurrentUser, require_admin

router = APIRouter(prefix='/admin/users', tags=['admin users'])
Database = Annotated[sqlite3.Connection, Depends(get_database)]
Admin = Annotated[CurrentUser, Depends(require_admin)]


class AdminUserResponse(BaseModel):
    id: int
    name: str
    username: str
    role: str
    active: bool


@router.get('', response_model=list[AdminUserResponse])
def list_users(database: Database, _: Admin) -> list[AdminUserResponse]:
    rows = database.execute(
        "SELECT id, name, username, role, active FROM users WHERE username NOT LIKE 'guest-%' ORDER BY id DESC"
    ).fetchall()
    return [AdminUserResponse.model_validate(dict(row)) for row in rows]


@router.patch('/{user_id}/ban', response_model=AdminUserResponse)
def toggle_user_ban(user_id: int, database: Database, admin: Admin) -> AdminUserResponse:
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail='Du kan inte porta ditt eget konto.')
    user = database.execute('SELECT id, active FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        raise HTTPException(status_code=404, detail='Användaren hittades inte.')
    database.execute('UPDATE users SET active = ? WHERE id = ?', (0 if user['active'] else 1, user_id))
    database.commit()
    row = database.execute('SELECT id, name, username, role, active FROM users WHERE id = ?', (user_id,)).fetchone()
    return AdminUserResponse.model_validate(dict(row))


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, database: Database, admin: Admin) -> None:
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail='Du kan inte radera ditt eget konto.')
    if database.execute('SELECT 1 FROM users WHERE id = ?', (user_id,)).fetchone() is None:
        raise HTTPException(status_code=404, detail='Användaren hittades inte.')
    database.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
    database.execute('DELETE FROM product_reviews WHERE user_id = ?', (user_id,))
    database.execute('DELETE FROM cart_line_items WHERE cart_id IN (SELECT id FROM carts WHERE user_id = ?)', (user_id,))
    database.execute('DELETE FROM carts WHERE user_id = ?', (user_id,))
    database.execute('DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE user_id = ?)', (user_id,))
    database.execute('DELETE FROM orders WHERE user_id = ?', (user_id,))
    database.execute('DELETE FROM users WHERE id = ?', (user_id,))
    database.commit()
