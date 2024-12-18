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

# Global definitions 
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
            background-image: url('https://www.google.com/url?sa=i&url=https%3A%2F%2Fstablediffusionweb.com%2Fimage%2F17629250-anime-style-healthy-food-exercise-collage&psig=AOvVaw3kdWUZySA12O9QHMwy07Ef&ust=1732631421935000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCJjI6ZXZ94kDFQAAAAAdAAAAABAE'); 
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

    # Fetch and display recipes (first part already in global definitions)

    if query:
        recipes = get_recipes(query, calorie_range[0], calorie_range[1], dietary_preferences, exclude_ingredient, cuisine, meal_type)
        if recipes and "results" in recipes:
            for recipe in recipes["results"]:
                if query.lower() in recipe["title"].lower():
                    st.write(f"### {recipe['title']}")
                    st.image(recipe.get("image", ""), width=250)
                    nutrients = recipe.get("nutrition", {}).get("nutrients", [])
                    calories = next((n["amount"] for n in nutrients if n["name"] == "Calories"), "N/A")
                    st.write(f"**Calories:** {calories} kcal")

                    # View recipe details
                    show_details = st.checkbox(f"View Full Recipe for {recipe['title']}", key=f"details_{recipe['id']}")
                    if show_details:
                        details = get_recipe_details(recipe["id"])
                        if details:
                            st.write("#### Ingredients:")
                            for ingredient in details["extendedIngredients"]:
                                st.write(f"- {ingredient['original']}")
                            st.write("#### Instructions:")
                            for step in details.get("analyzedInstructions", [{}])[0].get("steps", []):
                                st.write(f"{step['number']}. {step['step']}")

                            # Display user-selected filters
                            st.write("#### Filters and Categories:")
                            st.write(", ".join([key for key, value in dietary_preferences.items() if value]))
                            st.write(f"**Meal Type:** {meal_type or 'N/A'}")
                            st.write(f"**Cuisine:** {cuisine or 'N/A'}")

                            # Save to "My Recipes"
                            if meal_type:  # Ensure meal_type is selected
                                if st.button(f"Save to My Recipes: {recipe['title']}", key=f"save_{recipe['id']}"):
                                    if recipe not in st.session_state["saved_recipes"][meal_type]:
                                        st.session_state["saved_recipes"][meal_type].append(recipe)
                                        st.success(f"{recipe['title']} added to {meal_type} recipes.")
                                    else:
                                        st.warning(f"{recipe['title']} is already in {meal_type} recipes.")
                            else:
                                st.warning("Please select a meal type to save this recipe.")

# My Recipes
elif page == "My Recipes":
    st.title("My Recipes 📒")
    for meal_type, recipes in st.session_state["saved_recipes"].items():
        st.subheader(f"{meal_type} Recipes")
        for recipe in recipes:
            st.write(f"### {recipe['title']}")
            st.image(recipe.get("image", ""), width=250)
            calories = next((n["amount"] for n in recipe.get("nutrition", {}).get("nutrients", []) if n["name"] == "Calories"), "N/A")
            st.write(f"**Calories:** {calories} kcal")

            # View recipe details
            if st.checkbox(f"View Full Recipe for {recipe['title']}", key=f"view_{recipe['id']}"):
                details = get_recipe_details(recipe["id"])  # Ensure this function is defined earlier
                if details:
                    st.write("#### Ingredients:")
                    for ingredient in details["extendedIngredients"]:
                        st.write(f"- {ingredient['original']}")
                    st.write("#### Instructions:")
                    for step in details.get("analyzedInstructions", [{}])[0].get("steps", []):
                        st.write(f"{step['number']}. {step['step']}")

# Weekly Planner 
if page == "Weekly Planner":
    st.title("Weekly Planner 📅")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meals = ["Breakfast", "Lunch", "Dinner"]

    for day in days:
        st.write(f"### {day}")
        col1, col2, col3 = st.columns(3)
        total_calories = 0

        for col, meal in zip([col1, col2, col3], meals):
            with col:
                selected_recipe = st.selectbox(
                    f"{meal}:", 
                    ["None"] + [recipe["title"] for recipe in st.session_state["saved_recipes"][meal]],
                    key=f"{day}_{meal}"
                )
                if selected_recipe != "None":
                    recipe = next(
                        (recipe for recipe in st.session_state["saved_recipes"][meal] if recipe["title"] == selected_recipe),
                        None
                    )
                    if recipe:
                        calories = next(
                            (n["amount"] for n in recipe.get("nutrition", {}).get("nutrients", []) if n["name"] == "Calories"), 
                            0
                        )
                        total_calories += calories

        st.write(f"**Total Calories for {day}: {total_calories} kcal**")

# My Account
elif page == "My Account":
    st.title("My Account 🧑‍💻")

    # Initialize session state for accounts
    if "accounts" not in st.session_state:
        st.session_state["accounts"] = {}  # Format: {"username": {"name": "Name", "password": "Password"}}

    if not st.session_state["logged_in"]:
        # Log In Section
        st.subheader("Log In")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_btn = st.button("Log In")

        if login_btn:
            if username in st.session_state["accounts"] and st.session_state["accounts"][username]["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = username
                st.success("Logged in successfully!")
            else:
                st.error("Wrong username or password. Please try again.")

        # Create Account Section
        st.subheader("Create Account")
        name = st.text_input("Name", key="create_name")
        new_username = st.text_input("Username", key="create_username")
        new_password = st.text_input("Password", type="password", key="create_password")
        create_btn = st.button("Create Account")

        if create_btn:
            if name and new_username and new_password:
                if new_username in st.session_state["accounts"]:
                    st.error("Username already exists. Please choose a different one.")
                else:
                    st.session_state["accounts"][new_username] = {"name": name, "password": new_password}
                    st.success("Account created successfully!")
            else:
                st.error("All fields must be filled out to create an account.")

    else:
        # After Login
        user_name = st.session_state["accounts"][st.session_state["current_user"]]["name"]
        st.markdown(f"### Welcome, {user_name}!")
        st.button("Log Out", on_click=lambda: st.session_state.update({"logged_in": False, "current_user": None}))

