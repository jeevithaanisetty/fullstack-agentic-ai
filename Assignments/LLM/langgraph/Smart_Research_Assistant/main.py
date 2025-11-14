from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from db import init_db,save_query,get_all_queries,get_recent_query

app = FastAPI(title="Smart Research Assistant")

graph= create_graph()

class Run(BaseModel):
    query:str

@app.get("/")
async def health():
    return {"status":"Running...","API":"smart research agent"}

@app.on_event("startup")
def startup():
    init_db()

@app.post("/run_graph")
async def run_workflow(data:Run):
    if not data.query:
        raise HTTPException(status_code=400,detail="query parameter is required...")
    state={
        "query":data.query,
        "search_results":None,
        "analysis":None,
        "summary":None,
        "validated_summary":None,
        "prompt_overrides":{},
        "raw_search_chunks":[]
        }
    final_state=None

    async for step in graph.astrem(state,stream_mode="updates"):      #astream yields intermediate states as final state
        final_state=step
    
    doc={ "query":data.query,
        "search_results":final_state.get("search_results"),
        "analysis":final_state.get("analysis"),
        "summary":final_state.get("summary"),
        "validated_summary":final_state.get("validated_summary")
        }
    save_query(doc)
    
    return doc

@app.get("/history")
async def query_history(limit:int=10):
    history= await get_all_queries(limit)
    return {"recent":[{"id":h[0],"query":h[1]} for h in history]}

@app.get("/recent_history")
async def get_recent_history():
    history=await get_recent_query()
    if not history:
        raise HTTPException(status_code=404,detail="not found")
    return history

