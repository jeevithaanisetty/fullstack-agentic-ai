from graph import GraphState,llm

async def summary_agent(state:GraphState):
    analysis=state["anallysis"]

    prompt=f"""
    You are a Summarizer Agent. Create a polished structured report including:
    -Introduction
    -Key Insights
    -Trends
    -Final Summary
    Analysis:
    {analysis}
    """
    response=llm.invoke(prompt)
    return {"summary":response.content}