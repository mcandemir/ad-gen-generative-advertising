from img2img import Img2Img
import argparse


parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-i', '--image', type=str, help='path to your BASE image')
parser.add_argument('-p', '--prompt', type=str, help='BASE prompt to generate image')
parser.add_argument('-l', '--logo', type=str, help='path to your logo')
parser.add_argument('-c', '--color', type=str, help='include color in generated image')
parser.add_argument('-pl', '--punchline', type=str, help='a punchline text')
parser.add_argument('-pc', '--punchlinecolor', type=int, nargs='+', help='color of punchline text as RGB. (0, 90, 0) by default. Enter by integers.')
parser.add_argument('-b', '--button', type=str, help='a button text')
parser.add_argument('-bc', '--buttoncolor', type=int, nargs='+' ,help='color of button as RGB. (0, 190, 0) by default. Enter by integers.')


if __name__ == "__main__":
    img2img = Img2Img()

    imgpath = 'resources/adai2.png'
    prompt = 'a cardboard coffee cup on the table'
    color = 'red'

    punchline1 = "This is your chance to showcase your creativity and your brilliant ideas!If you're more about the actual game design, there are several titles wherein you are free able to make 'mods' or altered versions of existing games."
    punchline2 = "Creativity is seeing what others see and thinking what no one else ever thought."
    punchline3 = "Hello There! Obi-wan Kenobi.."
    punchline4 = "Hello!"

    button1 = "Buy now!"
    button2 = "Philosophy is pretty fun!"


    args = parser.parse_args()
    # ---------------------------
    if args.image:
        image_path = args.image
    else:
        image_path = 'resources/adai2.png'
    # ---------------------------
    if args.prompt:
        prompt = args.prompt
    else:
        prompt = prompt
    # ---------------------------
    if args.logo:
        logo_path = args.logo
    else:
        logo_path = 'resources/logo.png'
    # ---------------------------
    if args.color:
        color = args.color
    else:
        color = 'red'
    # ---------------------------
    if args.punchline:
        punchline = args.punchline
    else:
        punchline = punchline1
    # ---------------------------
    if args.punchlinecolor:
        print(args.punchlinecolor)
        punchline_color = tuple(args.punchlinecolor)
    else:
        punchline_color = (0, 90, 0)
    # ---------------------------
    if args.button:
        button = args.button
    else:
        button = button2
    # ---------------------------
    if args.buttoncolor:
        button_color = tuple(args.buttoncolor)
    else:
        button_color = (0, 190, 0)
    # ---------------------------

    img2img.generate_image_t1(imgpath=imgpath, prompt=prompt, color=color)

    img2img.generate_image_t2(
        logo_path=logo_path,
        punchline=punchline,
        punchline_color=punchline_color,
        button=button,
        button_color=button_color,
        )



