from app.core.engine import LectureBrainEngine

engine = LectureBrainEngine()

# إنشاء User, Subject, Lecture
engine.create_user("u1", "Rami")
engine.create_subject("u1", "s1", "Math")
engine.create_lecture("u1", "s1", "l1", "Algebra")

# إضافة Knowledge
k1 = engine.add_text_knowledge(
    "u1", "s1", "l1",
    "Important algebra point number one. This is a sample content to test chunking functionality."
)
k2 = engine.add_text_knowledge(
    "u1", "s1", "l1",
    "Second piece of knowledge for testing. Should be chunked correctly."
)

# طباعة Knowledge chunks
lecture = engine.get_user("u1").subjects[0].lectures[0]
for idx, k in enumerate(lecture.knowledge):
    print(f"\nKnowledge {idx+1} chunks:")
    print(k.processed_chunks)


answer = engine.ask_question("u1", "s1", "l1", "Explain Algebra")
print(answer)
