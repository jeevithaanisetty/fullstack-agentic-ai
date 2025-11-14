from graph import GraphState,llm

async def validator_agent(state:GraphState):
    summary=state["summary"]
    prompt=f"""
    You are a Validator Agent.Review the summary for consistency,clarity and correctness.
    Identify issues and provide corrections if needed.
    Summary:{summary}
    """
    response=llm.invoke(prompt)
    return {"validated_summary":response.content}