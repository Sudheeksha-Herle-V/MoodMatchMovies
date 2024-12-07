import streamlit as st
from PIL import Image
import numpy as np
import cv2
from keras.models import model_from_json
from support import *  # Assuming all your support functions like `get_all_recom` are in this file

# Emotion dictionary
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# Set page config
st.set_page_config(
    page_title="MoodMatch Movies",
    layout="wide",  # Use a wide layout
    initial_sidebar_state="collapsed",
)

def landing_page():
    st.markdown(
    """
    <style>
        body {
            margin: 0 !important;
            padding: 0 !important;
            background-color: #171430 !important;
            height: 100vh;
            color: white;
            overflow-x: hidden;
        }

        .main {
            padding: 0 !important;
        }

        .block-container {
            padding: 0 !important;
            margin: 0 auto !important;
            width: 100% !important;
        }

        header {
            background-color: #B9B0EB !important;
            color: black !important;
        }

        header .css-1q8dd3e {
            color: white !important;
        }

        .css-18ni7ap.e8zbici2 {
            background-color: #171430 !important;
            color: white !important;
        }

        footer {
            background: transparent !important;
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="background: linear-gradient(to bottom, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0)), #8271DC; height: 100vh; display: flex; justify-content: center; align-items: center;">
            <div style="background-color: #171430; color: white; border-radius: 15px; padding: 80px; text-align: center; width: 70%; box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), 0 10px 20px rgba(0, 0, 0, 0.4);">
                <h1 style="margin-bottom: 20px;">MoodMatch Movies</h1>
                <p style="font-size: 18px;">Find movies that match your mood!</p>
                <a href="?page=main" style="background-color: #5533D4; padding: 10px 20px; color: white; text-decoration: none; border-radius: 10px; font-size: 16px;">Click to Get Started</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Main page function
def main_page():
    st.markdown(
        """
        <style>
            .head {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: #5533D4;
                z-index: 1000;
                padding: 10px;
                margin: 40px 0;
                padding-left: 80px;
            }

            header h2 {
                margin: 0;
                color: white;
            }

            .stColumn {
                padding-right: 30px;
            }

            .stColumn2 {
                padding-left: 30px;
            }

            .movie-row {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                margin-bottom: 20px;  /* Reduced space between rows */
            }

            .movie-item {
                width: 30%;
                margin-bottom: 10px;  /* Reduced space between movies */
                text-align: center;
            }

            .movie-item img {
                width: 100%;
                height: 400px;
                width: 200px;
            }

            .genre-header {
                font-size: 22px;
                color: #5533D4;
                margin-bottom: 10px;  /* Reduced space after genre header */
            }

            .movie-title {
                font-weight: bold;
                font-size: 16px;
                margin-top: 5px;  /* Reduced margin */
            }

            .movie-genre {
                font-size: 14px;
                color: #888;
                margin-top: 3px;  /* Reduced margin for genre */
            }
        </style>
        """, unsafe_allow_html=True)

    # Fixed header
    st.markdown("""<div class="head"><header><h2>MoodMatch Movies</h2></header></div>""", unsafe_allow_html=True)

    # Create two columns with spacing
    col1, col2 = st.columns([1, 2])  # 1/3 for left column, 2/3 for right column

    # Left Column: Sidebar content
    with col1:
        # Color selection
        st.markdown("""<br><br>
        <h4 style="background-color: #5533D4; padding: 10px 20px; color: white; border-radius: 10px; font-size: 18px;">Select Colors</h4><br>
        """, unsafe_allow_html=True)

        color_select1 = st.selectbox("Select Color 1", ["Black", "White", "Red", "Yellow", "Blue"], key=1)
        color_select2 = st.selectbox("Select Color 2", ["Black", "White", "Red", "Yellow", "Blue"], key=2)
        color_select3 = st.selectbox("Select Color 3", ["Black", "White", "Red", "Yellow", "Blue"], key=3)

        st.markdown("""<br>
        <h4 style="background-color: #5533D4; padding: 10px 20px; color: white; border-radius: 10px; font-size: 18px;">Capture image</h4><br><br>
        """, unsafe_allow_html=True)

        img_file_buffer = st.camera_input("Capture Image", label_visibility="collapsed")
        
        suggest_button = st.button("Suggest Movies", key="suggest_button")

    # Right Column: Main content
    with col2:
        emotion_detected = None
        emotion_id = None
        
        if suggest_button:
            if img_file_buffer is not None:
                image = Image.open(img_file_buffer)
                cv2_img = np.array(image)

                try:
                    # Detect emotion
                    img, emotion_id = detect_emotion(cv2_img)  # Replace with actual function
                    if img is not None and emotion_id is not None:
                        st.markdown(
                            f'<br><br><h4 style="background-color: #5533D4; padding: 10px 20px; color: white; border-radius: 10px; font-size: 18px;">Detected Emotion: {emotion_dict[emotion_id]}</h4>',
                            unsafe_allow_html=True
                        )

                        # Get colors from the left column
                        all_colors = [color_select1, color_select2, color_select3]

                        # Get movie recommendations
                        all_movie_names, all_poster_links, all_genres = get_all_recom(all_colors, emotion_id)

                        st.markdown("<h3>Recommended Movies:</h3>", unsafe_allow_html=True)

                        if all_movie_names:
                            # Display movies in rows
                            for i in range(0, len(all_movie_names), 3):
                                col1, col2, col3 = st.columns(3)
                                for j, col in enumerate([col1, col2, col3]):
                                    movie_index = i + j
                                    if movie_index < len(all_movie_names):
                                        name = all_movie_names[movie_index]
                                        poster = all_poster_links[movie_index]
                                        genre = all_genres[movie_index]
                                        with col:
                                            st.markdown(f"<b>{name}</b>", unsafe_allow_html=True)
                                            st.image(poster, width=200)
                                            st.markdown(f"<span class='movie-genre'>{genre}</span>", unsafe_allow_html=True)
                                st.markdown("<br><br>", unsafe_allow_html=True)  # Space between rows
                        else:
                            st.warning("No movie recommendations found for the detected emotion.")
                    else:
                        st.error("Could not detect emotion.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please capture an image first!")


def detect_emotion(img):
    try:
        with open('model/model.json', 'r') as json_file:
            loaded_model_json = json_file.read()
        emotion_model = model_from_json(loaded_model_json)
        emotion_model.load_weights('model/model.h5')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

    try:
        face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            return img, maxindex
    except Exception as e:
        st.error(f"Error during emotion detection: {e}")
        return None, None

# Check for query params
query_params = st.query_params
page = query_params.get("page", "landing")  # Default to 'landing' if not present

if page == "landing":
    landing_page()
elif page == "main":
    main_page()
else:
    st.error("Invalid page parameter. Please check the URL.")
    landing_page()  # Fall back to landing page
