import streamlit as st
import requests

def intro():
    import streamlit as st

    st.title("Meal Planner 🍗")
    st.sidebar.success("Select a demo above.")

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
