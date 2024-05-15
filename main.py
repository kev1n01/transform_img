import streamlit as st
import cv2
import numpy as np
from streamlit_drawable_canvas import st_canvas
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def upload_image():
    img_upload = st.file_uploader("Subir imagen", type=['jpg', 'png', 'jpeg'], label_visibility='visible')
    if img_upload is not None:
        bytes = np.asarray(bytearray(img_upload.read()), dtype=np.uint8)
        img = cv2.imdecode(bytes, cv2.IMREAD_COLOR)
        return img

def convert_image_to_grey(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def convert_binary_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

def resize_image(image, size):
    img_resized = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    _, img_binary = cv2.threshold(img_resized, 127, 255, cv2.THRESH_BINARY)
    return img_binary

def create_canvas(image):
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        background_image=image,
        update_streamlit=True,
        height=50,
        width=50,
        drawing_mode="none",
        key="canvas"
    )
    return canvas_result

def draw_from_matplotlib(image):
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.imshow(image, cmap='binary', extent=[0, 50, 0, 50])

    ax.set_xticks(np.arange(0, 51, 1))
    ax.set_yticks(np.arange(0, 51, 1))
    ax.grid(which='both', color='gray', linestyle='-', linewidth=0.5)

    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)
    for i in range(50):
        for j in range(50):
            pixel_value = image[i, j]
            rect = Rectangle((j, i), 1, 1, linewidth=0.5, edgecolor='red', facecolor='none')
            ax.add_patch(rect)
    return fig

def main():
    st.title("Modificación de imágenes")
    img = upload_image()
    if img is not None:
        col1, col2 = st.columns(2)
        with st.container():
            with col1:
                st.image(img, caption='Imagen original', use_column_width=True)
            with col2:
                img_grey = convert_image_to_grey(img)
                st.image(img_grey, caption='Imagen escala de grises', use_column_width=True)
              
        with st.container():
            st.header('Canvas 50 x 50 de la imagen subida')
            img_binary = resize_image(img_grey, (50, 50))
            st.pyplot(draw_from_matplotlib(img_binary))

if __name__ == '__main__':
    main()