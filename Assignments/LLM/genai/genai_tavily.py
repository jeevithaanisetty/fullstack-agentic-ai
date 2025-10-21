import google.generativeai as genai
from tavily import TavilyClient
import os

genai.configure(api_key=(os.getenv("GEMINI-API-KEY")))
model=genai.GenerativeModel("gemini-2.5-pro")

query="AI in Education in 2025"
tavily=TavilyClient(api_key=os.getenv("TAVILY-API-KEY"))

results= tavily.search(query)
results_text = "\n".join([str(r) for r in results])

summary=model.generate_content(f"Summarize these results: \n\n{results_text}")
print(summary)