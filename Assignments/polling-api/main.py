from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def health():
    return f"Hi viewer ! This is a polling API"
