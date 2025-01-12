from pydantic import BaseModel

class DenoiseResponse(BaseModel):
    status: str
    denoised_image_url: str