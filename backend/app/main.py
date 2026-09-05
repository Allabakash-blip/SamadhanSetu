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

    # Lightweight compatibility migrations for existing MySQL installations.
    # SQLAlchemy create_all() creates new tables but does not alter existing
    # columns/enums, so these checks keep upgraded local databases working.
    with engine.begin() as connection:
        try:
            connection.execute(text("""
                ALTER TABLE users
                MODIFY COLUMN role ENUM(
                    'CITIZEN','UNIVERSITY','INDUSTRY','GOVERNMENT',
                    'COMMUNITY_GROUP','PRI','ULB','ADMIN'
                ) NULL
            """))
        except Exception:
            pass

        try:
            connection.execute(text("""
                ALTER TABLE problems
                ADD COLUMN reporter_type VARCHAR(40) NOT NULL DEFAULT 'INDIVIDUAL_CITIZEN'
            """))
        except Exception:
            pass

        try:
            connection.execute(text("""
                CREATE INDEX ix_problems_reporter_type ON problems (reporter_type)
            """))
        except Exception:
            pass

        # Existing challenges remain individual-citizen challenges unless
        # their user account explicitly maps to an institutional submitter.
        try:
            connection.execute(text("""
                UPDATE problems p
                JOIN users u ON u.id = p.user_id
                SET p.reporter_type = CASE u.role
                    WHEN 'COMMUNITY_GROUP' THEN 'COMMUNITY_GROUP'
                    WHEN 'PRI' THEN 'PRI'
                    WHEN 'ULB' THEN 'ULB'
                    WHEN 'GOVERNMENT' THEN 'GOVERNMENT_DEPARTMENT'
                    ELSE 'INDIVIDUAL_CITIZEN'
                END
            """))
        except Exception:
            pass

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
