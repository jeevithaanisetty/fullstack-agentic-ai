from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph,END
from search_agent import search_agent
from analysis_agent import analysis_agent
from summary_agent import summary_agent
from validator_agent import validator_agent
from typing import TypedDict

llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro")


class GraphState(TypedDict):
    query:str
    search_results:str
    analysis:str
    summary:str
    validated_summary:str

def create_graph():
    graph=StateGraph(GraphState)

    graph.add_node("search",search_agent)
    graph.add_node("analysis",analysis_agent)
    graph.add_node("summary",summary_agent)
    graph.add_node("validation",validator_agent)

    graph.set_entry_point("search")

    graph.add_edge("search","analysis")
    graph.add_edge("analysis","summary")
    graph.add_edge("summary","validation")
    graph.add_edge("validation",END)

    return graph.compile()