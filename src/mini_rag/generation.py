import requests

BASE_URL = "https://openrouter.ai/api/v1"
CHAT_MODEL = "minimax/minimax-m3:free"


def generate_answer(query: str, context_chunks: list[str], api_key: str, model: str = CHAT_MODEL) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    context_text = "\n\n---\n\n".join(context_chunks)

    system_prompt = (
        "Kamu adalah asisten yang menjawab pertanyaan HANYA berdasarkan "
        "context yang diberikan di bawah. Jika jawabannya tidak ada di "
        "context, katakan kamu tidak tahu — jangan mengarang."
    )
    user_prompt = f"Context:\n{context_text}\n\nPertanyaan: {query}"

    response = requests.post(
        url=f"{BASE_URL}/chat/completions",
        headers=headers,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        },
    )
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]