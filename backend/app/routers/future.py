from fastapi import APIRouter, HTTPException

router = APIRouter(tags=['future integration'])


def not_implemented(feature: str) -> None:
    raise HTTPException(
        status_code=501,
        detail=f'{feature} är förberedd men inte implementerad ännu.',
    )


@router.get('/cart')
def get_cart() -> None:
    not_implemented('Kundvagn')


@router.post('/cart/items')
def add_cart_item() -> None:
    not_implemented('Kundvagn')


@router.patch('/cart/items/{item_id}')
def update_cart_item(item_id: int) -> None:
    not_implemented('Kundvagn')


@router.delete('/cart/items/{item_id}', status_code=204)
def delete_cart_item(item_id: int) -> None:
    not_implemented('Kundvagn')


@router.post('/checkout/quote')
def quote_checkout() -> None:
    not_implemented('Prissättning och checkout')


@router.post('/checkout/orders')
def create_order() -> None:
    not_implemented('Order och betalning')


@router.get('/shipping-options')
def list_shipping_options() -> None:
    not_implemented('Leveransalternativ')


@router.post('/auth/login')
def login() -> None:
    not_implemented('Autentisering')


@router.post('/auth/register')
def register() -> None:
    not_implemented('Autentisering')


@router.post('/auth/logout', status_code=204)
def logout() -> None:
    not_implemented('Autentisering')


@router.get('/account')
def get_account() -> None:
    not_implemented('Konto')


@router.patch('/account/profile')
def update_profile() -> None:
    not_implemented('Konto')


@router.get('/account/orders')
def list_orders() -> None:
    not_implemented('Orderhistorik')


@router.get('/account/addresses')
def list_addresses() -> None:
    not_implemented('Adressbok')


@router.post('/account/addresses')
def create_address() -> None:
    not_implemented('Adressbok')


@router.patch('/account/addresses/{address_id}')
def update_address(address_id: int) -> None:
    not_implemented('Adressbok')


@router.delete('/account/addresses/{address_id}', status_code=204)
def delete_address(address_id: int) -> None:
    not_implemented('Adressbok')
