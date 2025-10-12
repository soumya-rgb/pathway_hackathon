from main import adapt_difficulty

def demonstrate_adaptive_update(student_id: str, correct: bool):
        """Demonstrate how the student's mastery adapts based on performance."""
        # Access the document store
        doc_store = app.question_answerer.indexer
        docs = getattr(doc_store, "docs", None)

        if not docs or len(docs) == 0:
            print("No documents found to demonstrate adaptive update.")
            return

        # Select first document for the demo
        doc = list(docs)[0]
        filename = doc.metadata.get("filename", "Unknown Document")
        topic = doc.metadata.get("topic", "General")
        old_mastery = doc.metadata.get(f"student_mastery_{student_id}", 0.5)

        # Apply the update
        new_mastery = adapt_difficulty(student_id, doc, correct)

        # Display summary
        print("\n============================")
        print(f"Adaptive Learning Demo for {student_id}")
        print("----------------------------")
        print(f"Topic: {topic}")
        print(f"Document: {filename}")
        print(f"Previous Mastery: {old_mastery:.2f}")
        print(f"Updated Mastery:  {new_mastery:.2f}")
        print(f"Performance: {'✅ Correct' if correct else '❌ Incorrect'}")
        print("============================\n")

    # Run a demonstration for presentation
    demonstrate_adaptive_update("student_1", correct=True)


'''# Mock a document with metadata
class MockDoc:
    def __init__(self):
        self.metadata = {
            "topic": "electromagnetism",
            "content_type": "lesson",
            "difficulty": "medium",
            "student_mastery": {"student_1": 0.5, "student_2": 0.8}
        }

# Create a mock document
doc = MockDoc()

print("Before update:", doc.metadata)

# Test case 1: student_1 performs poorly (score = 0.2)
adapt_difficulty(doc, "student_1", performance_score=0.2)
print("After low score:", doc.metadata)

# Test case 2: student_1 improves (score = 0.9)
adapt_difficulty(doc, "student_1", performance_score=0.9)
print("After high score:", doc.metadata)

# Test case 3: new student (student_3)
adapt_difficulty(doc, "student_3", performance_score=0.7)
print("After new student:", doc.metadata)'''
