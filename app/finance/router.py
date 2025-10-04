from .service import FinanceService
from fastapi import APIRouter, HTTPException
from .schema import InvestmentActionRequest

router = APIRouter(prefix="/invest")
finance_service = FinanceService()

@router.post("/invest")
def invest(request: InvestmentActionRequest):
    try:
        return finance_service.invest(request.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/withdraw")
def withdraw_cash(request: InvestmentActionRequest):
    try:
        return finance_service.withdraw(request.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
