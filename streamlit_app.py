import streamlit as st
import requests

# API setup
API_URL = "https://api.spoonacular.com/recipes/complexSearch"
RECIPE_INFO_URL = "https://api.spoonacular.com/recipes/{id}/information"  # URL to get recipe details
API_KEY = "a636f339cbdb4409ae46bb47e0c35577"

# Initialize session state
if "saved_recipes" not in st.session_state:
    st.session_state["saved_recipes"] = {"Breakfast": [], "Lunch": [], "Dinner": []}
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "weekly_plan" not in st.session_state:
    st.session_state["weekly_plan"] = {}

# Sidebar navigation
if "sidebar_visible" not in st.session_state:
    st.session_state["sidebar_visible"] = False

if st.session_state["sidebar_visible"]:
    st.sidebar.title("My Nutrition Coach")
    page = st.sidebar.radio("Navigate", ["Home", "Recipe Generator", "My Recipes", "Weekly Planner", "My Account"])
else:
    page = "Home"

# Global definitions for both recipe generator and my recipes 
def get_recipes(query, min_calories, max_calories, dietary, exclude, cuisine, meal_type):
    params = {
        "query": query,
        "apiKey": API_KEY,
        "number": 10,
        "addRecipeInformation": True,
        "minCalories": min_calories,
        "maxCalories": max_calories,
        "cuisine": cuisine if cuisine else None,
        "type": meal_type if meal_type else None,
        "intolerances": ",".join([key for key, value in dietary.items() if value]),
        "excludeIngredients": exclude if exclude else None,
    }
    response = requests.get(API_URL, params=params)
    return response.json() if response.status_code == 200 else None

def get_recipe_details(recipe_id):
    url = RECIPE_INFO_URL.format(id=recipe_id)
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

# Home Page
if page == "Home":
    st.title("My Nutrition Coach 🥗")
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://media.istockphoto.com/id/586162072/photo/various-kitchen-utensils.jpg?s=612x612&w=0&k=20&c=auwz9ZHqkG_UlKw5y-8UqvMLznA2PySQ_Jt3ameL1aU='); 
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h2>Welcome to your personalized nutrition and fitness assistant!</h2>", unsafe_allow_html=True)

    if st.button("Let's Get Started!"):
        st.session_state["sidebar_visible"] = True

# Recipe Generator
elif page == "Recipe Generator":
    st.title("Recipe Generator 🍳")
    
    # User inputs
    query = st.text_input("Enter a recipe keyword:", "")
    dietary_preferences = {
        "Vegan": st.checkbox("Vegan"),
        "Vegetarian": st.checkbox("Vegetarian"),
        "Lactose-Free": st.checkbox("Lactose-Free"),
        "Gluten-Free": st.checkbox("Gluten-Free"),
    }
    exclude_ingredient = st.text_input("Exclude Ingredient (optional):", "")
    calorie_range = st.slider(
        "Calorie Range (optional):", min_value=0, max_value=2000, value=(0, 500), step=10
    )
    cuisine = st.selectbox(
        "Filter by Cuisine (optional):",
        options=["", "African", "Asian", "American", "European", "Italian", "Mexican", "Indian", "Mediterranean"],
        index=0,
    )
    meal_type = st.selectbox("Meal Type:", options=["Breakfast", "Lunch", "Dinner"], index=0)

    # Button to start the search
    search_pressed = st.button("Search")

    # Initialize session state to store search results and expanded details
    if "search_results" not in st.session_state:
        st.session_state["search_results"] = []  # Store recipes
        st.session_state["expanded_recipes"] = {}  # Track expanded recipe details

    # Perform search when the button is pressed
    if search_pressed:
        st.session_state["search_results"] = get_recipes(
            query,
            calorie_range[0],
            calorie_range[1],
            dietary_preferences,
            exclude_ingredient,
            cuisine,
            meal_type,
        ).get("results", [])

    # Display search results
    if st.session_state["search_results"]:
        for recipe in st.session_state["search_results"]:
            st.write(f"### {recipe['title']}")
            st.image(recipe.get("image", ""), width=250)
            nutrients = recipe.get("nutrition", {}).get("nutrients", [])
            calories = next((n["amount"] for n in nutrients if n["name"] == "Calories"), "N/A")
            
            # Updated to round and add "per meal"
            if calories != "N/A":
                calories = f"{round(calories)} kcal per meal"
            else:
                calories = "N/A per meal"

            st.write(f"**Calories:** {calories}")

            # Manage details toggle
            recipe_id = recipe["id"]
            if recipe_id not in st.session_state["expanded_recipes"]:
                st.session_state["expanded_recipes"][recipe_id] = False

            # Toggle visibility for recipe details
            toggle_details = st.checkbox(
                f"View Full Recipe for {recipe['title']}",
                key=f"details_{recipe_id}",
                value=st.session_state["expanded_recipes"][recipe_id],
            )
            st.session_state["expanded_recipes"][recipe_id] = toggle_details

            # Show full recipe details if toggled
            if st.session_state["expanded_recipes"][recipe_id]:
                details = get_recipe_details(recipe_id)
                if details:
                    st.write("#### Ingredients:")
                    for ingredient in details["extendedIngredients"]:
                        st.write(f"- {ingredient['original']}")
                    st.write("#### Instructions:")
                    for step in details.get("analyzedInstructions", [{}])[0].get("steps", []):
                        st.write(f"{step['number']}. {step['step']}")

                    # Save recipe to "My Recipes"
                    if meal_type:
                        if st.button(f"Save to My Recipes: {recipe['title']}", key=f"save_{recipe_id}"):
                            if recipe not in st.session_state["saved_recipes"][meal_type]:
                                st.session_state["saved_recipes"][meal_type].append(recipe)
                                st.success(f"{recipe['title']} added to {meal_type} recipes.")
                            else:
                                st.warning(f"{recipe['title']} is already in {meal_type} recipes.")
                    else:
                        st.warning("Please select a meal type to save this recipe.")
    else:
        if search_pressed:
            st.warning("No recipes found. Please adjust your search criteria.")

# My Recipes
elif page == "My Recipes":
    st.title("My Recipes 📒")
    for meal_type, recipes in st.session_state["saved_recipes"].items():
        with st.expander(f"{meal_type} Recipes ({len(recipes)})"):
            for recipe in recipes:
                st.write(f"### {recipe['title']}")
                st.image(recipe.get("image", ""), width=250)
                calories = next(
                    (n["amount"] for n in recipe.get("nutrition", {}).get("nutrients", []) if n["name"] == "Calories"),
                    "N/A"
                )
                # Updated to round and add "per meal"
                if calories != "N/A":
                    calories = f"{round(calories)} kcal per meal"
                else:
                    calories = "N/A per meal"

                st.write(f"**Calories:** {calories}")
