from graph import GraphState,llm

async def analysis_agent(state:GraphState):
    data=state["search_results"]

    prompt=f""" 
    You are an Analysis Agent.Analyze the information below and extract:
    -Trends
    -Sentiment
    -Themes
    -Insights
    Data:{data}
    """
    response=llm.invoke(prompt)
    return {"analysis":response.content}
