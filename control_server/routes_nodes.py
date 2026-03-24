from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import StorageNode
from schemas import StorageNodeRegister, StorageNodeResponse

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.post("/register", response_model=StorageNodeResponse)
def register_node(node: StorageNodeRegister, db: Session = Depends(get_db)):
    existing = db.query(StorageNode).filter(StorageNode.id == node.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Node already exists")

    new_node = StorageNode(
        id=node.id,
        name=node.name,
        region=node.region,
        url=node.url,
        is_active=True,
    )

    db.add(new_node)
    db.commit()
    db.refresh(new_node)

    return new_node


@router.get("/", response_model=list[StorageNodeResponse])
def list_nodes(db: Session = Depends(get_db)):
    return (
        db.query(StorageNode)
        .filter(StorageNode.is_active == True)
        .order_by(StorageNode.id.asc())
        .all()
    )
