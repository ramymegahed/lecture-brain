from typing import List

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.subjects: List[Subject] = []

    def add_subject(self, subject):
        self.subjects.append(subject)


class Subject:
    def __init__(self, subject_id: str, title: str):
        self.subject_id = subject_id
        self.title = title
        self.lectures: List[LectureBrain] = []

    def add_lecture(self, lecture):
        self.lectures.append(lecture)


class LectureBrain:
    def __init__(self, lecture_id: str, title: str):
        self.lecture_id = lecture_id
        self.title = title
        self.knowledge: List[Knowledge] = []

    def add_knowledge(self, knowledge):
        self.knowledge.append(knowledge)


class Knowledge:
    def __init__(self, content: str, source: str = "text"):
        self.content = content
        self.source = source
