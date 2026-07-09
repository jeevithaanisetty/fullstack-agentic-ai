from fastapi import FastAPI
from api.routes import router

app=FastAPI(
    title="Question generator",
    version="1.0.0"
)
app.include_router(router)

@app.get("/")
def health():
    return{
        "status":"Running",
        "message":"Video question generator API"
    }