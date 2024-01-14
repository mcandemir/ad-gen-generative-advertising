from PIL import Image, ImageDraw, ImageFilter, ImageFont
import aggdraw
import textwrap


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def adjust_punchline(draw, punchline: str, punchline_color: tuple):
    # TODO: rework
    FONT_SIZE = 48
    max_x1, max_x2, max_y1, max_y2 = 128, 896, 720, 900

    punchline_wrapped_rows = textwrap.wrap(punchline, ((max_x2 - max_x1) / (FONT_SIZE//2)))
    print(punchline_wrapped_rows)

    while len(punchline_wrapped_rows) > 5:
        FONT_SIZE -= 1
        punchline_wrapped_rows = textwrap.wrap(punchline, ((max_x2 - max_x1) / (FONT_SIZE//2)))

    # print(FONT_SIZE)
    font = ImageFont.FreeTypeFont('C:\Windows\Fonts\Caladea-Bold.ttf', FONT_SIZE)
    y1 = max_y1
    x1 = max_x1
    for punchline_row in punchline_wrapped_rows:
        x1 = 532 - font.getlength(punchline_row)//2
        draw.text((x1, y1), punchline_row, punchline_color, font=font)
        y1 += FONT_SIZE
    

def adjust_button(draw, button_text: str, button_color: tuple):
    # TODO: rework
    font = ImageFont.FreeTypeFont('C:\Windows\Fonts\Caladea-Bold.ttf', 40)

    box_x1, box_y1, box_x2, box_y2 = 512-160, 920, 512+160, 980

    offset = 512-(len(button_text) * ((40//2)//2))
    end = offset+font.getlength(button_text)

    draw.rounded_rectangle((offset, box_y1, end+20, box_y2), 15, button_color)
    draw.text((offset+10, 920+7), button_text, (255, 255, 255), font=font)