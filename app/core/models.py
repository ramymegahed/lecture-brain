# app/core/models.py
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
from uuid import uuid4

# ---------------- Knowledge Type ----------------
class KnowledgeType(str, Enum):
    TEXT = "text"
    PDF = "pdf"
    YOUTUBE = "youtube"

# ---------------- Knowledge ----------------
class Knowledge:
    def __init__(self, content: str, type_: KnowledgeType = KnowledgeType.TEXT, metadata: Optional[Dict] = None):
        self.id: str = str(uuid4())
        self.raw_content: str = content
        self.processed_chunks: List[str] = []  # لتقسيم النصوص
        self.metadata: Dict = metadata or {}   # مثال: {"page":1, "timestamp": "...", "source_url": "..."}
        self.type: KnowledgeType = type_
        self.created_at: datetime = datetime.utcnow()

    def chunk_content(self, chunk_size: int = 50):
        """
        تقسيم النصوص لكلمات أو جمل صغيرة لتسهيل RAG
        chunk_size: عدد الكلمات لكل chunk
        """
        words = self.raw_content.split()
        self.processed_chunks = [
            " ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)
        ]
        return self.processed_chunks

# ---------------- Lecture ----------------
class LectureBrain:
    def __init__(self, lecture_id: str, title: str):
        self.lecture_id: str = lecture_id
        self.title: str = title
        self.knowledge: List[Knowledge] = []

    def add_knowledge(self, knowledge: Knowledge):
        knowledge.chunk_content()  # chunk تلقائي عند الإضافة
        self.knowledge.append(knowledge)

# ---------------- Subject ----------------
class Subject:
    def __init__(self, subject_id: str, title: str):
        self.subject_id: str = subject_id
        self.title: str = title
        self.lectures: List[LectureBrain] = []

    def add_lecture(self, lecture: LectureBrain):
        self.lectures.append(lecture)

# ---------------- User ----------------
class User:
    def __init__(self, user_id: str, name: str):
        self.user_id: str = user_id
        self.name: str = name
        self.subjects: List[Subject] = []

    def add_subject(self, subject: Subject):
        self.subjects.append(subject)
