from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_lawsuit(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{
            "role": "user",
            "content": f"""
Summarize this lawsuit in simple terms:

{text}

Include:
- who is being sued
- what happened
- possible consumer impact
- whether people may qualify for compensation
"""
        }]
    )

    return response.choices[0].message.content
