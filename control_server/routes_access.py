from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from auth import get_current_user
from audit import write_audit_log
from database import get_db
from models import AccessPolicy, FileChunk, FileMetadata, StorageNode, User

router = APIRouter(prefix="/access", tags=["access"])


def _is_policy_valid(policy: AccessPolicy) -> bool:
    now = datetime.utcnow()

    if policy.valid_from and policy.valid_from > now:
        return False

    if policy.valid_to and policy.valid_to < now:
        return False

    return True


@router.get("/file/{file_id}")
def access_file(
    file_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    chunks = db.query(FileChunk).filter(FileChunk.file_id == file.id).all()
    if not chunks:
        raise HTTPException(status_code=404, detail="No file chunks found")

    # Owner always has access
    if file.owner_id == current_user.id:
        result_chunks = []
        for chunk in chunks:
            node = db.query(StorageNode).filter(StorageNode.id == chunk.node_id).first()
            result_chunks.append({
                "chunk_index": chunk.chunk_index,
                "node_id": chunk.node_id,
                "node_name": node.name if node else None,
                "node_region": node.region if node else None,
                "node_url": node.url if node else None,
                "object_path": chunk.object_path,
            })

        write_audit_log(
            db=db,
            user_id=current_user.id,
            file_id=file.id,
            action="read_file",
            node_id=chunks[0].node_id if chunks else None,
            success=True,
            reason="Owner access granted",
            ip_address=request.client.host if request.client else None,
        )

        return {
            "message": "Access granted",
            "file_id": str(file.id),
            "filename": file.filename,
            "owner_access": True,
            "chunks": result_chunks,
        }

    # Shared-user policy check
    policy = (
        db.query(AccessPolicy)
        .filter(
            AccessPolicy.file_id == file.id,
            AccessPolicy.user_id == current_user.id,
            AccessPolicy.can_read == True,
        )
        .first()
    )

    if not policy or not _is_policy_valid(policy):
        write_audit_log(
            db=db,
            user_id=current_user.id,
            file_id=file.id,
            action="read_file",
            node_id=chunks[0].node_id if chunks else None,
            success=False,
            reason="Access denied: no valid read policy",
            ip_address=request.client.host if request.client else None,
        )

        raise HTTPException(status_code=403, detail="Read access denied")

    result_chunks = []
    for chunk in chunks:
        node = db.query(StorageNode).filter(StorageNode.id == chunk.node_id).first()
        result_chunks.append({
            "chunk_index": chunk.chunk_index,
            "node_id": chunk.node_id,
            "node_name": node.name if node else None,
            "node_region": node.region if node else None,
            "node_url": node.url if node else None,
            "object_path": chunk.object_path,
        })

    write_audit_log(
        db=db,
        user_id=current_user.id,
        file_id=file.id,
        action="read_file",
        node_id=chunks[0].node_id if chunks else None,
        success=True,
        reason="Shared access granted",
        ip_address=request.client.host if request.client else None,
    )

    return {
        "message": "Access granted",
        "file_id": str(file.id),
        "filename": file.filename,
        "owner_access": False,
        "chunks": result_chunks,
    }
