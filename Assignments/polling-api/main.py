from fastapi import FastAPI
from app.routes import poll_routes,user_routes

app=FastAPI(title="Polling-Application")

app.include_router(user_routes.router,tags=["Users"])
app.include_router(poll_routes.router,tags=["Polls"])

@app.get("/")
async def health():
    return f"Hi viewer ! This is a polling API"
