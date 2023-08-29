import streamlit as st
import tempfile
import ffmpeg
import os
from PIL import Image
from typing import IO
from pydub import AudioSegment


def image_info(filename: str, temp_file: IO) -> None:
    with st.expander(filename):
        columns = st.columns(2)
        with columns[0]:
            img = Image.open(temp_file.name)
            st.image(img, caption=filename)
        with columns[1]:
            st.write("Image size:", img.size)
            st.write("Image format:", img.format)
            st.write("Image mode:", img.mode)
            st.write("Image info:", img.info)


def image_converter() -> None:
    output_format = st.selectbox(
        "Select output format", ["png", "jpg", "jpeg", "tiff", "tif", "bmp", "webp"]
    )
    uploaded_file = st.file_uploader(
        "Upload image",
        accept_multiple_files=False,
        type=["png", "jpg", "jpeg", "tiff", "tif", "bmp"],
    )
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as original_file:
            original_file.write(uploaded_file.read())
            image_info(uploaded_file.name, original_file)
    if st.button("Convert Image", use_container_width=True) and uploaded_file:
        img = Image.open(original_file.name)
        if img.mode == "RGBA" and output_format in ["jpg", "jpeg"]:
            img = img.convert("RGB")
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{output_format}"
        ) as converted_file:
            img.save(converted_file.name)
            st.success("Image converted successfully!")
            download_name = f"{uploaded_file.name.split('.')[0]}.{output_format}"
            image_info(download_name, converted_file)
            st.download_button(
                "Download converted image",
                converted_file.name,
                file_name=download_name,
            )


def video_converter() -> None:
    output_format = st.selectbox(
        "Select output format", ["mp4", "webm", "ogg", "mov", "avi"]
    )
    uploaded_file = st.file_uploader(
        "Upload video",
        accept_multiple_files=False,
        type=["mp4", "webm", "ogg", "mov", "avi"],
    )
    if uploaded_file:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}"
        ) as original_file:
            original_file.write(uploaded_file.read())
    if st.button("Convert Video", use_container_width=True) and uploaded_file:
        output_filename = f"/tmp/output.{output_format}"
        with st.spinner("Converting video..."):
            ffmpeg.input(original_file.name).output(output_filename).run()
        st.success("Video converted successfully!")
        st.download_button(
            "Download converted video",
            open(output_filename, "rb").read(),
            file_name=f"{uploaded_file.name.split('.')[0]}.{output_format}",
        )
        os.remove(output_filename)


def audio_converter() -> None:
    output_format = st.selectbox(
        "Select output format", ["mp3", "wav", "ogg", "flac", "m4a"]
    )
    uploaded_file = st.file_uploader(
        "Upload audio",
        accept_multiple_files=False,
        type=["mp3", "wav", "ogg", "flac", "m4a"],
    )
    if uploaded_file:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}"
        ) as original_file:
            original_file.write(uploaded_file.read())

    if st.button("Convert Audio", use_container_width=True) and uploaded_file:
        audio = AudioSegment.from_file(original_file.name)
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{output_format}"
        ) as converted_file:
            audio.export(converted_file.name, format=output_format)
        st.success("Audio converted successfully!")
        st.download_button(
            "Download converted audio",
            open(converted_file.name, "rb").read(),
            file_name=f"{uploaded_file.name.split('.')[0]}.{output_format}",
        )


def main():
    st.title("Format Fusion")
    image_tab, video_tab, audio_tab = st.tabs(["Image", "Video", "Audio"])
    with image_tab:
        image_converter()
    with video_tab:
        video_converter()
    with audio_tab:
        audio_converter()


if __name__ == "__main__":
    main()
