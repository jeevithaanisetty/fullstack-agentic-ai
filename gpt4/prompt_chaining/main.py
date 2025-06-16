from fastapi import FastAPI
from app.chain import router                  

app=FastAPI(title="prompt chain API",version="1.0.0")
app.include_router(router,prefix="/api",tags=["Promptchain"])
