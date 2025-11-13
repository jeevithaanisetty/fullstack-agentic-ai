Smart Research Assistant -  Automates literature review and report generation for a given topic query.

--> LangGraph multi-agent workflow 
--> Fastapi wrapping
--> Lanfuse Observability
--> Gemini models as LLMs

OVERVIEW :--
This Example shows a multi agent pipeline using Langgraph and Python.
Agents:- 
-- Search Agent: Fetches data from the web sources using langchain tools.
-- Analysis Agent: runs an LLM to identify the trends and themes from the collected data.
-- Summarizer Agent: Produces a structured report like introduction , key insights and next steps.
 
Requirements:
1.Create a virtual env and install the required libraries,frameworks,tools from requirements.txt
2.Create an Open api key for calling Gemini models in your application.
3.Store all secret keys like api key in environment varialbes for safety.

Run:
commanad :- uvicorn main:app --reload

Fastapi Endpoint:-
POST/research
Body: 
{"query":"Topic"}

Response:
JSON formatted final summary and intermediate data.

