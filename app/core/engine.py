# app/core/engine.py

from typing import Dict
from .models import User, Subject, LectureBrain, Knowledge

class LectureBrainEngine:
    def __init__(self):
        # تخزين كل users في dictionary: user_id -> User
        self.users: Dict[str, User] = {}

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
    def add_text_knowledge(self, user_id: str, subject_id: str, lecture_id: str, content: str, source: str = "text"):
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        subject = next((s for s in user.subjects if s.subject_id == subject_id), None)
        if not subject:
            raise ValueError(f"Subject {subject_id} not found")
        lecture = next((l for l in subject.lectures if l.lecture_id == lecture_id), None)
        if not lecture:
            raise ValueError(f"Lecture {lecture_id} not found")
        knowledge = Knowledge(content, source)
        lecture.add_knowledge(knowledge)
        return knowledge

    # ---------- Ask Question (Mock) ----------
    def ask_question(self, user_id: str, subject_id: str, lecture_id: str, question: str):
        """
        Mock answer generator: يرجع النصوص كلها في LectureBrain
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
        # Mock answer: نجمع كل النصوص
        combined_text = "\n".join([k.content for k in lecture.knowledge])
        return f"Answer based on lecture knowledge:\n{combined_text}"
