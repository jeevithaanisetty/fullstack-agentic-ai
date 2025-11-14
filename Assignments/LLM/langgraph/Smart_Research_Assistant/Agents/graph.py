from langgraph.graph import StateGraph,END
from typing import TypedDict

class GraphState(TypedDict):
    query:str
    search_results:str
    analysis:str
    summary:str
    validated_summary:str
