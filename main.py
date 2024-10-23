from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Expense, User, ExpenseSplit, Base
from schemas import UserCreate, ExpenseCreate

from database import engine, get_db, Base, SessionLocal
from sqlalchemy import func


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(email=user.email, name=user.name, mobile=user.mobile)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/expenses/")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    if expense.split_method == 'percentage' and sum(expense.percentages) != 100:
        raise HTTPException(status_code=400, detail="Percentages must add up to 100%")

    total_amount = expense.total_amount
    splits = []
    
    if expense.split_method == 'equal':
        amount_per_user = total_amount / len(expense.involved_user_ids)
        for user_id in expense.involved_user_ids:
            splits.append({"user_id": user_id, "amount_owed": amount_per_user})

    elif expense.split_method == 'exact':
        if sum(expense.exact_amounts) != total_amount:
            raise HTTPException(status_code=400, detail="Exact amounts must add up to the total")
        for i, user_id in enumerate(expense.involved_user_ids):
            splits.append({"user_id": user_id, "amount_owed": expense.exact_amounts[i]})

    elif expense.split_method == 'percentage':
        for i, user_id in enumerate(expense.involved_user_ids):
            split_amount = total_amount * (expense.percentages[i] / 100)
            splits.append({"user_id": user_id, "amount_owed": split_amount})

    db_expense = Expense(payer_id=expense.payer_id, total_amount=total_amount, split_method=expense.split_method)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    for split in splits:
        db_split = ExpenseSplit(expense_id=db_expense.id, user_id=split['user_id'], amount_owed=split['amount_owed'])
        db.add(db_split)

    db.commit()
    return {"status": "Expense added successfully"}

@app.get("/balance/{user_id}")
def get_balance(user_id: int, db: Session = Depends(get_db)):
    total_owed = db.query(func.sum(ExpenseSplit.amount_owed)).filter(ExpenseSplit.user_id == user_id).scalar()
    total_paid = db.query(func.sum(Expense.total_amount)).filter(Expense.payer_id == user_id).scalar()
    balance = total_paid - total_owed if total_paid and total_owed else 0
    return {"user_id": user_id, "balance": balance}

@app.get("/balance/download/{user_id}")
def download_balance_sheet(user_id: int):
    
    pass






























