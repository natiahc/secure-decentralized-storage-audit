from fastapi import FastAPI
from database import Base, engine
from routes_auth import router as auth_router
from routes_nodes import router as nodes_router
from routes_files import router as files_router
from routes_policy import router as policy_router
from routes_audit import router as audit_router

app.include_router(auth_router)
app.include_router(nodes_router)
app.include_router(files_router)
app.include_router(policy_router)
app.include_router(audit_router)

app = FastAPI(
    title="Secure Decentralized Storage Control Server",
    version="1.0.0"
)

# Create tables on startup
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Control server is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "control_server"
    }
