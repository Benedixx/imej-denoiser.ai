from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.denoiser import denoise_image
from app.models.image import DenoiseResponse

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/denoise", response_model=DenoiseResponse)
async def denoise(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    result = denoise_image(file.file)
    return result