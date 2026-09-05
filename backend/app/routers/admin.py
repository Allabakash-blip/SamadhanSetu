from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import require_roles
from app.models.user import (
    User,
    UserRole,
    AccountStatus,
    CitizenProfile,
    UniversityProfile,
    IndustryProfile,
    GovernmentProfile,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


def profile_verification_status(user: User):
    if user.role == UserRole.UNIVERSITY and user.university_profile:
        return user.university_profile.verification_status
    if user.role == UserRole.INDUSTRY and user.industry_profile:
        return user.industry_profile.verification_status
    if user.role == UserRole.GOVERNMENT and user.government_profile:
        return user.government_profile.verification_status
    if user.role == UserRole.CITIZEN:
        return "NOT_REQUIRED"
    return None


def user_summary(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "profile_picture_url": user.profile_picture_url,
        "role": user.role.value if user.role else None,
        "account_status": user.account_status.value,
        "verification_status": profile_verification_status(user),
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def user_details(user: User):
    result = user_summary(user)
    result["profile"] = None

    if user.role == UserRole.CITIZEN and user.citizen_profile:
        p = user.citizen_profile
        result["profile"] = {
            "type": "CITIZEN",
            "address_line": p.address_line,
            "state_id": p.state_id,
            "district_id": p.district_id,
            "block_id": p.block_id,
            "village_id": p.village_id,
            "pincode": p.pincode,
            "latitude": p.latitude,
            "longitude": p.longitude,
        }

    elif user.role == UserRole.UNIVERSITY and user.university_profile:
        p = user.university_profile
        result["profile"] = {
            "type": "UNIVERSITY",
            "university_name": p.university_name,
            "university_type": p.university_type,
            "registration_number": p.registration_number,
            "department": p.department,
            "designation": p.designation,
            "address": p.address,
            "state_id": p.state_id,
            "district_id": p.district_id,
            "city": p.city,
            "expertise": p.expertise,
            "verification_status": p.verification_status,
        }

    elif user.role == UserRole.INDUSTRY and user.industry_profile:
        p = user.industry_profile
        result["profile"] = {
            "type": "INDUSTRY",
            "company_name": p.company_name,
            "company_type": p.company_type,
            "website": p.website,
            "address": p.address,
            "state_id": p.state_id,
            "district_id": p.district_id,
            "city": p.city,
            "expertise": p.expertise,
            "available_support": p.available_support,
            "verification_status": p.verification_status,
        }

    elif user.role == UserRole.GOVERNMENT and user.government_profile:
        p = user.government_profile
        result["profile"] = {
            "type": "GOVERNMENT",
            "department": p.department,
            "designation": p.designation,
            "official_id": p.official_id,
            "state_id": p.state_id,
            "district_id": p.district_id,
            "verification_status": p.verification_status,
        }

    return result


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    total_users = db.query(User).count()
    citizens = db.query(User).filter(User.role == UserRole.CITIZEN).count()
    universities = db.query(User).filter(User.role == UserRole.UNIVERSITY).count()
    industries = db.query(User).filter(User.role == UserRole.INDUSTRY).count()
    government = db.query(User).filter(User.role == UserRole.GOVERNMENT).count()

    pending_universities = (
        db.query(User)
        .join(UniversityProfile)
        .filter(User.role == UserRole.UNIVERSITY,
                UniversityProfile.verification_status == "PENDING")
        .count()
    )
    pending_industries = (
        db.query(User)
        .join(IndustryProfile)
        .filter(User.role == UserRole.INDUSTRY,
                IndustryProfile.verification_status == "PENDING")
        .count()
    )
    pending_government = (
        db.query(User)
        .join(GovernmentProfile)
        .filter(User.role == UserRole.GOVERNMENT,
                GovernmentProfile.verification_status == "PENDING")
        .count()
    )

    return {
        "admin": user_summary(current_user),
        "counts": {
            "total_users": total_users,
            "citizens": citizens,
            "universities": universities,
            "industries": industries,
            "government_users": government,
            "pending_universities": pending_universities,
            "pending_industries": pending_industries,
            "pending_government": pending_government,
            "pending_total": pending_universities + pending_industries + pending_government,
        },
    }


@router.get("/verifications/pending")
def pending_verifications(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .filter(User.role.in_([UserRole.UNIVERSITY, UserRole.INDUSTRY, UserRole.GOVERNMENT]))
        .order_by(User.created_at.desc())
        .all()
    )
    return [user_summary(user) for user in users if profile_verification_status(user) == "PENDING"]


@router.get("/users")
def all_users(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [user_summary(user) for user in users]


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_details(user)


def get_verification_profile(user: User):
    if user.role == UserRole.UNIVERSITY:
        return user.university_profile
    if user.role == UserRole.INDUSTRY:
        return user.industry_profile
    if user.role == UserRole.GOVERNMENT:
        return user.government_profile
    return None


@router.put("/users/{user_id}/approve")
def approve_user(
    user_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role in {UserRole.ADMIN, UserRole.CITIZEN}:
        raise HTTPException(status_code=400, detail="This account does not require organization verification.")

    profile = get_verification_profile(user)
    if not profile:
        raise HTTPException(status_code=400, detail="User profile is incomplete.")

    profile.verification_status = "APPROVED"
    user.account_status = AccountStatus.ACTIVE
    db.commit()
    db.refresh(user)

    return {"message": "Account approved successfully.", "user": user_summary(user)}


@router.put("/users/{user_id}/reject")
def reject_user(
    user_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role in {UserRole.ADMIN, UserRole.CITIZEN}:
        raise HTTPException(status_code=400, detail="This account does not use organization verification.")

    profile = get_verification_profile(user)
    if not profile:
        raise HTTPException(status_code=400, detail="User profile is incomplete.")

    profile.verification_status = "REJECTED"
    user.account_status = AccountStatus.PENDING
    db.commit()
    db.refresh(user)

    return {"message": "Account rejected.", "user": user_summary(user)}
