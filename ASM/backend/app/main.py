from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.db.migrations import run_startup_migrations
from app.models import user, voucher, document, sla_config, notification
from app.api.routes import users, auth, vouchers, reports, documents, chatbot

# STEP 1: Create FastAPI app FIRST
app = FastAPI(
    title="ICT Tools ASM Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STEP 2: Create database tables
run_startup_migrations(engine)
Base.metadata.create_all(bind=engine)

# STEP 3: Include routers AFTER app is created
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(vouchers.router, prefix="/vouchers", tags=["Vouchers"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])

# STEP 4: Test route
@app.get("/")
def root():
    return {"message": "Backend is running successfully"}