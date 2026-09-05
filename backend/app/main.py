from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, inspect

from app.core.config import settings
from app.database.connection import Base, engine
from app.models import *

from app.routers import auth, location, dashboard, admin
from app.routers import problems, collaboration, analytics, ai, industry


app = FastAPI(
    title="SIH Social Innovation Collaboration Portal",
    version="0.1.0",
    description=(
        "SIH Social Innovation Collaboration Portal: "
        "authentication, profiles, locations, reporting, collaboration, "
        "solution implementation and impact analytics."
    )
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


def add_missing_matching_columns():
    """
    Add database columns required by the advanced representative
    matching system when they do not already exist.

    This is intentionally handled here because the project currently
    does not use a separate database migration framework.
    """

    matching_columns = {
        "university_profiles": {
            "availability_status": (
                "VARCHAR(30) NOT NULL DEFAULT 'AVAILABLE'"
            ),
            "relevant_experience": "TEXT NULL",
            "years_of_experience": "INT NULL",
            "latitude": "FLOAT NULL",
            "longitude": "FLOAT NULL",
        },
        "industry_profiles": {
            "availability_status": (
                "VARCHAR(30) NOT NULL DEFAULT 'AVAILABLE'"
            ),
            "relevant_experience": "TEXT NULL",
            "years_of_experience": "INT NULL",
            "latitude": "FLOAT NULL",
            "longitude": "FLOAT NULL",
        },
        "government_profiles": {
            "availability_status": (
                "VARCHAR(30) NOT NULL DEFAULT 'AVAILABLE'"
            ),
            "relevant_experience": "TEXT NULL",
            "years_of_experience": "INT NULL",
            "latitude": "FLOAT NULL",
            "longitude": "FLOAT NULL",
        },
    }

    inspector = inspect(engine)

    with engine.begin() as connection:

        for table_name, columns in matching_columns.items():

            if not inspector.has_table(table_name):
                continue

            existing_columns = {
                column["name"]
                for column in inspector.get_columns(table_name)
            }

            for column_name, column_definition in columns.items():

                if column_name in existing_columns:
                    continue

                sql = (
                    f"ALTER TABLE `{table_name}` "
                    f"ADD COLUMN `{column_name}` "
                    f"{column_definition}"
                )

                connection.execute(text(sql))

                print(
                    f"Added column '{column_name}' "
                    f"to '{table_name}'."
                )


@app.on_event("startup")
def startup():
    # Create any tables that do not already exist.
    Base.metadata.create_all(bind=engine)

    # Add new columns required by Feature 08.
    add_missing_matching_columns()


@app.get("/")
def root():
    return {
        "message": "SIH Social Innovation Portal API is running"
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception as exc:
        return {
            "status": "error",
            "database": "unavailable",
            "detail": str(exc)
        }