from fastapi import FastAPI
from fastapi import APIRouter, UploadFile, File

app = FastAPI()

@app.post("/inference")
async def inference(file: UploadFile = File(...)):
    # Dummy response
    return {"status": "success", "inference_result": "dummy_result"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=5000)