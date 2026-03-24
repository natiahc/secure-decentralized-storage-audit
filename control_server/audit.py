from sqlalchemy.orm import Session
from typing import Optional
from models import AuditLog


def write_audit_log(
    db: Session,
    user_id,
    file_id,
    action: str,
    node_id: Optional[str] = None,
    success: bool = True,
    reason: Optional[str] = None,
    ip_address: Optional[str] = None,
):
    log = AuditLog(
        user_id=user_id,
        file_id=file_id,
        action=action,
        node_id=node_id,
        success=success,
        reason=reason,
        ip_address=ip_address,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log
