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

    st.markdown("Hello, and welcome! You’ve just discovered a space where the ordinary transforms into the extraordinary, where dreams take shape, and where you are at the heart of it all.")

    st.markdown("Whether you’ve come to explore, to create, or simply to be inspired, this is a home designed for YOU. Here, innovation meets imagination, and every click brings you closer to something remarkable.")

    st.markdown("Let this be your sanctuary of discovery, a place where every moment feels special, and every experience is tailored to leave a lasting impression.")

    st.markdown("Relax, explore, and enjoy—because this isn’t just a website. It’s the start of something truly unforgettable.")

    # Injecting CSS for the background-image-area class
    st.markdown("""
        <style>
            .background-image-area {
                height: 300px;
                background-image: url('https://media.istockphoto.com/id/586162072/photo/various-kitchen-utensils.jpg?s=612x612&w=0&k=20&c=auwz9ZHqkG_UlKw5y-8UqvMLznA2PySQ_Jt3ameL1aU=');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
            }
        </style>
    """, unsafe_allow_html=True)

    # Creating a div with the class background-image-area
    st.markdown('<div class="background-image-area"></div>', unsafe_allow_html=True)

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

    import supabase
    from supabase import create_client, Client

    SUPABASE_URL = "https://qbnmfdcuzeghmyobcnhi.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFibm1mZGN1emVnaG15b2JjbmhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI2OTg5NzcsImV4cCI6MjA0ODI3NDk3N30.FXophJC6_BilPfwJ8G1oI9Z_8UBqD9uf2UX0OgY3i00"

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Initialize session state for login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_data = None

    # Function to insert a new user
    def insert_user(username: str, password: str, name: str):
        try:
            response = supabase.table("users").insert({
                "username": username,
                "password": password,
                "name": name
            }).execute()
            return response.data
        except Exception as e:
            return e

    # Function to display user profile and allow updating weight and height
    def display_profile(user_data):
        st.subheader("Profile Information")
        st.write(f"**Name:** {user_data.get('name', 'N/A')}")
        st.write(f"**Username:** {user_data.get('username', 'N/A')}")

        # Input fields for weight and height
        weight = st.number_input("Enter your weight (kg):", min_value=0.0, step=0.1, key="weight")
        height = st.number_input("Enter your height (cm):", min_value=0.0, step=0.1, key="height")

        if st.button("Save Weight and Height"):
            try:
                # Update the user's weight and height in the database
                response = supabase.table("users").update({"weight": weight, "height": height}).eq("username", user_data["username"]).execute()
                if response.data:
                    st.success("Weight and height updated successfully!")
                else:
                    st.error("Failed to update weight and height.")
            except Exception as e:
                st.error(f"Error: {e}")

    if not st.session_state.logged_in:
        # Tabs for Login and Registration
        tab1, tab2 = st.tabs(["Login", "Register"])

        # Login tab
        with tab1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login"):
                try:
                    # Retrieve user profile after login
                    response = supabase.table("users").select("*").eq("username", login_username).eq("password", login_password).execute()
                    if response.data:
                        user_data = response.data[0]  # Get the first matching user
                        st.session_state.logged_in = True  # Mark user as logged in
                        st.session_state.user_data = user_data  # Store user data
                        st.success("Login successful!")
                    else:
                        st.error("Invalid username or password.")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Registration tab
        with tab2:
            st.subheader("Register")
            reg_name = st.text_input("Name", key="reg_name")
            reg_username = st.text_input("Username", key="reg_username")
            reg_password = st.text_input("Password", type="password", key="reg_password")

            if st.button("Register"):
                if reg_name and reg_username and reg_password:
                    response = insert_user(reg_username, reg_password, reg_name)
                    if isinstance(response, list):  # Successful registration returns a list of inserted rows
                        st.session_state.logged_in = True  # Mark user as logged in
                        st.session_state.user_data = {"name": reg_name, "username": reg_username}  # Store user data
                        st.success("User registered successfully!")
                    else:
                        st.error(f"Error: {response}")
                else:
                    st.error("Please fill in all fields (Name, Username, and Password).")
    else:
        # Display profile if logged in
        display_profile(st.session_state.user_data)
