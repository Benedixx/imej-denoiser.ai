from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
