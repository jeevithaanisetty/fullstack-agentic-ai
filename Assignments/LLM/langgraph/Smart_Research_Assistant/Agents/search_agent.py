from graph import GraphState,llm

async def search_agent(state:GraphState):
    query=state["query"]
    prompt=f"""
    You are a Search Agent.Retrieve or simulate research findings about the topic below.
    Provide 5 bullet points of factual information.
    Topic:{query}
    """
    response= llm.invoke(prompt)
    return {"search_results":response.content}