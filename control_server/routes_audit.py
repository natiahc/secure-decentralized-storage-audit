from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import AuditLog, FileMetadata, User
from auth import get_current_user

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/file/{file_id}")
def get_file_audit_logs(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can view audit logs")

    logs = (
        db.query(AuditLog)
        .filter(AuditLog.file_id == file.id)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    result = []
    for log in logs:
        result.append({
            "audit_id": str(log.id),
            "user_id": str(log.user_id) if log.user_id else None,
            "file_id": str(log.file_id) if log.file_id else None,
            "action": log.action,
            "node_id": log.node_id,
            "timestamp": log.timestamp,
            "success": log.success,
            "reason": log.reason,
            "ip_address": log.ip_address,
        })

    return {
        "file_id": str(file.id),
        "filename": file.filename,
        "audit_logs": result,
    }


@router.get("/me")
def get_my_audit_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.user_id == current_user.id)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    result = []
    for log in logs:
        result.append({
            "audit_id": str(log.id),
            "file_id": str(log.file_id) if log.file_id else None,
            "action": log.action,
            "node_id": log.node_id,
            "timestamp": log.timestamp,
            "success": log.success,
            "reason": log.reason,
            "ip_address": log.ip_address,
        })

    return {
        "user_id": str(current_user.id),
        "username": current_user.username,
        "activity": result,
    }
