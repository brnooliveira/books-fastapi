from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def first_api():
    return {
        "message": "Hello Breno!"
    }

@app.get("/{name}")
async def read_name(name: str):
    return {
        name
    }
