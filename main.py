from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import db
from controllers import (
    auth_controller,
    user_controller,
    bank_account_controller,
    transaction_controller,
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(user_controller.router, prefix="/users", tags=["users"])
app.include_router(bank_account_controller.router, prefix="/accounts", tags=["accounts"])
app.include_router(transaction_controller.router, prefix="/transactions", tags=["transactions"])
#app.include_router(transaction_history_controller.router, prefix="/transactions", tags=["transaction-history"])

@app.on_event("startup")
async def startup_event():
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Bank API"}