import streamlit as st
import requests

st.set_page_config(
    page_title="Home",
    page_icon="🏠"
)

st.title("Welcome to the Meal Planner")
st.sidebar.title("Meal Planner App")  
st.sidebar.success("Navigate through the pages above.")

st.markdown("Hello, and welcome! You’ve just discovered a space where the ordinary transforms into the extraordinary, where dreams take shape, and where you are at the heart of it all.")

st.markdown("Whether you’ve come to explore, to create, or simply to be inspired, this is a home designed for YOU. Here, innovation meets imagination, and every click brings you closer to something remarkable.")

st.markdown("Let this be your sanctuary of discovery, a place where every moment feels special, and every experience is tailored to leave a lasting impression.")

st.markdown("Relax, explore, and enjoy—because this isn’t just a website. It’s the start of something truly unforgettable.")

st.markdown("""
    <style>
        .background-image-area {
            height: 800px;
            background-image: url('st.markdown("""
    <style>
        .background-image-area {
            height: 600px; /* Consider using min-height for better scalability */
            background-image: url('https://media.istockphoto.com/id/586162072/photo/various-kitchen-utensils.jpg?s=612x612&w=0&k=20&c=auwz9ZHqkG_UlKw5y-8UqvMLznA2PySQ_Jt3ameL1aU=');
            background-size: cover; /* Ensures the image covers the area without distortion */
            background-position: center; /* Keeps the image centered */
            background-repeat: no-repeat; /* Prevents tiling of the image */
            display: flex; /* Makes it easier to add content inside, if needed */
            align-items: center; /* Centers child elements vertically if present */
            justify-content: center; /* Centers child elements horizontally if present */
            overflow: hidden; /* Hides overflow if necessary */
            border-radius: 8px; /* Adds subtle rounded corners for aesthetics */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
        }
    </style>
    """

    st.markdown('<div class="background-image-area"></div>', unsafe_allow_html=True)');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
    </style>
    <div class="background-image-area"></div>
    """, unsafe_allow_html=True)
