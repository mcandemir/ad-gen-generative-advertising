from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import base64
from img2img import Img2Img
from fastapi.responses import FileResponse


class GenerationRequest(BaseModel):
    # request structure
    image64: str | None = None
    prompt: str
    logo64: str | None = None
    color: str   
    punchline: str
    punchline_color: list[int]
    button: str
    button_color: list[int]


# define fastapi application
app = FastAPI()


@app.post("/generate")
async def generate_image(generation_request: GenerationRequest):
    image64 = generation_request.image64
    if generation_request.image64 is None or generation_request.image64 == "" or generation_request.image64 == "string":
        with open('resources/adai2.png', 'rb') as image_file:
            image64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    
    logo64 = generation_request.logo64
    if generation_request.logo64 is None or generation_request.logo64 == "" or generation_request.logo64 == "string":
        with open('resources/logo.png', 'rb') as logo_file:
            logo64 = base64.b64encode(logo_file.read()).decode('utf-8')


    img2img = Img2Img()
    img2img.generate_image_t1(
        imgpath=None,
        prompt=generation_request.prompt,
        color=generation_request.color,
        image64=image64
    )

    img2img.generate_image_t2(
        logo_path=None,
        punchline=generation_request.punchline,
        punchline_color=tuple(generation_request.punchline_color),
        button=generation_request.button,
        button_color=tuple(generation_request.button_color),
        logo64=logo64
    )


    return FileResponse('generated_ads/creation.png')
