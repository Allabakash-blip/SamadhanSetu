from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import require_roles
from app.models.user import User, UserRole
from app.models.problem import Problem
from app.services.ai_matching import classify_problem, find_matches

router = APIRouter(prefix="/ai", tags=["AI Classification & Matching"])


def admin_only(current_user: User = Depends(require_roles(UserRole.ADMIN))):
    return current_user


@router.post("/problems/{problem_id}/classify")
def classify_problem_endpoint(
    problem_id: int,
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db),
):
    problem = db.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found.")

    return {
        "problem_id": problem.id,
        "analysis": classify_problem(problem),
    }


@router.get("/problems/{problem_id}/matches")
def problem_matches(
    problem_id: int,
    limit: int = 5,
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db),
):
    problem = db.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found.")

    limit = max(1, min(limit, 10))
    analysis = classify_problem(problem)
    return {
        "problem_id": problem.id,
        "analysis": analysis,
        "matches": find_matches(db, problem, analysis, limit),
    }


@router.get("/problems/{problem_id}/recommendations")
def recommendations(
    problem_id: int,
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db),
):
    problem = db.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found.")

    analysis = classify_problem(problem)
    return {
        "problem_id": problem.id,
        "classification": analysis,
        "recommended_representatives": find_matches(db, problem, analysis, 5),
    }
