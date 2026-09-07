import requests

BASE_URL = "https://openrouter.ai/api/v1"
EMBED_MODEL = "openai/text-embedding-3-small"

def embed_texts(texts: list[str], api_key: str, model: str = EMBED_MODEL) -> list[list[float]]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url=f"{BASE_URL}/embeddings",
        headers=headers,
        json={
            "model": model,
            "input": texts,
        },
    )
    response.raise_for_status()
    data = response.json()

    return [item["embedding"] for item in data["data"]]