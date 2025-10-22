import os

import dotenv
from fastapi import FastAPI  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from openai import OpenAI  # type: ignore

dotenv.load_dotenv(override=True)

app = FastAPI()

@app.get("/api")
def idea():
    client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                    api_key=os.getenv('GOOGLE_API_KEY'))

    prompt = [{"role": "user", "content": ("Come up with a new business idea for AI Agents, "
                                           "formatted with headings, sub-headings and bullet points")}]

    stream = client.chat.completions.create(model="gemini-2.5-flash-lite-preview-09-2025",
                                            messages=prompt,
                                            stream=True)

    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
