import requests

def denoise_image(image_file):
    url = "http://model:5000/inference"
    files = {"file": image_file}
    response = requests.post(url, files=files)
    return response.json()