from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI
from chatbot.memory import vectorstore, embeddings
from langchain.docstore.document import Document
from langchain_core.documents import Document
from chatbot.sentiment import analyze_sentiment
from journal_db import init_db, save_entry, get_all_entries
from flask_cors import CORS




load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
init_db()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Analyze mood
    sentiment = analyze_sentiment(user_input)

    # Retrieve similar past messages from memory
    results = vectorstore.similarity_search(user_input, k=3)
    past_context = "\n".join([r.page_content for r in results])

    prompt = f"""
    You are a compassionate mental health assistant.
    Respond with empathy and awareness of the user's emotions.

    Previous context:
    {past_context}

    User (mood: {sentiment}): {user_input}
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )
    reply = completion.choices[0].message.content

    # Store both in memory and journal
    docs = [
        Document(page_content=f"User: {user_input}"),
        Document(page_content=f"Assistant: {reply}")
    ]
    vectorstore.add_documents(docs)

    save_entry(user_input, sentiment, reply)

    return jsonify({"response": reply, "sentiment": sentiment})

if __name__ == "__main__":
    print("Flask app starting...")
    app.run(debug=True)