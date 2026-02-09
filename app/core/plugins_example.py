from .interfaces import ActionPlugin, SourcePlugin

# ------------ Dummy Source ------------
class TextSource(SourcePlugin):
    name = "text"

    def fetch(self, identifier: str) -> str:
        return f"Fetched text from {identifier}"

# ------------ Dummy Action ------------
class SummaryAction(ActionPlugin):
    name = "summary"

    def run(self, lecture, params: dict) -> str:
        # يرجع أول knowledge فقط
        if lecture.knowledge:
            return f"Summary: {lecture.knowledge[0].content}"
        return "No knowledge to summarize"
