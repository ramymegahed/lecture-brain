# app/core/engine.py
from typing import Dict, Optional
from .models import User, Subject, LectureBrain, Knowledge
from .registry import PluginRegistry


class LectureBrainEngine:
    def __init__(self):
        # تخزين كل users في dictionary: user_id -> User
        self.users: Dict[str, User] = {}
        self.registry = PluginRegistry()
    # ---------- Users ----------
    def create_user(self, user_id: str, name: str):
        if user_id in self.users:
            raise ValueError(f"User {user_id} already exists")
        user = User(user_id, name)
        self.users[user_id] = user
        return user

    def get_user(self, user_id: str):
        return self.users.get(user_id)

    # ---------- Subjects ----------
    def create_subject(self, user_id: str, subject_id: str, title: str):
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        subject = Subject(subject_id, title)
        user.add_subject(subject)
        return subject

    # ---------- Lectures ----------
    def create_lecture(self, user_id: str, subject_id: str, lecture_id: str, title: str):
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        subject = next((s for s in user.subjects if s.subject_id == subject_id), None)
        if not subject:
            raise ValueError(f"Subject {subject_id} not found for user {user_id}")
        lecture = LectureBrain(lecture_id, title)
        subject.add_lecture(lecture)
        return lecture

    # ---------- Knowledge ----------
    def add_text_knowledge(self, user_id: str, subject_id: str, lecture_id: str, content: str, type_: str = "text", metadata: Optional[Dict] = None):
        user = self.get_user(user_id)
        if not user:
           raise ValueError(f"User {user_id} not found")
        subject = next((s for s in user.subjects if s.subject_id == subject_id), None)
        if not subject:
           raise ValueError(f"Subject {subject_id} not found")
        lecture = next((l for l in subject.lectures if l.lecture_id == lecture_id), None)
        if not lecture:
           raise ValueError(f"Lecture {lecture_id} not found")

        from .models import Knowledge, KnowledgeType
        knowledge = Knowledge(content=content, type_=KnowledgeType(type_), metadata=metadata)
        lecture.add_knowledge(knowledge)
        return knowledge

    # ---------- Ask Question (Mock) ----------
    # ---------- Ask Question (Chunk-based Mock) ----------
    def ask_question(self, user_id: str, subject_id: str, lecture_id: str, question: str) -> str:
     """
     Mock answer generator باستخدام Knowledge chunks:
     - يجيب كل chunks من الـ Lecture
     - يدمجهم في نص واحد (محاكي لـ RAG)
     """
     user = self.get_user(user_id)
     if not user:
        raise ValueError(f"User {user_id} not found")
     subject = next((s for s in user.subjects if s.subject_id == subject_id), None)
     if not subject:
        raise ValueError(f"Subject {subject_id} not found")
     lecture = next((l for l in subject.lectures if l.lecture_id == lecture_id), None)
     if not lecture:
        raise ValueError(f"Lecture {lecture_id} not found")

    # جمع كل الـ chunks
     all_chunks = []
     for k in lecture.knowledge:
        all_chunks.extend(k.processed_chunks)  # كل Knowledge ممكن يكون فيها أكثر من chunk

    # هنا نقدر نعمل أي معالجة Mock إضافية
    # مثلاً اختيار أول 3 chunks بس أو دمجهم في نص واحد
     combined_text = "\n".join(all_chunks)

    # نرجع Mock answer
     return f"Question: {question}\nAnswer based on chunks:\n{combined_text}"

    
        # ---------- Plugins ----------
    def register_action(self, action_class):
        self.registry.register_action(action_class)

    def register_source(self, source_class):
        self.registry.register_source(source_class)

    def run_action(self, action_name: str, lecture: LectureBrain, params: dict):
        action = self.registry.get_action(action_name)
        return action.run(lecture, params)

    def run_source(self, source_name: str, location: str):
        source = self.registry.get_source(source_name)
        return source.fetch(location)

