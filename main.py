import logging
'''import csv
import os
import datetime'''

import pathway as pw
from dotenv import load_dotenv
from pathway.xpacks.llm.question_answering import AdaptiveRAGQuestionAnswerer
from pathway.xpacks.llm.servers import QASummaryRestServer
from pydantic import BaseModel, ConfigDict, InstanceOf
#from pathway import Client

# To use advanced features with Pathway Scale, get your free license key from
# https://pathway.com/features and paste it below.
# To use Pathway Community, comment out the line below.
# pw.set_license_key("demo-license-key-with-telemetry")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv()

#csv for updating the mastery and difficulty
'''CSV_PATH = "logs/student_mastery_log.csv"  # mount logs folder into container if using Docker

def ensure_log_folder(path):
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

def append_mastery_log(doc_id, student_id, topic, mastery, difficulty, source="", csv_path=CSV_PATH):
    """
    Append a single row to the mastery CSV log with durable flush.
    """
    ensure_log_folder(csv_path)
    row = [
        datetime.datetime.utcnow().isoformat(),
        doc_id,
        student_id,
        topic,
        f"{mastery:.4f}",
        difficulty,
        source
    ]
    # Append row safely and flush to disk
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # If file was empty, write header first
        if f.tell() == 0:
            writer.writerow(["timestamp","doc_id","student_id","topic","mastery","difficulty","source"])
        writer.writerow(row)
        f.flush()
        os.fsync(f.fileno())
# persistence.py (continued)
import collections

def load_mastery_from_csv(csv_path=CSV_PATH):
    """
    Read the CSV log and return a mapping:
      latest[doc_id][student_id] = (mastery: float, difficulty: str, topic: str, source: str)
    We keep the last-seen row for each doc+student.
    """
    latest = collections.defaultdict(dict)
    if not os.path.exists(csv_path):
        return latest

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            doc_id = row["doc_id"]
            student_id = row["student_id"]
            try:
                mastery = float(row["mastery"])
            except Exception:
                continue
            difficulty = row.get("difficulty", "")
            topic = row.get("topic", "")
            source = row.get("source", "")
            # Overwrite previous — iterating file in chronological order preserves latest
            latest[doc_id][student_id] = {
                "mastery": mastery,
                "difficulty": difficulty,
                "topic": topic,
                "source": source
            }
    return latest'''


def adapt_difficulty(doc, student_id, performance_score):#, doc_id=None):
    """
    doc: object with doc.metadata
    student_id: string
    performance_score: float in [0,1]
    doc_id: string identifier (filename or id). If None, try to infer from metadata.
    """
    # ensure structure
    #doc.metadata.setdefault("student_mastery", {})

    mastery = doc.metadata["student_mastery"].get(student_id, 0.5)
    mastery = 0.8 * mastery + 0.2 * performance_score
    doc.metadata["student_mastery"][student_id] = mastery

    if mastery < 0.4:
        doc.metadata["difficulty"] = "easy"
    elif mastery < 0.7:
        doc.metadata["difficulty"] = "medium"
    else:
        doc.metadata["difficulty"] = "hard"

    # infer doc_id and topic
    '''if doc_id is None:
        doc_id = doc.metadata.get("filename") or doc.metadata.get("source") or "unknown_doc"
    topic = doc.metadata.get("topic", "")

    # append to CSV log
    append_mastery_log(doc_id=doc_id,
                       student_id=student_id,
                       topic=topic,
                       mastery=mastery,
                       difficulty=doc.metadata["difficulty"],
                       source=doc.metadata.get("source", ""))'''

    print(f"📈 Updated {student_id}: mastery={mastery:.2f}, difficulty={doc.metadata['difficulty']}")
    return doc

class App(BaseModel):
    question_answerer: InstanceOf[AdaptiveRAGQuestionAnswerer]
    host: str = "0.0.0.0"
    port: int = 8000

    with_cache: bool = True
    terminate_on_error: bool = False

    def run(self) -> None:
        server = QASummaryRestServer(self.host, self.port, self.question_answerer)
        server.run(
            with_cache=self.with_cache,
            terminate_on_error=self.terminate_on_error,
        )

    model_config = ConfigDict(extra="forbid")


if __name__ == "__main__":
    with open("app.yaml") as f:
        config = pw.load_yaml(f)
    app = App(**config)
    '''client = Client("http://localhost:8010")

    # Send a query
    response = client.answer(
        prompt="Explain electromagnetic induction",
        filters={"topic": "electromagnetism"}
    )

    print(response)'''
    '''def demonstrate_adaptive_update(student_id: str, correct: bool):
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
    demonstrate_adaptive_update("student_1", correct=True)'''

    
    '''latest = load_mastery_from_csv()

    # latest is mapping doc_id -> { student_id: {mastery, difficulty, ...} }
    # Apply to documents in your document store
    doc_store = app.question_answerer.indexer
    try:
        docs = doc_store.docs  # your actual document collection
        for doc in docs:
            fname = doc.metadata.get("filename") or "unknown_doc"
            if fname in latest:
                for sid, data in latest[fname].items():
                    doc.metadata.setdefault("student_mastery", {})
                    doc.metadata["student_mastery"][sid] = data["mastery"]
                doc.metadata["difficulty"] = list(latest[fname].values())[-1]["difficulty"]
        print("✅ Mastery applied to document store.")
    except Exception as e:
        print("⚠️ Could not apply mastery data:", e)'''
    app.run()
