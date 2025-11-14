from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph,END
from typing import TypedDict

llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro")


class GraphState(TypedDict):
    query:str
    search_results:str
    analysis:str
    summary:str
    validated_summary:str
