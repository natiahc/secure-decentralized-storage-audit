from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


# ------------------------
# User Schemas
# ------------------------
class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str

    class Config:
        from_attributes = True


# ------------------------
# Storage Node Schemas
# ------------------------
class StorageNodeRegister(BaseModel):
    id: str
    name: str
    region: str
    url: str


class StorageNodeResponse(BaseModel):
    id: str
    name: str
    region: str
    url: str

    class Config:
        from_attributes = True


# ------------------------
# File Schemas
# ------------------------
class FileCreate(BaseModel):
    filename: str
    size: int
    checksum: str
    expires_at: Optional[datetime] = None


class FileResponse(BaseModel):
    id: uuid.UUID
    filename: str
    size: int
    checksum: str
    created_at: datetime

    class Config:
        from_attributes = True


# ------------------------
# Policy Schemas
# ------------------------
class PolicyCreate(BaseModel):
    file_id: uuid.UUID
    user_id: uuid.UUID
    can_read: bool = False
    can_write: bool = False
    can_delete: bool = False
    valid_to: Optional[datetime] = None


# ------------------------
# Audit Schemas
# ------------------------
class AuditResponse(BaseModel):
    user_id: Optional[uuid.UUID]
    file_id: Optional[uuid.UUID]
    action: str
    timestamp: datetime
    success: bool
    reason: Optional[str]

    class Config:
        from_attributes = True
