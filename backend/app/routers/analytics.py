from collections import Counter
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.problem import (
    Problem, ProblemStatus, ProblemPriority, Solution, SolutionStatus
)
from app.models.industry_partnership import IndustrySupportOffer, IndustryPartnership, PartnershipStatus

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Administrator access required.")
    return current_user


@router.get("/overview")
def analytics_overview(
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db),
):
    problems = db.query(Problem).all()
    solutions = db.query(Solution).all()
    industry_offers = db.query(IndustrySupportOffer).all()
    industry_partnerships = db.query(IndustryPartnership).all()

    status_counts = Counter((p.status.value if p.status else "UNKNOWN") for p in problems)
    priority_counts = Counter((p.priority.value if p.priority else "UNKNOWN") for p in problems)
    category_counts = Counter((p.category or "Uncategorized") for p in problems)

    # Aggregate affected people without making missing values look like zero impact.
    affected_people_reported = sum(p.affected_people or 0 for p in problems)

    solution_status_counts = Counter(
        (s.status.value if s.status else "UNKNOWN") for s in solutions
    )
    industry_support_type_counts = Counter(
        (o.support_type.value if o.support_type else "UNKNOWN") for o in industry_offers
    )

    implemented_problem_ids = {
        s.problem_id
        for s in solutions
        if s.status in {SolutionStatus.IMPLEMENTED, SolutionStatus.VERIFIED}
    }

    verified_solution_count = sum(
        1 for s in solutions if s.status == SolutionStatus.VERIFIED
    )
    approved_solution_count = sum(
        1 for s in solutions
        if s.status in {
            SolutionStatus.APPROVED,
            SolutionStatus.IMPLEMENTATION_STARTED,
            SolutionStatus.IMPLEMENTED,
            SolutionStatus.VERIFIED,
        }
    )

    # Last 6 calendar months, including the current month.
    now = datetime.utcnow()
    months = []
    year, month = now.year, now.month
    for offset in range(5, -1, -1):
        m = month - offset
        y = year
        while m <= 0:
            m += 12
            y -= 1
        months.append((y, m))

    monthly = []
    for y, m in months:
        if m == 12:
            next_start = datetime(y + 1, 1, 1)
        else:
            next_start = datetime(y, m + 1, 1)
        start = datetime(y, m, 1)
        count = sum(1 for p in problems if start <= p.created_at < next_start)
        monthly.append({
            "month": start.strftime("%b %Y"),
            "count": count,
        })

    return {
        "generated_at": now.isoformat(),
        "totals": {
            "problems": len(problems),
            "open_problems": sum(
                1 for p in problems
                if p.status not in {ProblemStatus.CLOSED, ProblemStatus.REJECTED}
            ),
            "resolved_problems": sum(
                1 for p in problems if p.status == ProblemStatus.CLOSED
            ),
            "rejected_problems": sum(
                1 for p in problems if p.status == ProblemStatus.REJECTED
            ),
            "affected_people_reported": affected_people_reported,
            "solutions": len(solutions),
            "approved_solutions": approved_solution_count,
            "verified_solutions": verified_solution_count,
            "problems_with_implemented_solution": len(implemented_problem_ids),
            "industry_offers": len(industry_offers),
            "active_industry_partnerships": sum(1 for p in industry_partnerships if p.status == PartnershipStatus.ACTIVE),
            "completed_industry_partnerships": sum(1 for p in industry_partnerships if p.status == PartnershipStatus.COMPLETED),
            "industry_partners": len({p.industry_id for p in industry_partnerships}),
        },
        "status_counts": dict(status_counts),
        "priority_counts": dict(priority_counts),
        "category_counts": dict(category_counts.most_common()),
        "solution_status_counts": dict(solution_status_counts),
        "industry_support_type_counts": dict(industry_support_type_counts),
        "monthly_problem_trend": monthly,
    }
