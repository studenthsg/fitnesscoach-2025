import streamlit as st

st.title("Meal Planner 🍗")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
number = st.slider("How much fun is this project", 0, 100)

#API link to app
API_URL = "https://api.spoonacular.com/recipes/complexSearch" #link to our API
API_KEY = "YOUR_API_KEY"

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
