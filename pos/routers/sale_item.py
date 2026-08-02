from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from pos.services import sale_item as sale_item_service
from pos.schemas.sale_item import SaleItemExtendedRead
from pos.core.security import get_current_user

router = APIRouter(prefix="/sale-items", tags=["sale items"])

@router.get("/sale/{sale_id}", response_model=list[SaleItemExtendedRead])
def get_line_items_by_sale(
    sale_id: int, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    
    return sale_item_service.list_items_by_sale(db, sale_id,current_user)
