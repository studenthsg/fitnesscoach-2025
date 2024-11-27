import streamlit as st

st.markdown("Users")
st.sidebar.header("Users")

from supabase import create_client, Client
# Replace these with your Supabase project details
SUPABASE_URL = "https://qbnmfdcuzeghmyobcnhi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFibm1mZGN1emVnaG15b2JjbmhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI2OTg5NzcsImV4cCI6MjA0ODI3NDk3N30.FXophJC6_BilPfwJ8G1oI9Z_8UBqD9uf2UX0OgY3i00"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
