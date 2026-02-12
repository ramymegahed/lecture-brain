# app/api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.engine import LectureBrainEngine
from fastapi import Path

# ----------- FastAPI app ----------
app = FastAPI(title="Lecture Brain API")

# ----------- Core Engine Instance ----------
engine = LectureBrainEngine()

# ----------- Pydantic Schema for User ----------
class UserCreate(BaseModel):
    user_id: str
    name: str

# ----------- Endpoint: Create User ----------
@app.post("/users")
async def create_user(user: UserCreate):
    try:
        new_user = engine.create_user(user.user_id, user.name)
        return {"user_id": new_user.user_id, "name": new_user.name}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------- Pydantic Schema for Subject ----------
class SubjectCreate(BaseModel):
    subject_id: str
    title: str

# ----------- Endpoint: Create Subject ----------
@app.post("/users/{user_id}/subjects")
async def create_subject(
    user_id: str = Path(..., description="ID of the user"),
    subject: SubjectCreate = None
):
    user = engine.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    try:
        new_subject = engine.create_subject(user_id, subject.subject_id, subject.title)
        return {"subject_id": new_subject.subject_id, "title": new_subject.title}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------- Pydantic Schema for Lecture ----------
class LectureCreate(BaseModel):
    lecture_id: str
    title: str

# ----------- Endpoint: Create Lecture ----------
@app.post("/users/{user_id}/subjects/{subject_id}/lectures")
async def create_lecture(
    user_id: str = Path(..., description="ID of the user"),
    subject_id: str = Path(..., description="ID of the subject"),
    lecture: LectureCreate = None
):
    user = engine.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    subject = next((s for s in user.subjects if s.subject_id == subject_id), None)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found for user {user_id}")
    
    try:
        new_lecture = engine.create_lecture(user_id, subject_id, lecture.lecture_id, lecture.title)
        return {"lecture_id": new_lecture.lecture_id, "title": new_lecture.title}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------- Pydantic Schema for Knowledge ----------
class KnowledgeCreate(BaseModel):
    content: str
    source: str = "text"

# ----------- Endpoint: Add Knowledge ----------
@app.post("/users/{user_id}/subjects/{subject_id}/lectures/{lecture_id}/knowledge")
async def add_knowledge(
    user_id: str = Path(..., description="ID of the user"),
    subject_id: str = Path(..., description="ID of the subject"),
    lecture_id: str = Path(..., description="ID of the lecture"),
    knowledge: KnowledgeCreate = None
):
    user = engine.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    subject = next((s for s in user.subjects if s.subject_id == subject_id), None)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found for user {user_id}")
    
    lecture = next((l for l in subject.lectures if l.lecture_id == lecture_id), None)
    if not lecture:
        raise HTTPException(status_code=404, detail=f"Lecture {lecture_id} not found")
    
    new_knowledge = engine.add_text_knowledge(user_id, subject_id, lecture_id, knowledge.content, knowledge.source)
    return {"content": new_knowledge.raw_content, "source": new_knowledge.type.name}


# ----------- Pydantic Schema for Question ----------
class QuestionRequest(BaseModel):
    question: str

# ----------- Endpoint: Ask Question ----------
@app.post("/users/{user_id}/subjects/{subject_id}/lectures/{lecture_id}/ask")
async def ask_question(
    user_id: str = Path(..., description="ID of the user"),
    subject_id: str = Path(..., description="ID of the subject"),
    lecture_id: str = Path(..., description="ID of the lecture"),
    request: QuestionRequest = None
):
    user = engine.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    subject = next((s for s in user.subjects if s.subject_id == subject_id), None)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found for user {user_id}")
    
    lecture = next((l for l in subject.lectures if l.lecture_id == lecture_id), None)
    if not lecture:
        raise HTTPException(status_code=404, detail=f"Lecture {lecture_id} not found")
    
    answer = engine.ask_question(user_id, subject_id, lecture_id, request.question)
    return {"question": request.question, "answer": answer}
