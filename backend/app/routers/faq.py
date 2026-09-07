from fastapi import APIRouter

from app.schemas import FaqItem

router = APIRouter(prefix='/faq', tags=['content'])


@router.get('', response_model=list[FaqItem])
def list_faq() -> list[FaqItem]:
    """Integrationspunkt för FAQ/CMS. Innehåll hanteras i frontend tills vidare."""
    return []
