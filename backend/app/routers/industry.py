from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_db
from app.core.security import require_roles
from app.models.user import User, UserRole, AccountStatus
from app.models.problem import Problem, ProblemStatus, ProblemAssignment, Solution, SolutionStatus, ImplementationUpdate
from app.models.industry_partnership import (
    IndustrySupportOffer, IndustryPartnership, SupportType, OfferStatus, PartnershipStatus
)
from app.models.problem import Notification
from app.schemas.industry import SupportOfferCreateRequest, IndustryPartnershipStatusRequest, IndustryImplementationUpdateRequest

router = APIRouter(prefix="/industry", tags=["Industry Partnership"])


def ensure_industry(current_user: User):
    if current_user.role != UserRole.INDUSTRY or current_user.account_status != AccountStatus.ACTIVE:
        raise HTTPException(403, "Your industry account must be active.")
    if not current_user.industry_profile or current_user.industry_profile.verification_status != "APPROVED":
        raise HTTPException(403, "Your industry account must be administrator-approved.")


def company_name(user):
    return user.industry_profile.company_name if user and user.industry_profile else user.name if user else "Industry"


def user_payload(user):
    return {
        "id": user.id, "name": user.name, "email": user.email,
        "role": user.role.value if user.role else None,
        "organization": company_name(user),
    }


def offer_payload(offer, db):
    industry = db.get(User, offer.industry_id)
    problem = db.get(Problem, offer.problem_id)
    return {
        "id": offer.id, "problem_id": offer.problem_id,
        "problem_title": problem.title if problem else "Unknown problem",
        "problem_category": problem.category if problem else None,
        "support_type": offer.support_type.value, "title": offer.title,
        "description": offer.description, "amount": offer.amount, "duration": offer.duration,
        "status": offer.status.value, "industry": user_payload(industry),
        "created_at": offer.created_at, "updated_at": offer.updated_at,
    }


def partnership_payload(partnership, db):
    industry = db.get(User, partnership.industry_id)
    problem = db.get(Problem, partnership.problem_id)
    return {
        "id": partnership.id, "problem_id": partnership.problem_id,
        "problem_title": problem.title if problem else "Unknown problem",
        "problem_category": problem.category if problem else None,
        "support_type": partnership.support_type.value,
        "scope": partnership.scope, "status": partnership.status.value,
        "industry": user_payload(industry), "offer_id": partnership.offer_id,
        "started_at": partnership.started_at, "completed_at": partnership.completed_at,
    }


def problem_payload(problem, existing_offer=None):
    assignment = problem.assignment
    return {
        "id": problem.id, "title": problem.title, "description": problem.description,
        "category": problem.category, "status": problem.status.value,
        "priority": problem.priority.value, "affected_people": problem.affected_people,
        "address": problem.address, "created_at": problem.created_at,
        "assignment": {
            "organization_role": assignment.organization_role,
            "assignee_id": assignment.assignee_id,
        } if assignment else None,
        "existing_offer": {"id": existing_offer.id, "status": existing_offer.status.value} if existing_offer else None,
        "partnerships": [],
    }


def notify(db, user_id, title, message, problem_id):
    db.add(Notification(user_id=user_id, title=title, message=message, problem_id=problem_id, is_read=0))


@router.get("/projects")
def available_projects(
    current_user: User = Depends(require_roles(UserRole.INDUSTRY)),
    db: Session = Depends(get_db),
):
    ensure_industry(current_user)
    eligible = {
        ProblemStatus.VALIDATED, ProblemStatus.ASSIGNED, ProblemStatus.IN_PROGRESS,
        ProblemStatus.SOLUTION_PROPOSED, ProblemStatus.PILOT, ProblemStatus.IMPLEMENTED,
    }
    problems = db.query(Problem).filter(Problem.status.in_(list(eligible))).options(
        joinedload(Problem.assignment)
    ).order_by(Problem.created_at.desc()).all()
    result = []
    for problem in problems:
        offer = db.query(IndustrySupportOffer).filter(
            IndustrySupportOffer.problem_id == problem.id,
            IndustrySupportOffer.industry_id == current_user.id,
            IndustrySupportOffer.status.in_([OfferStatus.PROPOSED, OfferStatus.ACCEPTED]),
        ).order_by(IndustrySupportOffer.created_at.desc()).first()
        if offer and offer.status == OfferStatus.ACCEPTED:
            continue
        item = problem_payload(problem)
        item["offer_status"] = offer.status.value if offer else None
        result.append(item)
    return result


@router.get("/projects/{problem_id}")
def project_detail(
    problem_id: int,
    current_user: User = Depends(require_roles(UserRole.INDUSTRY)),
    db: Session = Depends(get_db),
):
    ensure_industry(current_user)
    problem = db.query(Problem).options(joinedload(Problem.assignment)).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(404, "Project not found")
    offer = db.query(IndustrySupportOffer).filter(
        IndustrySupportOffer.problem_id == problem.id, IndustrySupportOffer.industry_id == current_user.id
    ).order_by(IndustrySupportOffer.created_at.desc()).first()
    item = problem_payload(problem, offer)
    partnerships = db.query(IndustryPartnership).filter(IndustryPartnership.problem_id == problem.id).all()
    item["partnerships"] = [partnership_payload(x, db) for x in partnerships]
    if offer:
        item["existing_offer"] = offer_payload(offer, db)
    return item


@router.post("/projects/{problem_id}/offers")
def create_support_offer(
    problem_id: int,
    payload: SupportOfferCreateRequest,
    current_user: User = Depends(require_roles(UserRole.INDUSTRY)),
    db: Session = Depends(get_db),
):
    ensure_industry(current_user)
    problem = db.get(Problem, problem_id)
    if not problem or problem.status in {ProblemStatus.REJECTED, ProblemStatus.CLOSED}:
        raise HTTPException(400, "This project is not open for industry support.")
    try:
        support_type = SupportType(payload.support_type.upper())
    except ValueError:
        raise HTTPException(400, "Invalid support type.")
    existing = db.query(IndustrySupportOffer).filter(
        IndustrySupportOffer.problem_id == problem_id,
        IndustrySupportOffer.industry_id == current_user.id,
        IndustrySupportOffer.status == OfferStatus.PROPOSED,
    ).first()
    if existing:
        raise HTTPException(400, "You already have a pending support offer for this project.")
    offer = IndustrySupportOffer(
        problem_id=problem_id, industry_id=current_user.id, support_type=support_type,
        title=payload.title.strip(), description=payload.description.strip(),
        amount=payload.amount, duration=payload.duration, status=OfferStatus.PROPOSED,
    )
    db.add(offer)
    db.flush()
    notify(db, problem.user_id, "Industry Support Offer",
           f'{company_name(current_user)} offered {support_type.value.replace("_", " ").lower()} support for your problem "{problem.title}".', problem.id)
    if problem.assignment:
        notify(db, problem.assignment.assignee_id, "Industry Support Offer",
               f'{company_name(current_user)} offered support for problem #{problem.id}.', problem.id)
    db.commit()
    db.refresh(offer)
    return offer_payload(offer, db)


@router.get("/support")
def my_support(
    current_user: User = Depends(require_roles(UserRole.INDUSTRY)),
    db: Session = Depends(get_db),
):
    ensure_industry(current_user)
    offers = db.query(IndustrySupportOffer).filter(IndustrySupportOffer.industry_id == current_user.id).order_by(IndustrySupportOffer.created_at.desc()).all()
    partnerships = db.query(IndustryPartnership).filter(IndustryPartnership.industry_id == current_user.id).order_by(IndustryPartnership.started_at.desc()).all()
    return {
        "offers": [offer_payload(x, db) for x in offers],
        "partnerships": [partnership_payload(x, db) for x in partnerships],
    }


@router.put("/partnerships/{partnership_id}/status")
def update_partnership_status(
    partnership_id: int,
    payload: IndustryPartnershipStatusRequest,
    current_user: User = Depends(require_roles(UserRole.INDUSTRY)),
    db: Session = Depends(get_db),
):
    ensure_industry(current_user)
    partnership = db.query(IndustryPartnership).filter(
        IndustryPartnership.id == partnership_id, IndustryPartnership.industry_id == current_user.id
    ).first()
    if not partnership:
        raise HTTPException(404, "Partnership not found")
    try:
        status = PartnershipStatus(payload.status.upper())
    except ValueError:
        raise HTTPException(400, "Invalid partnership status")
    partnership.status = status
    if status == PartnershipStatus.COMPLETED:
        from datetime import datetime
        partnership.completed_at = datetime.utcnow()
    db.commit()
    return partnership_payload(partnership, db)


@router.get("/partnerships/{partnership_id}/implementation")
def partnership_implementation(
    partnership_id: int,
    current_user: User = Depends(require_roles(UserRole.INDUSTRY)),
    db: Session = Depends(get_db),
):
    """Return implementation progress for an active industry partnership."""
    ensure_industry(current_user)
    partnership = db.query(IndustryPartnership).filter(
        IndustryPartnership.id == partnership_id,
        IndustryPartnership.industry_id == current_user.id,
    ).first()
    if not partnership:
        raise HTTPException(404, "Partnership not found")

    solution = db.query(Solution).filter(
        Solution.problem_id == partnership.problem_id,
        Solution.status.in_([
            SolutionStatus.APPROVED,
            SolutionStatus.IMPLEMENTATION_STARTED,
            SolutionStatus.IMPLEMENTED,
            SolutionStatus.VERIFIED,
        ]),
    ).order_by(Solution.created_at.desc()).first()

    updates = []
    if solution:
        updates = [
            {"id": u.id, "status": u.status, "note": u.note, "user_id": u.user_id, "created_at": u.created_at}
            for u in solution.implementation_updates
        ]

    return {
        "partnership": partnership_payload(partnership, db),
        "solution": {
            "id": solution.id,
            "title": solution.title,
            "status": solution.status.value,
        } if solution else None,
        "updates": updates,
    }


@router.post("/partnerships/{partnership_id}/implementation-updates")
def add_partnership_implementation_update(
    partnership_id: int,
    payload: IndustryImplementationUpdateRequest,
    current_user: User = Depends(require_roles(UserRole.INDUSTRY)),
    db: Session = Depends(get_db),
):
    """Let an active industry partner contribute implementation progress to the approved solution."""
    ensure_industry(current_user)
    partnership = db.query(IndustryPartnership).filter(
        IndustryPartnership.id == partnership_id,
        IndustryPartnership.industry_id == current_user.id,
        IndustryPartnership.status == PartnershipStatus.ACTIVE,
    ).first()
    if not partnership:
        raise HTTPException(404, "Active partnership not found")

    solution = db.query(Solution).filter(
        Solution.problem_id == partnership.problem_id,
        Solution.status.in_([
            SolutionStatus.APPROVED,
            SolutionStatus.IMPLEMENTATION_STARTED,
            SolutionStatus.IMPLEMENTED,
        ]),
    ).order_by(Solution.created_at.desc()).first()
    if not solution:
        raise HTTPException(400, "An approved solution is required before industry implementation updates can be added.")

    status = payload.status.upper().strip()
    allowed = {"IMPLEMENTATION_STARTED", "IMPLEMENTATION_IN_PROGRESS", "IMPLEMENTED"}
    if status not in allowed:
        raise HTTPException(400, "Status must be IMPLEMENTATION_STARTED, IMPLEMENTATION_IN_PROGRESS or IMPLEMENTED.")

    note = payload.note.strip()
    db.add(ImplementationUpdate(solution_id=solution.id, user_id=current_user.id, status=status, note=note))

    if status == "IMPLEMENTATION_STARTED":
        solution.status = SolutionStatus.IMPLEMENTATION_STARTED
        partnership.problem.status = ProblemStatus.IN_PROGRESS
    elif status == "IMPLEMENTATION_IN_PROGRESS":
        solution.status = SolutionStatus.IMPLEMENTATION_STARTED
        partnership.problem.status = ProblemStatus.PILOT
    else:
        solution.status = SolutionStatus.IMPLEMENTED
        partnership.problem.status = ProblemStatus.IMPLEMENTED

    record = __import__("app.routers.collaboration", fromlist=["record_status"]).record_status
    record(db, partnership.problem, partnership.problem.status.value, current_user, note)

    notify(db, partnership.problem.user_id, "Industry Implementation Update",
           f'{company_name(current_user)} updated implementation for "{partnership.problem.title}" to {status.replace("_", " ").lower()}.',
           partnership.problem.id)

    if partnership.problem.assignment and partnership.problem.assignment.assignee_id != current_user.id:
        notify(db, partnership.problem.assignment.assignee_id, "Industry Implementation Update",
               f'Industry partner {company_name(current_user)} updated implementation for "{partnership.problem.title}".',
               partnership.problem.id)

    db.commit()
    return {
        "message": "Implementation update saved.",
        "partnership": partnership_payload(partnership, db),
        "solution": {"id": solution.id, "title": solution.title, "status": solution.status.value},
    }


@router.get("/admin/offers")
def admin_industry_offers(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    offers = db.query(IndustrySupportOffer).order_by(IndustrySupportOffer.created_at.desc()).all()
    return [offer_payload(x, db) for x in offers]


@router.put("/admin/offers/{offer_id}/{action}")
def admin_decide_offer(
    offer_id: int,
    action: str,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    offer = db.get(IndustrySupportOffer, offer_id)
    if not offer:
        raise HTTPException(404, "Support offer not found")
    if action not in {"accept", "reject"}:
        raise HTTPException(400, "Action must be accept or reject")
    if offer.status != OfferStatus.PROPOSED:
        raise HTTPException(400, "Only pending support offers can be decided.")
    problem = db.get(Problem, offer.problem_id)
    industry = db.get(User, offer.industry_id)
    if action == "reject":
        offer.status = OfferStatus.REJECTED
        notify(db, offer.industry_id, "Support Offer Rejected", f'Your industry support offer for "{problem.title}" was not accepted.', problem.id)
    else:
        offer.status = OfferStatus.ACCEPTED
        existing = db.query(IndustryPartnership).filter(
            IndustryPartnership.problem_id == offer.problem_id,
            IndustryPartnership.industry_id == offer.industry_id,
            IndustryPartnership.status == PartnershipStatus.ACTIVE,
        ).first()
        if not existing:
            partnership = IndustryPartnership(
                problem_id=offer.problem_id, industry_id=offer.industry_id, offer_id=offer.id,
                support_type=offer.support_type, scope=offer.description, status=PartnershipStatus.ACTIVE,
            )
            db.add(partnership)
        notify(db, offer.industry_id, "Industry Partnership Approved", f'Your support offer for "{problem.title}" has been approved and an active partnership was created.', problem.id)
        notify(db, problem.user_id, "Industry Partnership Started", f'{company_name(industry)} is now supporting your problem "{problem.title}".', problem.id)
        if problem.assignment:
            notify(db, problem.assignment.assignee_id, "Industry Partnership Started", f'{company_name(industry)} is now supporting problem #{problem.id}.', problem.id)
    db.commit()
    return offer_payload(offer, db)


@router.get("/admin/partnerships")
def admin_partnerships(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    partnerships = db.query(IndustryPartnership).order_by(IndustryPartnership.created_at.desc()).all()
    return [partnership_payload(x, db) for x in partnerships]
