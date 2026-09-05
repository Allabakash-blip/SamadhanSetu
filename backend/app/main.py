from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.database.connection import Base, engine
from app.models import *
from app.routers import auth, location, dashboard, admin
from app.routers import problems, collaboration, analytics, ai, industry
app = FastAPI(
    title="SIH Social Innovation Collaboration Portal",
    version="0.1.0",
    description="SIH Social Innovation Collaboration Portal: authentication, profiles, locations, reporting, collaboration, solution implementation and impact analytics."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(location.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(
    problems.router,
    prefix="/api",
)
app.include_router(collaboration.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(industry.router, prefix="/api")
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message":"SIH Social Innovation Portal API is running"}

@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status":"ok","database":"connected"}
    except Exception as exc:
        return {"status":"error","database":"unavailable","detail":str(exc)}
