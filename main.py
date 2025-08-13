from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine, Base
from datetime import date
from fastapi import FastAPI

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Leave Management System")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def days_between(start_date: date, end_date: date) -> int:
    delta = end_date - start_date
    return delta.days + 1  # inclusive

@app.post("/employees", response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(models.Employee).filter(models.Employee.email == employee.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_emp = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        joining_date=employee.joining_date,
        leave_balance=employee.leave_balance or 20
    )
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

@app.post("/leave/apply", response_model=schemas.LeaveOut)
def apply_leave(payload: schemas.LeaveCreate, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == payload.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    if payload.start_date > payload.end_date:
        raise HTTPException(status_code=400, detail="Invalid dates: start_date after end_date")

    if payload.start_date < emp.joining_date:
        raise HTTPException(status_code=400, detail="Cannot apply for leave before joining date")

    requested_days = days_between(payload.start_date, payload.end_date)
    if requested_days > emp.leave_balance:
        raise HTTPException(status_code=400, detail=f"Requested {requested_days} days, only {emp.leave_balance} available")

    # overlap check with APPROVED or PENDING leaves
    existing = db.query(models.LeaveRequest).filter(models.LeaveRequest.employee_id == emp.id).all()
    for ex in existing:
        if ex.status in ("PENDING", "APPROVED"):
            if not (ex.end_date < payload.start_date or ex.start_date > payload.end_date):
                raise HTTPException(status_code=400, detail="Overlapping leave request exists")

    db_leave = models.LeaveRequest(
        employee_id=emp.id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        reason=payload.reason,
        status="PENDING"
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

@app.put("/leave/{leave_id}/approve", response_model=schemas.LeaveOut)
def approve_leave(leave_id: int, db: Session = Depends(get_db)):
    lv = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not lv:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if lv.status != "PENDING":
        raise HTTPException(status_code=400, detail="Only pending requests can be approved")
    emp = db.query(models.Employee).filter(models.Employee.id == lv.employee_id).first()
    requested_days = days_between(lv.start_date, lv.end_date)
    if requested_days > emp.leave_balance:
        raise HTTPException(status_code=400, detail="Not enough leave balance to approve")

    # check overlap with other approved leaves (excluding this one)
    approved = db.query(models.LeaveRequest).filter(
        models.LeaveRequest.employee_id == emp.id,
        models.LeaveRequest.status == "APPROVED",
        models.LeaveRequest.id != lv.id
    ).all()
    for ex in approved:
        if not (ex.end_date < lv.start_date or ex.start_date > lv.end_date):
            raise HTTPException(status_code=400, detail="Overlaps with an already approved leave")

    emp.leave_balance -= requested_days
    lv.status = "APPROVED"
    db.commit()
    db.refresh(lv)
    return lv

@app.put("/leave/{leave_id}/reject", response_model=schemas.LeaveOut)
def reject_leave(leave_id: int, db: Session = Depends(get_db)):
    lv = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == leave_id).first()
    if not lv:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if lv.status != "PENDING":
        raise HTTPException(status_code=400, detail="Only pending requests can be rejected")
    lv.status = "REJECTED"
    db.commit()
    db.refresh(lv)
    return lv

@app.get("/leave/balance/{employee_id}")
def get_balance(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"employee_id": employee_id, "leave_balance": emp.leave_balance}

@app.get("/employees", response_model=List[schemas.EmployeeOut])
def list_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

@app.get("/leave/employee/{employee_id}", response_model=List[schemas.LeaveOut])
def list_employee_leaves(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db.query(models.LeaveRequest).filter(models.LeaveRequest.employee_id == employee_id).all()
