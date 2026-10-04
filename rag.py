from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


def generate_answer(question, retrieved_results):

    context = "\n\n".join(
        [
            f"Source: {result['source']}\n{result['text']}"
            for result in retrieved_results
        ]
    )

    prompt = f"""
You are CampusSathi, an AI Student Support & Opportunity Navigator.

Answer ONLY from the provided context.

Rules:
1. Never invent information.
2. If information is missing, say:
   "I could not verify this information from the available documents."
3. Mention relevant source names.
4. Be clear and concise.

Context:
{context}

Student Question:
{question}

Provide:

ANSWER

SOURCES USED
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        return """
⚠️ AI service temporarily unavailable.

Please review the retrieved evidence below.
"""