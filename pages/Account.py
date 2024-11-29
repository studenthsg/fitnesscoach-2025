import streamlit as st
from supabase import create_client, Client

# Define Supabase credentials
SUPABASE_URL = "https://qbnmfdcuzeghmyobcnhi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFibm1mZGN1emVnaG15b2JjbmhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI2OTg5NzcsImV4cCI6MjA0ODI3NDk3N30.FXophJC6_BilPfwJ8G1oI9Z_8UBqD9uf2UX0OgY3i00"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Streamlit application UI
st.title("Account Management")

# Function to insert user into the database
def insert_user(username: str, password: str):
    try:
        # Insert a new user into the "users" table
        response = supabase.table("users").insert({"username": username, "password": password}).execute()
        return response.data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit form for user input
with st.form("user_form"):
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    submit_button = st.form_submit_button("Create Account")

# Handle form submission
if submit_button:
    if username and password:
        result = insert_user(username, password)
        if result:
            st.success("User successfully created!")
        else:
            st.error("Failed to create user.")
    else:
        st.warning("Please fill out both fields.")
