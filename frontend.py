# gradio_adaptive_query.py
import gradio as gr
import requests

# CONFIGURATION

RAG_ENDPOINT = "http://localhost:8008/v2/answer"
STUDENT_ID = "student_1"

# DEMO DATA + LOGIC
class Doc:
    def __init__(self, filename, topic, difficulty="medium"):
        self.metadata = {
            "filename": filename,
            "topic": topic,
            "difficulty": difficulty,
            f"student_mastery_{STUDENT_ID}": 0.5,
        }

'''# one example document (replace with real topic later)
demo_doc = Doc("Electromagntic induction", "electromagnetism")'''

def adapt_difficulty(student_id, doc, correct):
    mastery = doc.metadata.get(f"student_mastery_{student_id}", 0.5)
    delta = 0.1 if correct else -0.05
    mastery = max(0, min(1, mastery + delta))
    doc.metadata[f"student_mastery_{student_id}"] = mastery
    return mastery

# -----------------------------
# RAG QUERY FUNCTION
# -----------------------------
'''def ask_query(prompt, topic, difficulty):
    """
    Sends a query to the Adaptive RAG backend and returns the model answer + any retrieved sources.
    """
    filters = {"topic": topic, "content_type": "lesson"}
    if difficulty.lower() != "any":
        filters["difficulty"] = difficulty.lower()

    payload = {
        "prompt": prompt,
        "filters_flat": filters  # use filters_flat to avoid flattening errors
    }

    try:
        resp = requests.post(RAG_ENDPOINT, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("answer") or data.get("response") or "No response text returned."
        # extract filenames or context if available
        sources = []
        for key in ("sources", "docs", "retrieved_documents", "context"):
            if key in data and isinstance(data[key], list):
                for d in data[key]:
                    fname = d.get("filename") or d.get("doc_id") or d.get("source")
                    if fname:
                        sources.append(fname)
        src_text = ", ".join(sources) if sources else "No sources found."
        return answer, src_text
    except Exception as e:
        return f"❌ Error contacting RAG: {e}", ""
'''
def ask_query(prompt, topic, difficulty):
    """
    Sends a query to the Adaptive RAG backend and returns the model answer + any retrieved sources.
    Also creates a dynamic doc based on the topic.
    """
    # Decide filename based on topic (or just keep topic as filename)
    filename = f"{topic.title()} Lesson" if topic else "General Lesson"
    
    # Create a dynamic document
    global demo_doc
    demo_doc = Doc(filename, topic or "general")  # fallback to "general"

    # Filters for RAG
    filters = {"topic": demo_doc.metadata["topic"], "content_type": "lesson"}
    if difficulty.lower() != "any":
        filters["difficulty"] = difficulty.lower()

    payload = {"prompt": prompt, "filters_flat": filters}

    try:
        resp = requests.post(RAG_ENDPOINT, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("answer") or data.get("response") or "No response text returned."

        sources = []
        for key in ("sources", "docs", "retrieved_documents", "context"):
            if key in data and isinstance(data[key], list):
                for d in data[key]:
                    fname = d.get("filename") or d.get("doc_id") or d.get("source")
                    if fname:
                        sources.append(fname)
        src_text = ", ".join(sources) if sources else "No sources found."

        return answer, src_text

    except Exception as e:
        return f"❌ Error contacting RAG: {e}", ""

# -----------------------------
# ADAPTIVE UPDATE FUNCTION
# -----------------------------
def update_mastery(choice):
    correct = choice == "Correct"
    mastery = adapt_difficulty(STUDENT_ID, demo_doc, correct)

    # dynamic difficulty switching
    if mastery < 0.4:
        demo_doc.metadata["difficulty"] = "easy"
    elif mastery < 0.7:
        demo_doc.metadata["difficulty"] = "medium"
    else:
        demo_doc.metadata["difficulty"] = "hard"

    return (
        f"✅ Mastery for {STUDENT_ID}: {mastery:.2f}",
        f"📘 Topic: {demo_doc.metadata['topic']}\n"
        f"📄 Document: {demo_doc.metadata['filename']}\n"
        f"⚙️ Current Difficulty: {demo_doc.metadata['difficulty']}"
    )

# -----------------------------
# GRADIO UI
# -----------------------------
with gr.Blocks(title="LearnPro") as demo:
    gr.Markdown("# 🎓 Adaptive RAG Learning Portal")
    gr.Markdown("Ask questions, receive lessons, and adjust your mastery interactively.")

    with gr.Tab("Ask a Question"):
        
        with gr.Row():
            # Input column
            with gr.Column(scale=2):
                prompt = gr.Textbox(
                    label="Your Question",
                    lines=3,
                    placeholder="Type your question here"
                )
                topic = gr.Textbox(
                    label="Topic",
                    placeholder="Enter the topic"
                )
                difficulty = gr.Dropdown(
                    choices=["any","easy","medium","hard"],
                    value="any",
                    label="Difficulty filter"
                )
                ask_btn = gr.Button("Ask RAG System")
            
            # Output column
            with gr.Column(scale=2):
                answer_box = gr.Textbox(
                    label="RAG Response",
                    lines=10
                )
                sources_box = gr.Textbox(
                    label="Sources",
                    lines=3
                )

        # Connect the button to your function
        ask_btn.click(
            fn=ask_query,  # your existing function
            inputs=[prompt, topic, difficulty],
            outputs=[answer_box, sources_box]
        )

    with gr.Tab("Adaptive Feedback"):
        gr.Markdown("Simulate student feedback to update mastery dynamically.")
        result_text = gr.Textbox(label="Mastery Update", interactive=False)
        doc_text = gr.Textbox(label="Document Info", interactive=False)

        with gr.Row():
            correct_btn = gr.Button("✅ Correct")
            incorrect_btn = gr.Button("❌ Incorrect")

        correct_btn.click(fn=lambda: update_mastery("Correct"), outputs=[result_text, doc_text])
        incorrect_btn.click(fn=lambda: update_mastery("Incorrect"), outputs=[result_text, doc_text])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
