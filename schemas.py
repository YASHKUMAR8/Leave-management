from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None
    joining_date: date
    leave_balance: Optional[int] = 20

class EmployeeOut(EmployeeCreate):
    id: int
    class Config:
        orm_mode = True

class LeaveCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None

class LeaveOut(BaseModel):
    id: int
    employee_id: int
    start_date: date
    end_date: date
    status: str
    reason: Optional[str] = None
    class Config:
        orm_mode = True
