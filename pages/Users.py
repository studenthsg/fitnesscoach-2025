import streamlit as st


st.title("Users")
st.markdown("Users")
st.sidebar.header("Users")

st.set_page_config(
    page_title="Account",
    page_icon="🌶️",
)

st.write("You have entered", st.session_state["my_input"])
