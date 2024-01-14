import json
import requests
import io
import base64
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from utils import add_corners, adjust_punchline, adjust_button


class Img2Img:
    def __init__(self) -> None:
        # define an endpoint and a base payload for the stable-diffusion-web-ui api
        self.BASE_URL = "http://127.0.0.1:7860"
        self.BASE_PAYLOAD = {
            "prompt": "",
            "steps": 25,
            "init_images": [
                ""
            ],
            "override_settings": {
                "sd_model_checkpoint": "realvisxlV20_v20Bakedvae.safetensors",
                "CLIP_stop_at_last_layers": 2,
            }
        }

    def generate_image_t1(self, imgpath, prompt, color, image64=None):
        # create and add the prompt to payload
        self.BASE_PAYLOAD['prompt'] = prompt + f', use {color} color.'

        # read and encode the base image in base64, then add to payload
        if imgpath:
            with open(imgpath, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        else:
            encoded_string = image64

        self.BASE_PAYLOAD['init_images'] = [encoded_string]


        # send the request
        r = requests.post(url=f'{self.BASE_URL}/sdapi/v1/img2img', json=self.BASE_PAYLOAD)
        r = r.json()

        # save request log for future debug
        formatted = json.dumps(r)
        with open('response.json', 'w') as f:
            json.dump(formatted, f)

        # save image if successfull
        try:
            image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
            image.save('generated_images/output.png')
            print('image saved')
        except:
            print('failed')

    def generate_image_t2(self, logo_path, punchline, punchline_color, button, button_color, logo64):
        # read resources
        img_from_t1 = Image.open('generated_images/output.png')
        canvas = Image.open('resources/canvas.png')
        if logo_path:
            logo = Image.open(logo_path)
        else:
            logo = Image.open(io.BytesIO(base64.b64decode(logo64)))

        # set LINE options
        LINE1_COOR = (32, 0, 992, 0)
        LINE2_COOR = (32, 1024, 992, 1024)
        LINE_COLOR = punchline_color
        LINE_WIDTH = 15
        LINE_CIRCLE_WIDTH = 8
        LINE1_CIRCLE1_COOR, LINE1_CIRCLE2_COOR = (32, 0), (992, 0)
        LINE2_CIRCLE1_COOR, LINE2_CIRCLE2_COOR = (32, 1024), (992, 1024)

        # set PUNCHLINE options
        PUNCHLINE_COLOR = punchline_color
        PUNCHLINE_TEXT = punchline

        # set BUTTON options
        BUTTON_COLOR = button_color

        # draw rounded template lines
        draw = ImageDraw.Draw(canvas)
        draw.line(LINE1_COOR, fill=LINE_COLOR, width=LINE_WIDTH)
        draw.line(LINE2_COOR, fill=LINE_COLOR, width=LINE_WIDTH)

        def circle(draw, center, radius, fill):
            draw.ellipse((center[0] - radius + 1, center[1] - radius + 1, center[0] + radius - 1, center[1] + radius - 1), fill=fill, outline=None)

        circle(draw, LINE1_CIRCLE1_COOR, LINE_CIRCLE_WIDTH, LINE_COLOR)
        circle(draw, LINE1_CIRCLE2_COOR, LINE_CIRCLE_WIDTH, LINE_COLOR)
        circle(draw, LINE2_CIRCLE1_COOR, LINE_CIRCLE_WIDTH, LINE_COLOR)
        circle(draw, LINE2_CIRCLE2_COOR, LINE_CIRCLE_WIDTH, LINE_COLOR)

        # create rounded corners
        img_from_t1 = add_corners(img_from_t1, 40)

        # paste logo
        logo.thumbnail((256, 256), Image.LANCZOS)
        canvas.paste(logo, ((512 - logo.size[0]//2), 23))

        # paste corner rounded image
        # img_from_t1.thumbnail((360, 360), Image.LANCZOS)
        canvas.paste(img_from_t1, ((256, 200)), img_from_t1)

        # punchline
        # font = ImageFont.FreeTypeFont('C:\Windows\Fonts\Caladea-Bold.ttf', 48)
        # draw.text((128, 740), PUNCHLINE_TEXT, (0, 120, 0), font=font)
        adjust_punchline(draw, punchline, punchline_color)

        # button
        adjust_button(draw, button, button_color)

        # result
        canvas.save('generated_ads/creation.png')

        