import streamlit as st
from supabase import create_client, Client

# Set up Streamlit title
st.title("Account")

# Supabase configuration
SUPABASE_URL = "https://qbnmfdcuzeghmyobcnhi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFibm1mZGN1emVnaG15b2JjbmhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI2OTg5NzcsImV4cCI6MjA0ODI3NDk3N30.FXophJC6_BilPfwJ8G1oI9Z_8UBqD9uf2UX0OgY3i00"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to insert a user
def insert_user(username: str, password: str):
    try:
        # Interact with the "users" table
        response = supabase.table("users").insert({"username": username, "password": password}).execute()
        return response.data
    except Exception as e:
        return str(e)  # Return exception as a string for debugging

# Example call to insert a user
response = insert_user("john_doe_5", "secure_password123")

# Display the response in Streamlit
st.write(response)
