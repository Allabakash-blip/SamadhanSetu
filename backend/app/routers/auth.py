from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database.connection import get_db
from app.models.user import User, UserRole, AccountStatus, CitizenProfile, UniversityProfile, IndustryProfile, GovernmentProfile
from app.schemas.auth import RegisterRequest, LoginRequest, GoogleLoginRequest, CompleteProfileRequest
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.services.google_auth import verify_google_credential
from app.services.cloudinary_service import upload_profile_picture

router = APIRouter(prefix="/auth", tags=["Authentication"])
ALLOWED_ROLES = {r.value for r in UserRole}

def user_dict(user: User):
    return {
        "id": user.id, "name": user.name, "email": user.email, "phone": user.phone,
        "profile_picture_url": user.profile_picture_url,
        "role": user.role.value if user.role else None,
        "account_status": user.account_status.value,
    }

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    role = payload.role.upper()
    if role not in ALLOWED_ROLES or role == "ADMIN":
        raise HTTPException(400, "Invalid registration role")
    if db.query(User).filter(User.email == payload.email.lower()).first():
        raise HTTPException(409, "Email already registered")
    if payload.phone and db.query(User).filter(User.phone == payload.phone).first():
        raise HTTPException(409, "Phone number already registered")
    account_status = AccountStatus.ACTIVE if role == "CITIZEN" else AccountStatus.PENDING
    user = User(
        name=payload.name.strip(), email=payload.email.lower(), phone=payload.phone,
        password_hash=hash_password(payload.password), role=UserRole(role), account_status=account_status
    )
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_access_token(user), "token_type": "bearer", "user": user_dict(user)}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    if user.account_status == AccountStatus.SUSPENDED:
        raise HTTPException(403, "Account is suspended")
    return {"access_token": create_access_token(user), "token_type": "bearer", "user": user_dict(user)}

@router.post("/google")
def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    info = verify_google_credential(payload.credential)
    google_id = info.get("sub")
    email = info.get("email", "").lower()
    name = info.get("name") or email.split("@")[0]
    picture = info.get("picture")
    if not google_id or not email:
        raise HTTPException(400, "Google did not provide required account information")
    user = db.query(User).filter(or_(User.google_id == google_id, User.email == email)).first()
    if not user:
        user = User(name=name, email=email, google_id=google_id, profile_picture_url=picture,
                    account_status=AccountStatus.INCOMPLETE)
        db.add(user); db.commit(); db.refresh(user)
    else:
        if not user.google_id: user.google_id = google_id
        if picture and not user.profile_picture_url: user.profile_picture_url = picture
        db.commit(); db.refresh(user)
    return {"access_token": create_access_token(user), "token_type": "bearer", "user": user_dict(user)}

@router.post("/profile-picture")
async def profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(400, "Only JPG, PNG or WEBP images are supported")
    url = await upload_profile_picture(file)
    current_user.profile_picture_url = url
    db.commit()
    return {"profile_picture_url": url}

@router.post("/complete-profile")
def complete_profile(
    payload: CompleteProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    role = payload.role.upper()
    if role not in ALLOWED_ROLES or role == "ADMIN":
        raise HTTPException(400, "Invalid role")
    if current_user.role and current_user.role != UserRole(role):
        raise HTTPException(400, "Role cannot be changed after registration")
    current_user.role = UserRole(role)
    if payload.phone: current_user.phone = payload.phone

    if role == "CITIZEN":
        profile = current_user.citizen_profile or CitizenProfile(user_id=current_user.id)
        for f in ["address_line","state_id","district_id","block_id","village_id","pincode","latitude","longitude"]:
            setattr(profile, f, getattr(payload, f))
        db.add(profile); current_user.account_status = AccountStatus.ACTIVE

    elif role == "UNIVERSITY":
        if not payload.university_name: raise HTTPException(400, "University name is required")
        profile = current_user.university_profile or UniversityProfile(user_id=current_user.id, university_name=payload.university_name)
        profile.university_name = payload.university_name
        profile.university_type = payload.university_type
        profile.registration_number = payload.registration_number
        profile.department = payload.department
        profile.designation = payload.designation
        profile.address = payload.address_line
        profile.state_id = payload.state_id
        profile.district_id = payload.district_id
        profile.city = payload.city
        profile.expertise = payload.expertise
        db.add(profile); current_user.account_status = AccountStatus.PENDING

    elif role == "INDUSTRY":
        if not payload.company_name: raise HTTPException(400, "Company name is required")
        profile = current_user.industry_profile or IndustryProfile(user_id=current_user.id, company_name=payload.company_name)
        profile.company_name = payload.company_name
        profile.company_type = payload.company_type
        profile.website = payload.website
        profile.address = payload.address_line
        profile.state_id = payload.state_id
        profile.district_id = payload.district_id
        profile.city = payload.city
        profile.expertise = payload.expertise
        profile.available_support = payload.available_support
        db.add(profile); current_user.account_status = AccountStatus.PENDING

    elif role == "GOVERNMENT":
        if not payload.government_department: raise HTTPException(400, "Government department is required")
        profile = current_user.government_profile or GovernmentProfile(user_id=current_user.id, department=payload.government_department)
        profile.department = payload.government_department
        profile.designation = payload.designation
        profile.official_id = payload.official_id
        profile.state_id = payload.state_id
        profile.district_id = payload.district_id
        db.add(profile); current_user.account_status = AccountStatus.PENDING

    db.commit(); db.refresh(current_user)
    return {"message": "Profile completed", "user": user_dict(current_user)}

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return user_dict(current_user)
