from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from database import Base


# ------------------------
# User
# ------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


# ------------------------
# Storage Node
# ------------------------
class StorageNode(Base):
    __tablename__ = "storage_nodes"

    id = Column(String, primary_key=True)  # node-1, node-2
    name = Column(String)
    region = Column(String)  # india, eu, us
    url = Column(String)

    is_active = Column(Boolean, default=True)


# ------------------------
# File Metadata
# ------------------------
class FileMetadata(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    filename = Column(String)
    size = Column(Integer)
    checksum = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    owner = relationship("User")


# ------------------------
# File Chunk Mapping
# ------------------------
class FileChunk(Base):
    __tablename__ = "file_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"))

    chunk_index = Column(Integer)
    node_id = Column(String, ForeignKey("storage_nodes.id"))
    object_path = Column(String)

    file = relationship("FileMetadata")
    node = relationship("StorageNode")


# ------------------------
# Access Policy
# ------------------------
class AccessPolicy(Base):
    __tablename__ = "policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    can_read = Column(Boolean, default=False)
    can_write = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)

    valid_from = Column(DateTime, default=datetime.utcnow)
    valid_to = Column(DateTime, nullable=True)

    file = relationship("FileMetadata")
    user = relationship("User")


# ------------------------
# Audit Log
# ------------------------
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True))
    file_id = Column(UUID(as_uuid=True))

    action = Column(String)  # upload, read, delete, denied
    node_id = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean)
    reason = Column(String)

    ip_address = Column(String)
