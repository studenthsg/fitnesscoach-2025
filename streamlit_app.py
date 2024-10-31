import streamlit as st
import requests 

st.title("Meal Planner 🍗")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
number = st.slider("How much fun is this project", 0, 100)

# Define query with an initial default value, such as an empty string
query = st.text_input("Enter a recipe keyword:", "")

#API link to app
API_URL = "https://api.spoonacular.com/recipes/complexSearch" #link to our API
API_KEY = "a636f339cbdb4409ae46bb47e0c35577"

def get_recipes(query):
    params = {"query": query, "apiKey": API_KEY}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Could not retrieve data. Please try again.")
        return None

# Get recipes when the user enters a search term
if query:
    recipes = get_recipes(query)
    if recipes:
        for recipe in recipes.get("results", []):
            st.write(recipe["title"])  # Display recipe titles