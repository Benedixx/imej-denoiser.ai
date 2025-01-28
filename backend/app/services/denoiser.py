import requests

def denoise_image(image_path: str):
    url = "http://model:5000/inference"
    files = {
        'file': (image_path, open(image_path, 'rb'), 'image/jpeg')
    }
    response = requests.post(url, files=files)
    return response

