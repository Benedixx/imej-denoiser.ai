import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.denoiser import denoise_image
from app.models.image import DenoiseResponse
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/denoise")
async def denoise(file: UploadFile = File(...)):
    try :
        tmp_folder = '/tmp'
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)
        else:
            for file_existing in os.listdir(tmp_folder):
                os.remove(os.path.join(tmp_folder, file_existing))
        image_path = os.path.join(tmp_folder, file.filename)
        with open(image_path, "wb") as f:
            f.write(file.file.read())
        response = denoise_image(image_path)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        output_image_path = image_path + "_output.jpg"
        with open(output_image_path, 'wb') as out_file:
            out_file.write(response.content)

        return FileResponse(output_image_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    