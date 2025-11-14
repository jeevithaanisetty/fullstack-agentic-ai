from langchain_google_genai import ChatGoogleGenerativeAI
from graph import GraphState

llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro")


async def search_agent(state:GraphState):
    query=state["query"]
    prompt=f"""
    You are a Search Agent.Retrieve or simulate research findings about the topic below.
    Provide 5 bullet points of factual information.
    Topic:{query}
    """
    response= await llm.invoke(prompt)
    return {"search_results":response.content}