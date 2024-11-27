import streamlit as st
import requests

st.set_page_config(page_title="Home", page_icon="🍎")

st.title("Meal Planner 🍗")
st.sidebar.header("Home")
st.sidebar.success("Select a page above.")

st.markdown("Hello, and welcome! You’ve just discovered a space where the ordinary transforms into the extraordinary, where dreams take shape, and where you are at the heart of it all.")

st.markdown("Whether you’ve come to explore, to create, or simply to be inspired, this is a home designed for YOU. Here, innovation meets imagination, and every click brings you closer to something remarkable.")

st.markdown("Let this be your sanctuary of discovery, a place where every moment feels special, and every experience is tailored to leave a lasting impression.")

st.markdown("Relax, explore, and enjoy—because this isn’t just a website. It’s the start of something truly unforgettable.")

st.markdown("""
    <style>
        .background-image-area {
            height: 200px;
            background-image: url('https://www.creativefabrica.com/wp-content/uploads/2023/02/20/Unicorn-Farting-A-Rainbow-Graphic-61806034-1.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
    </style>
    <div class="background-image-area"></div>
    """, unsafe_allow_html=True)
