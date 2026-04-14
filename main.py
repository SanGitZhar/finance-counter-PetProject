from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
#Инициализация FASTAPi приложения
app = FastAPI()


BALANCE = {}


class OperationRequest(BaseModel):
    wallet_name: str
    amount: float
    description: str | None = None 


@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        return {"total: ", sum(BALANCE.values())}
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    return {"wallet": wallet_name, "balance": BALANCE[wallet_name]}


@app.post("/wallets/{name}")
def create_wallet(name: str, initial_balance:float = 0):
    if name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{name}' alredy exist"
        )
    #create new wallet
    BALANCE[name] = initial_balance
    return {
        "message": f"Wallet '{name}' created",
        "wallet": name,
        "balance": BALANCE[name]
    }

@app.post("/operations/income")
def add_income(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    if operation.amount <=0:
        raise HTTPException(
            status_code=400,
            detail=f"Amount must be positive"
        )
    #Add income to BALANCE
    BALANCE[operation.wallet_name] += operation.amount
    #return info about operation
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }

@app.post("/operations/expense")
def add_expense(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    if operation.amount <=0:
        raise HTTPException(
            status_code=400,
            detail=f"Amount must be positive"
        )

    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {BALANCE[operation.wallet_name]}"
        )
    #add expence
    BALANCE[operation.wallet_name] -= operation.amount
    return{
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }

# def receive_money(name: str, amount:int):
#     if name not in BALANCE:
#         BALANCE[name] = 0
#     BALANCE[name] += amount

#     return{
#         "message": f"Added {amount} to {name}",
#         "wallet": name,
#         "new_balance": BALANCE[name]
#     }


