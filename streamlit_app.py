import streamlit as st
import requests

# App title
st.title("Meal Planner 🍗")

from supabase import create_client, Client
SUPABASE_URL = "https://qbnmfdcuzeghmyobcnhi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFibm1mZGN1emVnaG15b2JjbmhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI2OTg5NzcsImV4cCI6MjA0ODI3NDk3N30.FXophJC6_BilPfwJ8G1oI9Z_8UBqD9uf2UX0OgY3i00"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_user(username: str, password: str):
try:
response = supabase.table("users").insert({"username": username,
"password": password}).execute()
return response.data
except Exception as e:
return e
insert_user("john_doe_5", "secure_password123")

# API setup
API_URL = "https://api.spoonacular.com/recipes/complexSearch"
RECIPE_INFO_URL = "https://api.spoonacular.com/recipes/{id}/information"  # URL to get recipe details
API_KEY = "a636f339cbdb4409ae46bb47e0c35577"

# User input for recipe search
query = st.text_input("Enter a recipe keyword:", "")
max_calories = st.slider("Maximum Calories (optional):", min_value=0, max_value=2000, value=500, step=10)
min_calories = st.slider("Minimum Calories (optional):", min_value=0, max_value=max_calories, value=0, step=10)  # Dynamic max set by max_calories

# Function to fetch recipes from the API
def get_recipes(query, min_calories=None, max_calories=None):
    params = {
        "query": query,
        "apiKey": API_KEY,
        "number": 10,  # number of results to fetch
        "addRecipeInformation": True,
        "minCalories": min_calories if min_calories else None,
        "maxCalories": max_calories if max_calories else None
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Could not retrieve data. Please try again.")
        return None

# Function to fetch full recipe details
def get_recipe_details(recipe_id):
    url = RECIPE_INFO_URL.format(id=recipe_id)
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Could not retrieve full recipe details.")
        return None

# Display recipes based on the user's query and input criteria
if query:
    with st.spinner("Fetching recipes..."):
        recipes = get_recipes(query, min_calories, max_calories)
        
    if recipes and "results" in recipes:
        st.subheader("Results:")
        for recipe in recipes["results"]:
            st.write(f"### {recipe['title']}")
            if "image" in recipe:
                st.image(recipe["image"], width=250)
            
            # Display basic nutritional data if available
            if "nutrition" in recipe:
                nutrients = recipe["nutrition"].get("nutrients", [])
                calories = next((n["amount"] for n in nutrients if n["name"] == "Calories"), "N/A")
                st.write(f"**Calories:** {calories} kcal")
            else:
                st.write("Nutrition information not available.")

            # Toggle display of full recipe details
            show_details = st.checkbox(f"View Full Recipe for {recipe['title']}", key=recipe['id'])
            if show_details:
                recipe_details = get_recipe_details(recipe['id'])
                if recipe_details:
                    st.write("#### Ingredients:")
                    for ingredient in recipe_details["extendedIngredients"]:
                        st.write(f"- {ingredient['original']}")
                    
                    st.write("#### Instructions:")
                    for step in recipe_details["analyzedInstructions"][0]["steps"]:
                        st.write(f"{step['number']}. {step['step']}")
                
               
    else:
        st.info("No recipes found. Please adjust your search criteria.")
