import streamlit as st


st.title("User")
st.markdown("Users")
st.sidebar.header("Users")

st.write("You have entered", st.session_state["my_input"])
