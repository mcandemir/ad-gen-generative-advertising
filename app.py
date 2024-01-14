import streamlit as st
import requests
from PIL import ImageColor
from PIL import Image
import base64
from io import BytesIO
import json

st.set_page_config(layout='wide')

with st.sidebar:
    st.title('AdGen')

    st.markdown('Generative Advertising is the future advertising!')

    st.title(' ')

    st.markdown('## Example Inputs:')

    st.markdown("""

    **Prompt**: \n 
    - a cardboard coffee cup on the table

    **Punchline**: \n
    - Creativity is seeing what others see and thinking what no one else ever thought.

    **Button**: \n
    - Philosophy is fun!
                
    **Color**: \n
    - Red

    """)

    st.title(' ')
    st.title(' ')

    cols = st.sidebar.columns(6)

    with cols[1]:
        st.write("""<div style="width:100%;text-align:center;"><a href="https://portfolio-mcandemir.vercel.app/" style="float:center"><img src="https://raw.githubusercontent.com/mcandemir/portfolio/master/img/favicon/mcandemir.png" width="42px"></img></a></div>""", unsafe_allow_html=True)
        
    with cols[2]:
        st.write("""<div style="width:100%;text-align:center;"><a href="https://www.linkedin.com/in/mehmet-can-demir/" style="float:center"><img src="https://images.rawpixel.com/image_png_1100/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjk4Mi1kMS0xMC5wbmc.png" width="42px"></img></a></div>""", unsafe_allow_html=True)
        
    with cols[3]:
        st.write("""<div style="width:100%;text-align:center;"><a href="https://github.com/mcandemir" style="float:center"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="42px"></img></a></div>""", unsafe_allow_html=True)


# define generation state
if 'generated' not in st.session_state:
    st.session_state['generated'] = False

if 'request' not in st.session_state:
    st.session_state['request'] = False

if 'response' not in st.session_state:
    st.session_state['response'] = None




# callback
def set_generated_state():
    st.session_state['generated'] = True
    send_request()


# convert img to base64
def PIL_img_to_base64(img):
    try:
        encoded = base64.b64encode(img.getvalue()).decode('utf-8')
    except:
        imgByteArr = BytesIO()
        img.save(imgByteArr, format=img.format)
        encoded = base64.b64encode(imgByteArr.getvalue()).decode('utf-8')
    return encoded


# send request
def send_request():

    payload = {
            "image64": str(PIL_img_to_base64(base_image)),
            "prompt": prompt_input,
            "logo64": str(PIL_img_to_base64(base_logo)),
            "color": color_input,
            "punchline": punchline_input,
            "punchline_color": list(ImageColor.getcolor(punchline_color_input, 'RGB')),
            "button": button_input,
            "button_color": list(ImageColor.getcolor(button_color_input, 'RGB'))
            }

    # # payload logs for debuggind
    # load = json.dumps(payload)
    # with open('payload.json', 'w') as f:
    #     f.write(load)

    st.session_state['response'] = requests.post(
        url='http://127.0.0.1:81/generate',
        json=payload
    )




# build page
col1, col2, col3, col4, col5 = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])

with col3:
    st.markdown('# AdGen')

st.markdown("""---""")

st.markdown('### Parameters')

col1, col2, col3, col4, col5, col6 = st.columns([0.2, 0.01, 0.2, 0.1, 0.2, 0.2])


with col1:
    st.markdown('### ')
    prompt_input = st.text_area('**Prompt:**', value="a cardboard coffee cup on the table")
    punchline_input = st.text_area('**Punchline:**', value="Creativity is seeing what others see and thinking what no one else ever thought.", max_chars=138)
    button_input = st.text_area('**Button Text:**', value="Philosophy is fun!")

with col3:
    st.markdown('### ')
    color_input = st.text_input('**Color (to be used in generated image):**')
    punchline_color_input = st.color_picker('**Punchline color:**')
    button_color_input = st.color_picker('**Button color:**')
    base_image = st.file_uploader('**Base image:**')
    base_logo = st.file_uploader('**Logo image with a white background:**')
    

with col5:
    st.markdown('### Base image preview:')
    
    if base_image:
        st.image(base_image, width=256)
    else:
        base_image = Image.open('resources/adai2.png')
        st.image(base_image, width=256)

    st.title(' ')
    st.title(' ')

    st.button('Generate Ad!', use_container_width=True, on_click=set_generated_state)

with col6:
    st.markdown('### Base logo preview:')
    
    if base_logo:
        st.image(base_logo, width=256)
    else:
        base_logo = Image.open('resources/logo.png')
        st.image('resources/logo.png', width=256)




# Show generated image
if st.session_state['generated']:

    st.markdown("""---""")

    st.markdown('### Generated Ad:')
    
    st.title(' ')

    st.image('generated_ads/creation.png', width=768)






