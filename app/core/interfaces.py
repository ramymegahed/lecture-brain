# app/core/interfaces.py
from abc import ABC, abstractmethod

# ------------ Source Interface ------------
class SourcePlugin(ABC):
    """
    أي Source جديد لازم يرث من ده.
    زي: YouTube, PDF, Text File
    """
    name: str

    @abstractmethod
    def fetch(self, identifier: str) -> str:
        """
        identifier ممكن يكون رابط أو مسار للملف
        لازم ترجع النصوص المستخرجة من المصدر
        """
        pass


# ------------ Action Interface ------------
class ActionPlugin(ABC):
    """
    أي Action جديد لازم يرث من ده.
    زي: Summary, Explain, MakeQuestions
    """
    name: str

    @abstractmethod
    def run(self, lecture, params: dict) -> str:
        """
        lecture: LectureBrain object
        params: dictionary ممكن يستخدمه Action
        لازم ترجع النص الناتج أو النتيجة
        """
        pass
