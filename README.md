# Secure Decentralized File Storage with Access Auditing

## 📌 Overview

This project implements a **secure decentralized file storage system** with **policy-based access control** and **comprehensive audit logging**.

In decentralized environments, file data may reside across multiple storage nodes, making it difficult to:
- enforce access control
- track data location (data sovereignty)
- provide auditability for compliance (GDPR, HIPAA)

This system addresses these challenges by separating:
- **Data Plane (Decentralized Storage)**
- **Control Plane (Centralized Metadata + Policy + Audit)**

---

## 🎯 Objectives

- Store encrypted file data across multiple storage nodes
- Maintain metadata separately from file content
- Enforce policy-based access control
- Track all access via audit logs
- Support region-aware storage (data sovereignty)

---

## 🏗️ Architecture

### 🔹 Control Plane (Centralized)

Responsible for:
- Authentication (JWT)
- User management
- File metadata
- Access policies
- Audit logging
- Storage node registry

Tech:
- FastAPI
- PostgreSQL
- SQLAlchemy

---

### 🔹 Data Plane (Decentralized)

Responsible for:
- Storing encrypted file blobs
- File retrieval
- File deletion

Each storage node runs independently.

---

### 🔹 Client / API User

- Uploads file metadata
- Uploads encrypted file to storage node
- Requests access
- Receives storage location

---

## 🧠 Key Design Principle

> File data is decentralized, while metadata, policy, and audit are centralized.

This ensures:
- scalability
- compliance
- strong access control
- full traceability

---
## 🗂️ Folder Structure

```plaintext
secure-decentralized-storage-audit/
├── docker-compose.yml
│
├── control_server/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── audit.py
│   ├── routes_auth.py
│   ├── routes_nodes.py
│   ├── routes_files.py
│   ├── routes_policy.py
│   ├── routes_audit.py
│   └── routes_access.py
│
├── storage_node/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
```

## 🧩 Database Schema

### Tables

- **users** → user accounts
- **storage_nodes** → node registry (region, URL)
- **files** → file metadata
- **file_chunks** → mapping file → node
- **policies** → access control rules
- **audit_logs** → access and operation logs

---

## 🔐 Security Model

- Passwords hashed using **bcrypt**
- Authentication via **JWT tokens**
- File data stored as **encrypted blobs**
- Access controlled using **policy rules**
- All operations recorded in **audit logs**

---

## 📊 Features

### ✅ Implemented

- User registration & login
- JWT authentication
- Storage node registration
- File metadata management
- Region-aware node selection
- Access policy creation & update
- File access control (owner + shared users)
- Audit logging (success + denied)
- Multi-node decentralized storage

---

## 🚀 How to Run

### 1. Clone repo

```bash
git clone <your-repo-link>
cd secure-decentralized-storage-audit
```

### Start System
``` bash
docker-compose up --build
```

### Services

| Service        | URL                                            |
| -------------- | ---------------------------------------------- |
| Control Server | [http://localhost:8000](http://localhost:8000) |
| Storage Node 1 | [http://localhost:8001](http://localhost:8001) |
| Storage Node 2 | [http://localhost:8002](http://localhost:8002) |
| Storage Node 3 | [http://localhost:8003](http://localhost:8003) |

## API Usage
### Register User
``` bash
curl -X POST http://localhost:8000/auth/register \
-H "Content-Type: application/json" \
-d '{"username":"alice","password":"alice123"}'
```

### Login
``` bash
curl -X POST http://localhost:8000/auth/login \
-H "Content-Type: application/json" \
-d '{"username":"alice","password":"alice123"}'
```

### Register Storage Node
``` bash
curl -X POST http://localhost:8000/nodes/register \
-H "Content-Type: application/json" \
-d '{
  "id": "node-1",
  "name": "storage-node-1",
  "region": "india",
  "url": "http://storage_node_1:8000"
}'
```

### Create File Metadata
``` bash
curl -X POST "http://localhost:8000/files/metadata" \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"filename":"file.enc","size":100,"checksum":"abc123"}'
```

### Create Policy (Shared file)
``` bash
curl -X POST http://localhost:8000/policies \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "file_id":"<FILE_ID>",
  "user_id":"<USER_ID>",
  "can_read":true
}'
```

### Access File
``` bash
curl -X GET http://localhost:8000/access/file/<FILE_ID> \
-H "Authorization: Bearer <TOKEN>"
```

### View Audit Logs
``` bash
curl -X GET http://localhost:8000/audit/file/<FILE_ID> \
-H "Authorization: Bearer <TOKEN>"
```

## 🔄 Example Flows

- User registers and logs in  
- Storage nodes are registered  
- User creates file metadata  
- File is assigned to a node  
- Owner shares file via policy  
- Another user requests access  
- Access is allowed/denied  
- Audit log is recorded  


## 🏗️ Decentralization Model

This system follows a **hybrid decentralized architecture**:

- **File data** → decentralized across storage nodes  
- **Metadata & policies** → centralized control plane  

### Benefits

- Scalability  
- Strong governance  
- Auditability  
- Regulatory compliance  
