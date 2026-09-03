import os

dirs = [
    "app",
    "app/api",
    "app/api/endpoints",
    "app/core",
    "app/models",
    "app/schemas",
    "app/services",
    "app/repositories",
    "app/middleware",
    "app/utils",
    "app/db",
    "tests"
]

for d in dirs:
    os.makedirs(f"backend/{d}", exist_ok=True)
    with open(f"backend/{d}/__init__.py", "w") as f:
        pass

reqs = '''fastapi==0.110.0
uvicorn==0.27.1
pydantic==2.6.3
pydantic-settings==2.2.1
sqlalchemy==2.0.27
alembic==1.13.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
pytest==8.0.2
httpx==0.27.0'''

with open("backend/requirements.txt", "w") as f:
    f.write(reqs)

main_py = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Research Prototype Hub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Research Prototype Hub API"}
'''

with open("backend/app/main.py", "w") as f:
    f.write(main_py)
