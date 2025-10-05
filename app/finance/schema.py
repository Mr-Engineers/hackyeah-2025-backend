from pydantic import BaseModel

class InvestmentActionRequest(BaseModel):
    amount: float

