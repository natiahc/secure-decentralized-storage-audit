from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import FileMetadata, FileChunk, StorageNode, User
from schemas import FileCreate, FileResponse
from auth import get_current_user

router = APIRouter(prefix="/files", tags=["files"])


def select_storage_node(db: Session, preferred_region: str | None = None):
    if preferred_region:
        node = (
            db.query(StorageNode)
            .filter(
                StorageNode.is_active == True,
                StorageNode.region == preferred_region
            )
            .first()
        )
        if node:
            return node

    node = db.query(StorageNode).filter(StorageNode.is_active == True).first()
    return node


@router.post("/metadata")
def create_file_metadata(
    file: FileCreate,
    region: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    node = select_storage_node(db, region)

    if not node:
        raise HTTPException(status_code=400, detail="No active storage node available")

    new_file = FileMetadata(
        owner_id=current_user.id,
        filename=file.filename,
        size=file.size,
        checksum=file.checksum,
        expires_at=file.expires_at,
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    chunk = FileChunk(
        file_id=new_file.id,
        chunk_index=0,
        node_id=node.id,
        object_path=f"{new_file.id}_chunk_0.enc",
    )

    db.add(chunk)
    db.commit()

    return {
        "file_id": str(new_file.id),
        "filename": new_file.filename,
        "assigned_node": {
            "id": node.id,
            "name": node.name,
            "region": node.region,
            "url": node.url,
        },
        "object_path": chunk.object_path,
    }


@router.get("/", response_model=list[FileResponse])
def list_my_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    files = (
        db.query(FileMetadata)
        .filter(FileMetadata.owner_id == current_user.id)
        .order_by(FileMetadata.created_at.desc())
        .all()
    )
    return files


@router.get("/{file_id}")
def get_file_metadata(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this file")

    chunks = db.query(FileChunk).filter(FileChunk.file_id == file.id).all()

    chunk_details = []
    for chunk in chunks:
        node = db.query(StorageNode).filter(StorageNode.id == chunk.node_id).first()
        chunk_details.append({
            "chunk_index": chunk.chunk_index,
            "node_id": chunk.node_id,
            "node_name": node.name if node else None,
            "node_region": node.region if node else None,
            "node_url": node.url if node else None,
            "object_path": chunk.object_path,
        })

    return {
        "file_id": str(file.id),
        "filename": file.filename,
        "size": file.size,
        "checksum": file.checksum,
        "created_at": file.created_at,
        "expires_at": file.expires_at,
        "chunks": chunk_details,
    }
