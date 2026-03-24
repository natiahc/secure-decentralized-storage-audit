from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from models import AccessPolicy, FileMetadata, User
from schemas import PolicyCreate
from auth import get_current_user
from audit import write_audit_log

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("/")
def create_policy(
    policy: PolicyCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ------------------------
    # Validate file
    # ------------------------
    file = db.query(FileMetadata).filter(FileMetadata.id == policy.file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can create policy")

    # ------------------------
    # Validate target user
    # ------------------------
    target_user = db.query(User).filter(User.id == policy.user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    # ------------------------
    # Check existing policy
    # ------------------------
    existing = (
        db.query(AccessPolicy)
        .filter(
            AccessPolicy.file_id == policy.file_id,
            AccessPolicy.user_id == policy.user_id,
        )
        .first()
    )

    # ------------------------
    # Update existing policy
    # ------------------------
    if existing:
        existing.can_read = policy.can_read
        existing.can_write = policy.can_write
        existing.can_delete = policy.can_delete
        existing.valid_to = policy.valid_to

        db.commit()
        db.refresh(existing)

        # Audit log
        write_audit_log(
            db=db,
            user_id=current_user.id,
            file_id=file.id,
            action="update_policy",
            node_id=None,
            success=True,
            reason=f"Policy updated for user {target_user.username}",
            ip_address=request.client.host if request.client else None,
        )

        return {
            "message": "Policy updated",
            "policy_id": str(existing.id),
        }

    # ------------------------
    # Create new policy
    # ------------------------
    new_policy = AccessPolicy(
        file_id=policy.file_id,
        user_id=policy.user_id,
        can_read=policy.can_read,
        can_write=policy.can_write,
        can_delete=policy.can_delete,
        valid_to=policy.valid_to,
    )

    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    # Audit log
    write_audit_log(
        db=db,
        user_id=current_user.id,
        file_id=file.id,
        action="create_policy",
        node_id=None,
        success=True,
        reason=f"Policy created for user {target_user.username}",
        ip_address=request.client.host if request.client else None,
    )

    return {
        "message": "Policy created",
        "policy_id": str(new_policy.id),
    }


@router.get("/{file_id}")
def list_file_policies(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can view policies")

    policies = db.query(AccessPolicy).filter(AccessPolicy.file_id == file.id).all()

    result = []
    for p in policies:
        user = db.query(User).filter(User.id == p.user_id).first()

        result.append({
            "policy_id": str(p.id),
            "user_id": str(p.user_id),
            "username": user.username if user else None,
            "can_read": p.can_read,
            "can_write": p.can_write,
            "can_delete": p.can_delete,
            "valid_from": p.valid_from,
            "valid_to": p.valid_to,
        })

    return {
        "file_id": str(file.id),
        "filename": file.filename,
        "policies": result,
    }
