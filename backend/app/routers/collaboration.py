import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.database.connection import get_db
from app.core.security import require_roles
from app.models.user import (
    User, UserRole, AccountStatus,
)
from app.models.problem import (
    Problem, ProblemStatus, ProblemPriority,
    ProblemAssignment, ProblemStatusHistory,
    ProblemComment, Notification,
    Solution, SolutionMedia, SolutionFeedback, ImplementationUpdate, SolutionStatus,
)
from app.services.cloudinary_service import upload_problem_media
from app.schemas.collaboration import (
    AssignProblemRequest, AdminProblemUpdateRequest,
    RepresentativeStatusRequest, CommentRequest,
    SolutionCreateRequest, SolutionFeedbackRequest, ImplementationUpdateRequest,
)

router = APIRouter(tags=["Problem Collaboration"])


ORGANIZATION_ROLES = {
    UserRole.UNIVERSITY,
    UserRole.INDUSTRY,
    UserRole.GOVERNMENT,
}


def verification_status(user: User):
    if user.role == UserRole.UNIVERSITY and user.university_profile:
        return user.university_profile.verification_status
    if user.role == UserRole.INDUSTRY and user.industry_profile:
        return user.industry_profile.verification_status
    if user.role == UserRole.GOVERNMENT and user.government_profile:
        return user.government_profile.verification_status
    return None


def organization_name(user: User):
    if user.role == UserRole.UNIVERSITY and user.university_profile:
        return user.university_profile.university_name
    if user.role == UserRole.INDUSTRY and user.industry_profile:
        return user.industry_profile.company_name
    if user.role == UserRole.GOVERNMENT and user.government_profile:
        return user.government_profile.department
    return None


def designation(user: User):
    if user.role == UserRole.UNIVERSITY and user.university_profile:
        return user.university_profile.designation
    if user.role == UserRole.INDUSTRY and user.industry_profile:
        return None
    if user.role == UserRole.GOVERNMENT and user.government_profile:
        return user.government_profile.designation
    return None


def user_summary(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value if user.role else None,
        "phone": user.phone,
        "profile_picture_url": user.profile_picture_url,
        "organization": organization_name(user),
        "designation": designation(user),
    }


def problem_summary(problem: Problem):
    assignment = problem.assignment
    return {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "category": problem.category,
        "status": problem.status.value if hasattr(problem.status, "value") else str(problem.status),
        "priority": problem.priority.value if hasattr(problem.priority, "value") else str(problem.priority),
        "created_at": problem.created_at,
        "reporter": user_summary(problem.user),
        "assignment": {
            "id": assignment.id,
            "assignee": user_summary(assignment.assignee),
            "assigned_by": user_summary(assignment.assigned_by),
            "organization_role": assignment.organization_role,
            "remarks": assignment.remarks,
            "assigned_at": assignment.assigned_at,
        } if assignment else None,
    }


def solution_payload(solution: Solution):
    return {
        "id": solution.id,
        "problem_id": solution.problem_id,
        "title": solution.title,
        "description": solution.description,
        "benefits": solution.benefits,
        "estimated_cost": solution.estimated_cost,
        "required_resources": solution.required_resources,
        "implementation_time": solution.implementation_time,
        "status": solution.status.value if hasattr(solution.status, "value") else str(solution.status),
        "proposer": user_summary(solution.proposer),
        "created_at": solution.created_at,
        "updated_at": solution.updated_at,
        "media": [
            {"id": m.id, "media_type": m.media_type, "url": m.url, "original_filename": m.original_filename}
            for m in solution.media
        ],
        "feedback": [
            {
                "id": f.id, "feedback": f.feedback, "decision": f.decision,
                "user": user_summary(f.user), "created_at": f.created_at
            } for f in solution.feedback
        ],
        "implementation_updates": [
            {
                "id": u.id, "status": u.status, "note": u.note,
                "user": user_summary(u.user), "created_at": u.created_at
            } for u in solution.implementation_updates
        ],
    }


def problem_detail(problem: Problem):
    result = problem_summary(problem)
    result.update({
        "state_id": problem.state_id,
        "district_id": problem.district_id,
        "block_id": problem.block_id,
        "village_id": problem.village_id,
        "address": problem.address,
        "pincode": problem.pincode,
        "latitude": problem.latitude,
        "longitude": problem.longitude,
        "affected_people": problem.affected_people,
        "additional_details": problem.additional_details,
        "media": [
            {
                "id": m.id,
                "media_type": m.media_type,
                "url": m.url,
                "original_filename": m.original_filename,
            }
            for m in problem.media
        ],
        "timeline": [
            {
                "id": h.id,
                "status": h.status,
                "note": h.note,
                "changed_by": user_summary(h.changed_by),
                "created_at": h.created_at,
            }
            for h in problem.status_history
        ],
        "comments": [
            {
                "id": c.id,
                "comment": c.comment,
                "user": user_summary(c.user),
                "created_at": c.created_at,
            }
            for c in problem.comments
        ],
        "solutions": [solution_payload(s) for s in problem.solutions],
    })
    return result


def notify(db, user_id, title, message, problem_id=None):
    db.add(Notification(
        user_id=user_id,
        title=title,
        message=message,
        problem_id=problem_id,
        is_read=0,
    ))


def record_status(db, problem, status, user, note=None):
    db.add(ProblemStatusHistory(
        problem_id=problem.id,
        status=status,
        note=note,
        changed_by_id=user.id,
    ))


def load_problem(db, problem_id):
    return db.query(Problem).options(
        joinedload(Problem.user),
        joinedload(Problem.media),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.university_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.industry_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.government_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assigned_by),
        joinedload(Problem.status_history).joinedload(ProblemStatusHistory.changed_by),
        joinedload(Problem.comments).joinedload(ProblemComment.user),
    ).filter(Problem.id == problem_id).first()


@router.get("/admin/problems")
def admin_problems(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    problems = db.query(Problem).options(
        joinedload(Problem.user),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.university_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.industry_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.government_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assigned_by),
    ).order_by(Problem.created_at.desc()).all()
    return [problem_summary(p) for p in problems]


@router.get("/admin/problems/{problem_id}")
def admin_problem_detail(
    problem_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    return problem_detail(problem)


@router.get("/admin/problem-representatives")
def approved_representatives(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    users = db.query(User).filter(
        User.role.in_(list(ORGANIZATION_ROLES)),
        User.account_status == AccountStatus.ACTIVE,
    ).all()
    return [
        user_summary(u) for u in users
        if verification_status(u) == "APPROVED"
    ]


@router.put("/admin/problems/{problem_id}/assign")
def assign_problem(
    problem_id: int,
    payload: AssignProblemRequest,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")

    assignee = db.get(User, payload.assignee_id)
    if not assignee or assignee.role not in ORGANIZATION_ROLES:
        raise HTTPException(400, "Select a university, industry or government representative.")
    if assignee.account_status != AccountStatus.ACTIVE or verification_status(assignee) != "APPROVED":
        raise HTTPException(400, "The selected representative is not verified and active.")

    if problem.assignment:
        problem.assignment.assignee_id = assignee.id
        problem.assignment.assigned_by_id = current_user.id
        problem.assignment.organization_role = assignee.role.value
        problem.assignment.remarks = payload.remarks
    else:
        problem.assignment = ProblemAssignment(
            assignee_id=assignee.id,
            assigned_by_id=current_user.id,
            organization_role=assignee.role.value,
            remarks=payload.remarks,
        )

    problem.status = ProblemStatus.ASSIGNED
    record_status(db, problem, ProblemStatus.ASSIGNED.value, current_user, payload.remarks)
    notify(
        db, assignee.id, "New Problem Assigned",
        f'Problem #{problem.id} "{problem.title}" has been assigned to you.',
        problem.id,
    )
    notify(
        db, problem.user_id, "Problem Assigned",
        f'Your problem "{problem.title}" has been assigned to {organization_name(assignee) or assignee.role.value}.',
        problem.id,
    )
    db.commit()
    return problem_detail(load_problem(db, problem_id))


@router.put("/admin/problems/{problem_id}/update")
def admin_update_problem(
    problem_id: int,
    payload: AdminProblemUpdateRequest,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")

    if payload.priority:
        try:
            problem.priority = ProblemPriority(payload.priority.upper())
        except ValueError:
            raise HTTPException(400, "Invalid priority")

    if payload.status:
        try:
            new_status = ProblemStatus(payload.status.upper())
        except ValueError:
            raise HTTPException(400, "Invalid problem status")
        problem.status = new_status
        record_status(db, problem, new_status.value, current_user, payload.note)
        notify(db, problem.user_id, "Problem Status Updated",
               f'Your problem "{problem.title}" is now {new_status.value.replace("_", " ")}.',
               problem.id)
        if problem.assignment:
            notify(db, problem.assignment.assignee_id, "Problem Status Updated",
                   f'Problem #{problem.id} "{problem.title}" is now {new_status.value.replace("_", " ")}.',
                   problem.id)

    db.commit()
    return problem_detail(load_problem(db, problem_id))


@router.get("/representative/problems")
def representative_problems(
    current_user: User = Depends(require_roles(
        UserRole.UNIVERSITY, UserRole.INDUSTRY, UserRole.GOVERNMENT
    )),
    db: Session = Depends(get_db),
):
    if current_user.account_status != AccountStatus.ACTIVE or verification_status(current_user) != "APPROVED":
        raise HTTPException(403, "Your organization account must be approved before accessing assigned problems.")

    problems = db.query(Problem).join(ProblemAssignment).filter(
        ProblemAssignment.assignee_id == current_user.id
    ).options(
        joinedload(Problem.user),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.university_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.industry_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assignee).joinedload(User.government_profile),
        joinedload(Problem.assignment).joinedload(ProblemAssignment.assigned_by),
    ).order_by(Problem.updated_at.desc()).all()
    return [problem_summary(p) for p in problems]


@router.get("/representative/problems/{problem_id}")
def representative_problem_detail(
    problem_id: int,
    current_user: User = Depends(require_roles(
        UserRole.UNIVERSITY, UserRole.INDUSTRY, UserRole.GOVERNMENT
    )),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem or not problem.assignment or problem.assignment.assignee_id != current_user.id:
        raise HTTPException(404, "Assigned problem not found")
    return problem_detail(problem)


@router.put("/representative/problems/{problem_id}/status")
def representative_update_status(
    problem_id: int,
    payload: RepresentativeStatusRequest,
    current_user: User = Depends(require_roles(
        UserRole.UNIVERSITY, UserRole.INDUSTRY, UserRole.GOVERNMENT
    )),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem or not problem.assignment or problem.assignment.assignee_id != current_user.id:
        raise HTTPException(404, "Assigned problem not found")
    if current_user.account_status != AccountStatus.ACTIVE or verification_status(current_user) != "APPROVED":
        raise HTTPException(403, "Your organization account must be approved.")

    allowed = {
        ProblemStatus.IN_PROGRESS,
        ProblemStatus.SOLUTION_PROPOSED,
        ProblemStatus.PILOT,
        ProblemStatus.IMPLEMENTED,
        ProblemStatus.CLOSED,
    }
    try:
        new_status = ProblemStatus(payload.status.upper())
    except ValueError:
        raise HTTPException(400, "Invalid status")
    if new_status not in allowed:
        raise HTTPException(400, "Representatives can update only active workflow statuses.")

    problem.status = new_status
    record_status(db, problem, new_status.value, current_user, payload.note)
    notify(db, problem.user_id, "Problem Progress Updated",
           f'Your problem "{problem.title}" is now {new_status.value.replace("_", " ")}.',
           problem.id)
    db.commit()
    return problem_detail(load_problem(db, problem_id))


@router.post("/collaboration/problems/{problem_id}/comments")
def add_comment(
    problem_id: int,
    payload: CommentRequest,
    current_user: User = Depends(require_roles(
        UserRole.CITIZEN, UserRole.UNIVERSITY, UserRole.INDUSTRY,
        UserRole.GOVERNMENT, UserRole.ADMIN
    )),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")

    if current_user.role == UserRole.CITIZEN and problem.user_id != current_user.id:
        raise HTTPException(403, "You can comment only on your own problems.")
    if current_user.role in ORGANIZATION_ROLES:
        if not problem.assignment or problem.assignment.assignee_id != current_user.id:
            raise HTTPException(403, "You can comment only on problems assigned to you.")

    comment = ProblemComment(
        problem_id=problem.id,
        user_id=current_user.id,
        comment=payload.comment.strip(),
    )
    db.add(comment)

    recipients = {problem.user_id}
    if problem.assignment:
        recipients.add(problem.assignment.assignee_id)
    if current_user.role == UserRole.ADMIN:
        recipients.discard(problem.user_id)
    for uid in recipients:
        if uid != current_user.id:
            notify(db, uid, "New Problem Comment",
                   f'{current_user.name} commented on problem #{problem.id}.',
                   problem.id)

    db.commit()
    return {
        "id": comment.id,
        "message": "Comment added successfully.",
    }


@router.get("/collaboration/problems/{problem_id}/comments")
def get_comments(
    problem_id: int,
    current_user: User = Depends(require_roles(
        UserRole.CITIZEN, UserRole.UNIVERSITY, UserRole.INDUSTRY,
        UserRole.GOVERNMENT, UserRole.ADMIN
    )),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    if current_user.role == UserRole.CITIZEN and problem.user_id != current_user.id:
        raise HTTPException(403, "Access denied")
    if current_user.role in ORGANIZATION_ROLES and (not problem.assignment or problem.assignment.assignee_id != current_user.id):
        raise HTTPException(403, "Access denied")
    return [
        {"id": c.id, "comment": c.comment, "user": user_summary(c.user), "created_at": c.created_at}
        for c in problem.comments
    ]


@router.get("/citizen/problems/{problem_id}/collaboration")
def citizen_collaboration(
    problem_id: int,
    current_user: User = Depends(require_roles(UserRole.CITIZEN)),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem or problem.user_id != current_user.id:
        raise HTTPException(404, "Problem not found")
    return {
        "assignment": problem_detail(problem)["assignment"],
        "timeline": problem_detail(problem)["timeline"],
        "comments": problem_detail(problem)["comments"],
    }


@router.get("/notifications")
def notifications(
    current_user: User = Depends(require_roles(
        UserRole.CITIZEN, UserRole.UNIVERSITY, UserRole.INDUSTRY,
        UserRole.GOVERNMENT, UserRole.ADMIN
    )),
    db: Session = Depends(get_db),
):
    items = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).limit(100).all()
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "problem_id": n.problem_id,
            "is_read": bool(n.is_read),
            "created_at": n.created_at,
        }
        for n in items
    ]


@router.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(require_roles(
        UserRole.CITIZEN, UserRole.UNIVERSITY, UserRole.INDUSTRY,
        UserRole.GOVERNMENT, UserRole.ADMIN
    )),
    db: Session = Depends(get_db),
):
    n = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id,
    ).first()
    if not n:
        raise HTTPException(404, "Notification not found")
    n.is_read = 1
    db.commit()
    return {"message": "Notification marked as read."}


# ========================= MILESTONE 5 =========================

def load_solution(db, solution_id: int):
    return db.query(Solution).options(
        joinedload(Solution.proposer),
        joinedload(Solution.media),
        joinedload(Solution.feedback).joinedload(SolutionFeedback.user),
        joinedload(Solution.implementation_updates).joinedload(ImplementationUpdate.user),
    ).filter(Solution.id == solution_id).first()


def ensure_assignee(problem, current_user):
    return (
        problem.assignment is not None
        and problem.assignment.assignee_id == current_user.id
        and current_user.account_status == AccountStatus.ACTIVE
        and verification_status(current_user) == "APPROVED"
    )


@router.post("/representative/problems/{problem_id}/solutions")
async def create_solution(
    problem_id: int,
    solution_data: str = Form(...),
    images: list[UploadFile] = File(default=[]),
    videos: list[UploadFile] = File(default=[]),
    current_user: User = Depends(require_roles(
        UserRole.UNIVERSITY, UserRole.INDUSTRY, UserRole.GOVERNMENT
    )),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem or not ensure_assignee(problem, current_user):
        raise HTTPException(403, "Only the verified representative assigned to this problem can propose a solution.")
    try:
        data = json.loads(solution_data)
        payload = SolutionCreateRequest(**data)
    except Exception as exc:
        raise HTTPException(400, f"Invalid solution data: {exc}")

    solution = Solution(
        problem_id=problem.id,
        proposer_id=current_user.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        benefits=payload.benefits,
        estimated_cost=payload.estimated_cost,
        required_resources=payload.required_resources,
        implementation_time=payload.implementation_time,
        status=SolutionStatus.PROPOSED,
    )
    db.add(solution)
    db.flush()

    try:
        for image in images:
            if image and image.filename:
                result = await upload_problem_media(image, "image")
                db.add(SolutionMedia(solution_id=solution.id, media_type="IMAGE",
                                     url=result["url"], public_id=result["public_id"],
                                     original_filename=image.filename))
        for video in videos:
            if video and video.filename:
                result = await upload_problem_media(video, "video")
                db.add(SolutionMedia(solution_id=solution.id, media_type="VIDEO",
                                     url=result["url"], public_id=result["public_id"],
                                     original_filename=video.filename))
    except Exception as exc:
        db.rollback()
        raise HTTPException(502, f"Solution media upload failed: {exc}")

    problem.status = ProblemStatus.SOLUTION_PROPOSED
    record_status(db, problem, ProblemStatus.SOLUTION_PROPOSED.value, current_user,
                  f"Solution proposed: {solution.title}")
    notify(db, problem.user_id, "New Solution Proposed",
           f'{current_user.name} proposed a solution for "{problem.title}".', problem.id)
    db.commit()
    db.refresh(solution)
    return solution_payload(load_solution(db, solution.id))


@router.get("/problems/{problem_id}/solutions")
def list_solutions(
    problem_id: int,
    current_user: User = Depends(require_roles(
        UserRole.CITIZEN, UserRole.UNIVERSITY, UserRole.INDUSTRY,
        UserRole.GOVERNMENT, UserRole.ADMIN
    )),
    db: Session = Depends(get_db),
):
    problem = load_problem(db, problem_id)
    if not problem:
        raise HTTPException(404, "Problem not found")
    if current_user.role == UserRole.CITIZEN and problem.user_id != current_user.id:
        raise HTTPException(403, "Access denied")
    if current_user.role in ORGANIZATION_ROLES and (not problem.assignment or problem.assignment.assignee_id != current_user.id):
        raise HTTPException(403, "Access denied")
    return [solution_payload(s) for s in problem.solutions]


@router.post("/solutions/{solution_id}/feedback")
def solution_feedback(
    solution_id: int,
    payload: SolutionFeedbackRequest,
    current_user: User = Depends(require_roles(UserRole.CITIZEN)),
    db: Session = Depends(get_db),
):
    solution = load_solution(db, solution_id)
    if not solution or solution.problem.user_id != current_user.id:
        raise HTTPException(404, "Solution not found")
    decision = payload.decision.upper().strip()
    if decision not in {"APPROVE", "CHANGES_REQUESTED", "REJECT"}:
        raise HTTPException(400, "Decision must be APPROVE, CHANGES_REQUESTED or REJECT")

    solution.feedback.append(SolutionFeedback(
        user_id=current_user.id, feedback=payload.feedback.strip(), decision=decision
    ))
    if decision == "APPROVE":
        solution.status = SolutionStatus.APPROVED
        solution.problem.status = ProblemStatus.PILOT
        record_status(db, solution.problem, ProblemStatus.PILOT.value, current_user, "Citizen approved the proposed solution.")
    elif decision == "CHANGES_REQUESTED":
        solution.status = SolutionStatus.CHANGES_REQUESTED
    else:
        solution.status = SolutionStatus.REJECTED

    notify(db, solution.proposer_id, "Solution Feedback",
           f'{current_user.name} marked the solution "{solution.title}" as {decision.replace("_", " ").lower()}.',
           solution.problem_id)
    db.commit()
    return solution_payload(load_solution(db, solution.id))


@router.post("/solutions/{solution_id}/verify")
def verify_solution(
    solution_id: int,
    payload: SolutionFeedbackRequest,
    current_user: User = Depends(require_roles(UserRole.CITIZEN)),
    db: Session = Depends(get_db),
):
    """Citizen confirms that an implemented solution has delivered the intended outcome."""
    solution = load_solution(db, solution_id)
    if not solution or solution.problem.user_id != current_user.id:
        raise HTTPException(404, "Solution not found")
    if solution.status != SolutionStatus.IMPLEMENTED:
        raise HTTPException(400, "Only an implemented solution can be verified.")
    if not payload.feedback.strip():
        raise HTTPException(400, "Verification comments are required.")

    solution.feedback.append(SolutionFeedback(
        user_id=current_user.id,
        feedback=payload.feedback.strip(),
        decision="VERIFY",
    ))
    solution.status = SolutionStatus.VERIFIED
    solution.problem.status = ProblemStatus.CLOSED
    record_status(
        db, solution.problem, ProblemStatus.CLOSED.value, current_user,
        "Citizen verified the implemented solution and confirmed the impact."
    )
    notify(
        db, solution.proposer_id, "Solution Verified",
        f'{current_user.name} verified the implemented solution "{solution.title}".',
        solution.problem_id,
    )
    db.commit()
    return solution_payload(load_solution(db, solution.id))


@router.post("/solutions/{solution_id}/implementation-updates")
def add_implementation_update(
    solution_id: int,
    payload: ImplementationUpdateRequest,
    current_user: User = Depends(require_roles(
        UserRole.UNIVERSITY, UserRole.INDUSTRY, UserRole.GOVERNMENT
    )),
    db: Session = Depends(get_db),
):
    solution = load_solution(db, solution_id)
    if not solution or not ensure_assignee(solution.problem, current_user):
        raise HTTPException(403, "Only the assigned verified representative can update implementation.")
    new_status = payload.status.upper().strip()
    allowed = {
        "IMPLEMENTATION_STARTED", "IMPLEMENTATION_IN_PROGRESS",
        "IMPLEMENTED", "VERIFIED"
    }
    if new_status not in allowed:
        raise HTTPException(400, f"Status must be one of: {', '.join(sorted(allowed))}")

    solution.implementation_updates.append(ImplementationUpdate(
        user_id=current_user.id, status=new_status, note=payload.note.strip()
    ))
    if new_status == "IMPLEMENTATION_STARTED":
        solution.status = SolutionStatus.IMPLEMENTATION_STARTED
        solution.problem.status = ProblemStatus.IN_PROGRESS
    elif new_status == "IMPLEMENTATION_IN_PROGRESS":
        solution.status = SolutionStatus.IMPLEMENTATION_STARTED
        solution.problem.status = ProblemStatus.PILOT
    elif new_status == "IMPLEMENTED":
        solution.status = SolutionStatus.IMPLEMENTED
        solution.problem.status = ProblemStatus.IMPLEMENTED
    elif new_status == "VERIFIED":
        solution.status = SolutionStatus.VERIFIED
        solution.problem.status = ProblemStatus.CLOSED

    record_status(db, solution.problem, solution.problem.status.value, current_user, payload.note)
    notify(db, solution.problem.user_id, "Implementation Update",
           f'Implementation for "{solution.title}" is now {new_status.replace("_", " ").lower()}.',
           solution.problem_id)
    db.commit()
    return solution_payload(load_solution(db, solution.id))
