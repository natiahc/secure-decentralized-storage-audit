# Decentralized File Storage System with Data Sovereignty and Auditability

## 📌 Project Overview

This project implements a **decentralized file storage system** designed to address key challenges in modern cloud computing:

* **Data sovereignty**
* **Auditability**
* **Decentralized storage**
* **Fault tolerance**

In traditional cloud systems, data is centrally stored, making it difficult to ensure:

* where data resides
* who accessed it
* whether it has been tampered with

This system solves these issues by distributing file storage across multiple independent nodes using a **Distributed Hash Table (DHT)** and adding **cryptographic audit mechanisms**.

---

## 🎯 Objectives

* Eliminate centralized storage dependency
* Enable **jurisdiction-aware data placement**
* Provide **tamper-evident audit logs**
* Ensure **data integrity using Merkle trees**
* Simulate **real-world compliance requirements (GDPR, HIPAA)**

---

## 🏗️ System Architecture

The system follows a distributed architecture:

```
Frontend (Dashboard UI)
        ↓
Gateway (Client API)
        ↓
----------------------------------
|        |         |              |
Node1   Node2     Node3       ... Nodes
(IN)     (EU)      (US)
```

### Components:

* **Frontend**

  * User interface for upload/download
  * Displays node distribution and audit logs

* **Gateway**

  * Entry point for client requests
  * Splits files into chunks
  * Coordinates upload/download

* **Nodes (Peers)**

  * Store file chunks
  * Maintain audit logs
  * Participate in DHT routing

* **Network Layer**

  * Node discovery (`registry`)
  * Metadata distribution (`gossip`)

---

## ⚙️ Core Technologies

* Python
* FastAPI
* Docker & Docker Compose
* REST APIs
* SHA-256 hashing
* Distributed Hash Table (DHT)

---

## 🔑 Key Features

### 1. Decentralized Storage

* Files are split into chunks
* Each chunk is stored on different nodes
* No single node has the entire file

---

### 2. Distributed Hash Table (DHT)

* Determines which node stores each chunk
* Uses consistent hashing
* No central coordinator required

---

### 3. Data Sovereignty (Jurisdiction Awareness)

* Nodes represent different regions (IN, EU, US)
* Data can be restricted to a specific region

Example:

```
Store only in EU → complies with GDPR-like policy
```

---

### 4. Distributed Metadata (Gossip Protocol)

* File metadata is NOT stored centrally
* Replicated across nodes using gossip
* Enables decentralized lookup

---

### 5. Audit Logging (Hash Chain)

* Each node maintains a tamper-evident log
* Logs include:

  * chunk storage
  * data access
* Uses hash chaining for integrity

---

### 6. Data Integrity (Merkle Tree)

* Each file has a Merkle root
* During download:

  * file is reconstructed
  * integrity is verified
* Detects any tampering

---

### 7. Fault Tolerance

* Data is distributed across nodes
* System continues to work even if one node fails

---

## 📁 Project Structure

```
decentralized-storage-dht/
│
├── README.md
├── docker-compose.yml
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│
├── gateway/                          # lightweight entry point (NOT central brain)
│   ├── api.py                        # upload/download interface
│   ├── client.py                     # internal coordinator logic
│   ├── requirements.txt
│   ├── Dockerfile
│
├── node/                             # peer node (same image for all nodes)
│   ├── node.py                       # main storage node server
│   ├── storage.py                    # chunk storage handler
│   ├── dht.py                        # routing logic (simplified Kademlia-style)
│   ├── audit.py                      # local audit log
│   ├── jurisdiction.py               # region simulation (EU/US/IN)
│   ├── config.py
│   ├── requirements.txt
│   ├── Dockerfile
│
├── shared/
│   ├── hashing.py                    # SHA256 utilities
│   ├── chunker.py                    # file splitting logic
│   ├── models.py                     # request/response structures
│
├── network/
│   ├── registry.py                   # node discovery (bootstrap list)
│   ├── gossip.py                     # optional peer sharing simulation
│
```

---

## 🚀 Setup and Installation

### Prerequisites

* Docker
* Docker Compose

---

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd decentralized-storage-dht
```

---

### Step 2: Run System

```bash
docker-compose up --build
```

---

### Step 3: Open Frontend

Open in browser:

```
frontend/index.html
```

---

### Step 4: API Documentation

```
http://localhost:8000/docs
```

---

## 🧪 How to Use (Demo)

### 1. Upload File

* Select file
* Click Upload
* System:

  * splits file
  * distributes chunks across nodes
  * returns file ID

---

### 2. View Node Distribution

* Click “Refresh Status”
* See which node stores which chunks

---

### 3. View Audit Logs

* Click “Load Logs”
* See storage and access logs per node

---

### 4. Download File

* Enter file ID
* System reconstructs file from distributed chunks

---

### 5. Fault Tolerance Test

* Stop a node:

```bash
docker stop node2
```

* Try download again

---

## 🧠 How It Works

### Upload Flow

1. File is split into chunks
2. Each chunk is hashed (SHA-256)
3. DHT determines target node
4. Chunk is stored on responsible node
5. Metadata is distributed via gossip

---

### Download Flow

1. Metadata is retrieved from nodes
2. Chunks are fetched from distributed nodes
3. File is reconstructed
4. Merkle tree verifies integrity

---

## 📊 Example Output

### Node Status

```json
[
  {"node_id": "node1", "region": "IN", "stored_chunks": ["a1", "b2"]},
  {"node_id": "node2", "region": "EU", "stored_chunks": ["c3"]},
  {"node_id": "node3", "region": "US", "stored_chunks": ["d4"]}
]
```

---

### Audit Log

```json
{
  "event": "STORE",
  "details": "chunk=a1 stored_at=node1",
  "prev_hash": "...",
  "hash": "..."
}
```

---

## ⚠️ Limitations

* Metadata consistency is eventual (gossip-based)
* No encryption implemented (can be added)
* Simplified DHT (not full Kademlia)
* No consensus protocol (e.g., Raft)

---

## 🔮 Future Enhancements

* End-to-end encryption
* Full Kademlia DHT
* Blockchain-based audit ledger
* Smart policy engine (GDPR enforcement)
* Real-time network visualization

---

## 🎓 Conclusion

This project demonstrates a **decentralized, compliance-aware storage system** that:

* removes reliance on centralized cloud providers
* ensures transparency and traceability
* supports regulatory requirements
* provides secure and fault-tolerant storage

---
