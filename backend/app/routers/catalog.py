import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends

from app.database import get_database
from app.schemas import Category

router = APIRouter(prefix='/categories', tags=['catalog'])
Database = Annotated[sqlite3.Connection, Depends(get_database)]


@router.get('', response_model=list[Category])
def list_categories(database: Database) -> list[Category]:
    rows = database.execute(
        'SELECT id, name, slug, description FROM categories ORDER BY name'
    ).fetchall()
    return [Category.model_validate(dict(row)) for row in rows]
