from fastapi import FastAPI
from database import Base, engine

# Routers
from routes_auth import router as auth_router
from routes_nodes import router as nodes_router
from routes_files import router as files_router
from routes_policy import router as policy_router
from routes_audit import router as audit_router
from routes_access import router as access_router


app = FastAPI(
    title="Secure Decentralized Storage Control Server",
    description="Control plane for decentralized storage with access auditing",
    version="1.0.0"
)


# ------------------------
# Initialize DB
# ------------------------
Base.metadata.create_all(bind=engine)


# ------------------------
# Include Routers
# ------------------------
app.include_router(auth_router)
app.include_router(nodes_router)
app.include_router(files_router)
app.include_router(policy_router)
app.include_router(audit_router)
app.include_router(access_router)


# ------------------------
# Root
# ------------------------
@app.get("/")
def root():
    return {
        "message": "Control server is running",
        "services": [
            "auth",
            "nodes",
            "files",
            "policies",
            "audit"
        ]
    }


# ------------------------
# Health Check
# ------------------------
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "control_server"
    }
