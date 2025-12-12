print("🎉 MAIN.PY IS RUNNING")

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import time

# ---------------------------
# Initialize App
# ---------------------------
app = FastAPI(title="Agentic Lead System")

# ---------------------------
# CORS (MUST come before routers)
# ---------------------------
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow all frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# IMPORT ROUTES AFTER CORS
# ---------------------------
from app.core.database import Base, engine
from app.api.routes import router as public_routes
from app.api.internal_routes import router as internal_routes

# REGISTER ROUTES (once)
app.include_router(public_routes)
app.include_router(internal_routes)

# ---------------------------
# Health Check Route
# ---------------------------
@app.get("/")
def home():
    return {"message": "Backend is running!"}

# ---------------------------
# MySQL Wait
# ---------------------------
def wait_for_mysql():
    from app.core.database import DATABASE_URL
    if "sqlite" in DATABASE_URL:
        print("⚡ Using SQLite, skipping MySQL wait...")
        return True

    print("⏳ Waiting for MySQL to be ready...")
    retries = 20

    while retries > 0:
        try:
            with engine.connect() as conn:
                print("✅ MySQL is ready!")
                return True
        except OperationalError:
            retries -= 1
            print("❌ MySQL not ready, retrying in 3 seconds...")
            time.sleep(3)

    print("❌ Could not connect to MySQL")
    return False

# ---------------------------
# Startup Event
# ---------------------------
@app.on_event("startup")
def startup_event():
    if wait_for_mysql():
        print("🛠 Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully.")
    else:
        raise Exception("Database not ready - startup failed")
