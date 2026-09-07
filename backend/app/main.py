from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import initialize_database
from app.routers import admin_products, admin_users, auth, cart, catalog, faq, future, products, reviews


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title='Webbshop API', version='0.1.0', lifespan=lifespan)

Path('app/uploads').mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/health', tags=['system'])
def health_check() -> dict[str, str]:
    return {'status': 'ok'}


app.include_router(products.router, prefix='/api')
app.include_router(catalog.router, prefix='/api')
app.include_router(faq.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(cart.router, prefix='/api')
app.include_router(reviews.router, prefix='/api')
app.include_router(future.router, prefix='/api')
app.include_router(admin_products.router, prefix='/api')
app.include_router(admin_users.router, prefix='/api')
app.mount('/uploads', StaticFiles(directory='app/uploads'), name='uploads')
