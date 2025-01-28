import os
import gdown
import hashlib
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from .inference import allocate_buffers, load_engine, do_inference, preprocess_image, postprocess_image

app = FastAPI()

# Path untuk model
model_path = 'app/model.trt'

# Fungsi untuk cek ukuran file
def is_valid_file(file_path, expected_size):
    actual_size = os.path.getsize(file_path)
    print(f"File size: {actual_size} bytes, Expected size: {expected_size} bytes")
    return actual_size == expected_size

# Pastikan model terdownload dengan benar
if not os.path.exists(model_path):
    url = 'https://drive.google.com/uc?export=download&id=1LDS9zcLw1Jw8LEtQw-KodeMUWfFIqW99'  # Link langsung untuk download
    gdown.download(url, model_path, quiet=False)

    # Tambahkan ukuran file yang diharapkan (dalam bytes) = 2663 KB
    expected_size = 2663 * 1024
    if not is_valid_file(model_path, expected_size):
        raise RuntimeError("Model download failed, file size mismatch!")

# Load engine setelah validasi
engine = load_engine(model_path)

@app.post("/inference")
async def inference(file: UploadFile = File(...)):
    tmp_folder = '/tmp'
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)
    else:
        for file_existing in os.listdir(tmp_folder):
            os.remove(os.path.join(tmp_folder, file_existing))

    image_path = os.path.join(tmp_folder, file.filename)
    output_path = os.path.join(tmp_folder, file.filename + "_output.jpg")

    with open(image_path, "wb") as f:
        f.write(file.file.read())

    context = engine.create_execution_context()
    inputs, outputs, bindings, stream = allocate_buffers(engine)

    input_image, original_size = preprocess_image(image_path)
    np.copyto(inputs[0]['host'], input_image.ravel())

    output = do_inference(context, bindings, inputs, outputs, stream)
    output_image = postprocess_image(output[0], original_size)

    # Simpan gambar hasil output
    output_image.save(output_path)
    print(f"Output saved to {output_path}")
    return FileResponse(output_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
