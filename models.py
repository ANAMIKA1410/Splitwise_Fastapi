from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    mobile = Column(String(20), nullable=False, unique=True)

    expenses = relationship("Expense", back_populates="payer")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    payer_id = Column(Integer, ForeignKey('users.id'))
    total_amount = Column(Float, nullable=False)
    split_method = Column(String(50), nullable=False)  

    payer = relationship("User", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense")

    
class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey('expenses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    amount_owed = Column(Float)

    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="splits")

