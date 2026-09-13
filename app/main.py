from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db


# --------------------------------------------------
# PATHS
# --------------------------------------------------

# app/ folder
APP_DIR = Path(__file__).resolve().parent

# app/static/
STATIC_DIR = APP_DIR / "static"

# app/templates/
TEMPLATES_DIR = APP_DIR / "templates"

# app/static/assets/Ragini_Yadav_Resume.pdf
RESUME_PATH = STATIC_DIR / "assets" / "Ragini_Yadav_Resume.pdf"


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="Ragini Yadav — Portfolio",
    version="1.0.0"
)


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = TEMPLATES_DIR / "index.html"

    if not html_path.exists():
        raise HTTPException(
            status_code=404,
            detail="index.html not found"
        )

    return HTMLResponse(
        html_path.read_text(encoding="utf-8")
    )


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# --------------------------------------------------
# VIEW RESUME
# --------------------------------------------------

@app.get("/resume")
async def view_resume():

    if not RESUME_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Resume file not found"
        )

    return FileResponse(
        path=RESUME_PATH,
        media_type="application/pdf"
    )


# --------------------------------------------------
# DOWNLOAD RESUME
# --------------------------------------------------

@app.get("/resume/download")
async def download_resume():

    if not RESUME_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Resume file not found"
        )

    return FileResponse(
        path=RESUME_PATH,
        media_type="application/pdf",
        filename="Ragini_Yadav_Resume.pdf"
    )


# --------------------------------------------------
# CONTACT API
# --------------------------------------------------

@app.post(
    "/api/contact",
    response_model=schemas.ContactOut,
    status_code=201
)
def create_contact_message(
    payload: schemas.ContactCreate,
    db: Session = Depends(get_db),
):

    entry = models.ContactMessage(
        name=payload.name.strip(),
        email=str(payload.email),
        message=payload.message.strip(),
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


@app.get(
    "/api/contact",
    response_model=List[schemas.ContactOut]
)
def list_contact_messages(
    db: Session = Depends(get_db)
):

    return (
        db.query(models.ContactMessage)
        .order_by(
            models.ContactMessage.created_at.desc()
        )
        .all()
    )


# --------------------------------------------------
# PROJECTS API
# --------------------------------------------------

@app.post(
    "/api/projects",
    response_model=schemas.ProjectOut,
    status_code=201
)
def create_project(
    payload: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):

    project = models.Project(
        **payload.model_dump()
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@app.get(
    "/api/projects",
    response_model=List[schemas.ProjectOut]
)
def list_projects(
    db: Session = Depends(get_db)
):

    return (
        db.query(models.Project)
        .order_by(
            models.Project.created_at.desc()
        )
        .all()
    )


@app.delete(
    "/api/projects/{project_id}",
    status_code=204
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()