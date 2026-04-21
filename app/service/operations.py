from fastapi import HTTPException

from app.database import SessionLocal
#Import models to operate with money
from app.schemas import OperationRequest
#Import repository to work with wallets
from app.repository import wallets as wallets_repository


def add_income(operation: OperationRequest):
    db = SessionLocal()
    try:
        if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
            )

        #Add income to BALANCE
        wallet = wallets_repository.add_income(db, operation.wallet_name, operation.amount)
        
        db.commit()
        #return info about operation
        return {
            "message": "Income added",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": wallet.balance
        }
    finally: 
        db.close()

def add_expense(operation: OperationRequest):
    #is wallet exist?
    db = SessionLocal()
    try:
        if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
            )
        # is blance enough?
        wallet = wallets_repository.get_wallet_balance_by_name(db, operation.wallet_name)
        if wallet.balance < operation.amount:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient funds. Available: {wallet}"
            )
        #add expence
        wallet = wallets_repository.add_expence(db, operation.wallet_name, operation.amount)
        
        db.commit()
        return{
            "message": "Expense added",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": wallet.balance
        }
    finally:
        db.close()