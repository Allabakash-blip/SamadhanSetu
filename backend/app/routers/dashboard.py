from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole, AccountStatus
from app.models.problem import Problem, ProblemStatus, ProblemAssignment

router = APIRouter(prefix="/dashboard", tags=["Dashboards"])

@router.get("/summary")
def dashboard_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    counts = {
        "total_users": db.query(User).count(),
        "citizens": db.query(User).filter(User.role == UserRole.CITIZEN).count(),
        "universities": db.query(User).filter(User.role == UserRole.UNIVERSITY).count(),
        "industries": db.query(User).filter(User.role == UserRole.INDUSTRY).count(),
        "government_users": db.query(User).filter(User.role == UserRole.GOVERNMENT).count(),
        "pending_accounts": db.query(User).filter(User.account_status == AccountStatus.PENDING).count(),
    }

    # Citizen-specific dashboard metrics. These are scoped to the authenticated
    # citizen so one user's reports cannot affect another user's dashboard.
    if current_user.role == UserRole.CITIZEN:
        citizen_problems = db.query(Problem).filter(Problem.user_id == current_user.id)
        counts.update({
            "my_problems": citizen_problems.count(),
            "under_review": citizen_problems.filter(
                Problem.status == ProblemStatus.UNDER_REVIEW
            ).count(),
            "in_progress": citizen_problems.filter(
                Problem.status == ProblemStatus.IN_PROGRESS
            ).count(),
            "resolved": citizen_problems.filter(
                Problem.status == ProblemStatus.CLOSED
            ).count(),
        })

    # University representative dashboard metrics.  These must be scoped to
    # the authenticated university representative's actual assignments.
    # Previously the dashboard only populated citizen/admin/government/industry
    # counts, so university cards fell back to zero even when the representative
    # had assigned challenges visible on /representative/problems.
    if current_user.role == UserRole.UNIVERSITY:
        assigned_problems = (
            db.query(Problem)
            .join(ProblemAssignment, ProblemAssignment.problem_id == Problem.id)
            .filter(ProblemAssignment.assignee_id == current_user.id)
        )
        active_problems = assigned_problems.filter(
            Problem.status.notin_([ProblemStatus.CLOSED, ProblemStatus.REJECTED])
        )
        completed_problems = assigned_problems.filter(
            Problem.status == ProblemStatus.CLOSED
        )
        counts.update({
            "assigned_challenges": assigned_problems.count(),
            "active_projects": active_problems.count(),
            # Team management is not represented by a team table/model in the
            # current schema, so keep this explicitly zero until teams are added.
            "teams": 0,
            "completed": completed_problems.count(),
        })
    return {
        "user": {"id":current_user.id,"name":current_user.name,
                 "role":current_user.role.value if current_user.role else None,
                 "account_status":current_user.account_status.value},
        "counts": counts,
    }
