from openai import OpenAI
import json
from config import OPENROUTER_API_KEY

class QuestionService:

    client=OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key= OPENROUTER_API_KEY
    )

    @staticmethod
    def generate_questions(transcript:str):
        prompt= f"""
                You are an AI tutor.
                Generate questions ONLY from the transcript below.
                Return only valid JSON in the following format:
                {{
                    "mcqs":[
                    {{
                        "question":"",
                        "options":["","","",""],
                        "answer":""
                    }}
                    ]
                }}
                Transcript:{transcript}
                """
        response=QuestionService.client.chat.completions.create(
            model="openrouter/free",   #deepseek/deepseek-chat-v3-0324:free is not a free model now
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperature=0.3   
        )
        result=response.choices[0].message.content
        try:
            return json.loads(result)
        except Exception:
            return {
                "response":result
            }