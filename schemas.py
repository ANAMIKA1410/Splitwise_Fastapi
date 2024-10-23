from pydantic import BaseModel, EmailStr, conint, validator
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str

class ExpenseCreate(BaseModel):
    payer_id: int
    total_amount: float 
    involved_user_ids: List[int]
    split_method: str  
    exact_amounts: Optional[List[float]] = None  

    percentages: Optional[List[int]] = None 

    @validator('percentages', pre=True, always=True) 
    def validate_percentages(cls, v): 
        if v is not None and sum(v) != 100: 
            raise ValueError('Percentages must add up to 100.') 
        return v
