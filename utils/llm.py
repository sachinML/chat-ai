# utils/llm.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Make sure your API key is set in environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_answer(context: str, question: str) -> str:
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nIf you don't know the answer from the context, say \"I don't know the answer\"."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, who will give a proper response as per the question asked by the user.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
    )

    answer = response["choices"][0]["message"]["content"].strip()

    if "I don't know the answer" in answer:
        return "I don't know the answer"

    return answer
