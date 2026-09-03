from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, projects, tasks, prototypes, findings
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="THINK BIG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api", tags=["projects"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(prototypes.router, prefix="/api", tags=["prototypes"])
app.include_router(findings.router, prefix="/api", tags=["findings"])

@app.get("/")
def read_root():
    return {"message": "Welcome to THINK BIG API"}
