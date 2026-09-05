import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import get_db
from app.core.security import require_roles
from app.models.user import User, UserRole, State, District, Block, Village
from app.models.problem import Problem, ProblemMedia, ProblemStatus, ProblemPriority
from app.schemas.problem import ProblemResponse
from app.services.cloudinary_service import upload_problem_media

router = APIRouter(prefix="/problems", tags=["Problems"])


def _optional_int(value):
    if value in (None, "", "null"):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Location IDs must be valid integers.")


def _validate_location(db, state_id, district_id, block_id, village_id):
    state = db.get(State, state_id) if state_id else None
    district = db.get(District, district_id) if district_id else None
    block = db.get(Block, block_id) if block_id else None
    village = db.get(Village, village_id) if village_id else None

    if district and state_id and district.state_id != state_id:
        raise HTTPException(status_code=400, detail="District does not belong to the selected state.")
    if block and district_id and block.district_id != district_id:
        raise HTTPException(status_code=400, detail="Block does not belong to the selected district.")
    if village and block_id and village.block_id != block_id:
        raise HTTPException(status_code=400, detail="Village does not belong to the selected block.")
    if state_id and not state:
        raise HTTPException(status_code=400, detail="Selected state was not found.")
    if district_id and not district:
        raise HTTPException(status_code=400, detail="Selected district was not found.")
    if block_id and not block:
        raise HTTPException(status_code=400, detail="Selected block was not found.")
    if village_id and not village:
        raise HTTPException(status_code=400, detail="Selected village was not found.")


@router.post("", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
async def create_problem(
    problem_data: str = Form(...),
    images: list[UploadFile] = File(default=[]),
    videos: list[UploadFile] = File(default=[]),
    current_user: User = Depends(require_roles(UserRole.CITIZEN)),
    db: Session = Depends(get_db),
):
    try:
        data = json.loads(problem_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid problem data JSON.")

    title = str(data.get("title") or "").strip()
    description = str(data.get("description") or "").strip()
    category = str(data.get("category") or "").strip()

    if not title:
        raise HTTPException(status_code=400, detail="Problem title is required.")
    if not description:
        raise HTTPException(status_code=400, detail="Problem description is required.")
    if not category:
        raise HTTPException(status_code=400, detail="Problem category is required.")

    state_id = _optional_int(data.get("state_id"))
    district_id = _optional_int(data.get("district_id"))
    block_id = _optional_int(data.get("block_id"))
    village_id = _optional_int(data.get("village_id"))
    _validate_location(db, state_id, district_id, block_id, village_id)

    problem = Problem(
        user_id=current_user.id,
        title=title,
        description=description,
        category=category,
        state_id=state_id,
        district_id=district_id,
        block_id=block_id,
        village_id=village_id,
        address=data.get("address"),
        pincode=data.get("pincode"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        affected_people=data.get("affected_people"),
        additional_details=data.get("additional_details"),
        status=ProblemStatus.SUBMITTED,
        priority=ProblemPriority.MEDIUM,
    )

    db.add(problem)
    db.commit()
    db.refresh(problem)

    try:
        for image in images:
            if image and image.filename:
                result = await upload_problem_media(image, "image")
                db.add(ProblemMedia(problem_id=problem.id, media_type="IMAGE", url=result["url"], public_id=result["public_id"], original_filename=image.filename))

        for video in videos:
            if video and video.filename:
                result = await upload_problem_media(video, "video")
                db.add(ProblemMedia(problem_id=problem.id, media_type="VIDEO", url=result["url"], public_id=result["public_id"], original_filename=video.filename))

        db.commit()
        db.refresh(problem)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=502, detail=f"Media upload failed: {exc}")

    return problem


@router.get("/mine", response_model=list[ProblemResponse])
def my_problems(current_user: User = Depends(require_roles(UserRole.CITIZEN)), db: Session = Depends(get_db)):
    return db.query(Problem).filter(Problem.user_id == current_user.id).order_by(Problem.created_at.desc()).all()


@router.get("/{problem_id}", response_model=ProblemResponse)
def get_my_problem(problem_id: int, current_user: User = Depends(require_roles(UserRole.CITIZEN)), db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id, Problem.user_id == current_user.id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found.")
    return problem
