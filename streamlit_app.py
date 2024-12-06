# The app can be accessed via the following link: https://food2025.streamlit.app
# The app requires streamlit, supabase, scikit-learn, pandas and numpy.

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

# Sidebar
st.sidebar.title("My Nutrition Coach")
page = st.sidebar.radio("Navigate", ["Home", "Recipe Generator", "My Recipes", "Weekly Planner", "My Account"])

st.markdown(
    """
    <style>
    [data-testid="stSidebarContent"] {
        color: black;
        background-color: #ADD8E6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

if page == "Home":
    # Title
    st.title("My Nutrition Coach 🥗")

    # Welcome Message and Page Content
    st.markdown("<h2>Welcome to your personalized nutrition and fitness assistant!</h2>", unsafe_allow_html=True)
    st.markdown("Finding balance between enjoying delicious meals and maintaining a healthy lifestyle can feel overwhelming. That’s why having a tool that combines recipe discovery, meal planning, and personalized calorie tracking is so important.")
    st.markdown("This platform helps you find recipes that fit your tastes and goals while calculating your unique calorie needs based on your age, weight and height. With a built-in weekly planner, you can organize your meals effortlessly, saving time and staying on track.")
    st.markdown("It’s not just about food—it’s about creating a lifestyle where eating well is simple, enjoyable, and empowering. Cook smarter, eat better, and embrace a healthier, happier you.")
    
   # Injecting CSS for the background-image-area class
    st.markdown("""
        <style>
            .background-image-area {
                height: 300px;
                background-image: url('https://www.fitnessfirst.de/sites/g/files/tbchtk381/files/2023-08/Meal_Prep_Header.jpg');
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

            # Ensure calories is a rounded number
            if calories != "N/A":
                calories = round(calories)
        
            st.write(f"**Calories:** {calories} kcal")

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

                    # Filters and categories summary
                    st.write("#### Filters and Categories:")
                    st.write(", ".join([key for key, value in dietary_preferences.items() if value]))
                    st.write(f"**Meal Type:** {meal_type or 'N/A'}")
                    st.write(f"**Cuisine:** {cuisine or 'N/A'}")

                    # Save recipe to "My Recipes"
                    if meal_type:  # Ensure meal_type is selected
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
                st.write(f"**Calories:** {calories} kcal")
                
                if st.checkbox(f"View Full Recipe for {recipe['title']}", key=f"view_{recipe['id']}"):
                    details = get_recipe_details(recipe["id"])
                    if details:
                        st.write("#### Ingredients:")
                        for ingredient in details["extendedIngredients"]:
                            st.write(f"- {ingredient['original']}")
                        st.write("#### Instructions:")
                        for step in details.get("analyzedInstructions", [{}])[0].get("steps", []):
                            st.write(f"{step['number']}. {step['step']}")


# Import Supabase and initialize client
from supabase import create_client, Client

SUPABASE_URL = "https://qbnmfdcuzeghmyobcnhi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFibm1mZGN1emVnaG15b2JjbmhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI2OTg5NzcsImV4cCI6MjA0ODI3NDk3N30.FXophJC6_BilPfwJ8G1oI9Z_8UBqD9uf2UX0OgY3i00"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Weekly Planner
if page == "Weekly Planner":
    st.title("Weekly Planner 📅")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meals = ["Breakfast", "Lunch", "Dinner"]

    if st.session_state.get("logged_in", False):
        # Fetch the user's estimated calories from Supabase
        user_data = st.session_state.user_data
        username = user_data["username"]

        # Retrieve the estimated calories from Supabase - see Supabase Guide Nr. 6
        try:
            response = supabase.table("users").select("calories").eq("username", username).execute()
            if response.data:
                estimated_calories = response.data[0]["calories"]
            else:
                st.error("Failed to fetch estimated calories from the database.")
                estimated_calories = 0.0
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            estimated_calories = 0.0
    else:
        estimated_calories = None

    # Initialize data for the graph
    daily_totals = []
    estimated_line = [estimated_calories] * len(days) if estimated_calories else []

    # Loop through each day of the week
    for day in days:
        st.write(f"### {day}")
        col1, col2, col3 = st.columns(3)
        total_calories = 0

        # Loop through each meal for the day
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
                        # Extract calories from the recipe
                        calories = next(
                            (n["amount"] for n in recipe.get("nutrition", {}).get("nutrients", []) if n["name"] == "Calories"), 
                            0
                        )
                        total_calories += calories

        # Display total calories
        st.write(f"**Total Calories for {day}: {total_calories} kcal**")
        daily_totals.append(total_calories)

        # Display the difference only if logged in
        if estimated_calories is not None:
            difference = total_calories - estimated_calories
            st.write(f"**Difference from Estimated Calories: {difference:+.2f} kcal**")

    # Add a graph for weekly calorie comparison
    if daily_totals and estimated_line:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(days, daily_totals, label="Total Calories", marker="o", color="blue")
        if estimated_calories:
            ax.plot(days, estimated_line, label="Estimated Calories", linestyle="--", color="orange")

        ax.set_title("Weekly Calorie Overview", fontsize=16)
        ax.set_xlabel("Days of the Week", fontsize=12)
        ax.set_ylabel("Calories", fontsize=12)
        ax.legend(loc="upper left", fontsize=10)
        ax.grid(True)

        st.pyplot(fig)

import pandas as pd  # Import pandas to handle DataFrame
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

@st.cache_resource
def train_model():
    # Get data from Supabase - the data contains weight, height, gender, age and the daily calories of 1000 persons. The data has been created with ChatGTP and is fictitious. 
    try:
        response = supabase.table("calories").select("weight, height, gender, age, daily_caloric_needs").execute()

        # Now check the structure of the response
        if hasattr(response, 'data'):
            data = pd.DataFrame(response.data)  # Convert the data to DataFrame
            if data.empty:
                st.error("No data found in the calories table.")
                return None
        
            # Preprocessing: Convert Gender to numeric using LabelEncoder
            data['gender'] = LabelEncoder().fit_transform(data['gender'])

            # Select features and target variable
            features = ['weight', 'height', 'gender', 'age']
            target = 'daily_caloric_needs'

            # Prepare training data
            X = data[features]
            y = data[target]

            # Train RandomForestRegressor
            model = RandomForestRegressor(random_state=42, n_estimators=100)
            model.fit(X, y)

            return model
        else:
            st.error("Failed to fetch valid data from Supabase.")
            return None
    except Exception as e:
        st.error(f"Error loading data from Supabase: {e}")
        return None

# Load the trained model
model = train_model()

# My Account
# Created with Supabase Guide and ChatGTP
if page == "My Account":
    st.title("My Account 🧑‍💻")

    # Initialize session state for login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_data = None

    # Function to insert a new user - see Supabase Guide with instructions Nr. 5    
    def insert_user(username: str, password: str, name: str, age: int, gender: str):
        try:
            response = supabase.table("users").insert({
                "username": username,
                "password": password,
                "name": name,
                "age": age,
                "gender": gender,
                "weight": 0.0,  # Default weight
                "height": 0.0,  # Default height
                "calories": 0.0  # Default calories
            }).execute()
            return response.data
        except Exception as e:
            return e

    # Function to display user profile and allow updating weight, height, and calories
    def display_profile(user_data):
        st.subheader("Profile Information")
        st.write(f"**Username:** {user_data.get('username', 'N/A')}")
        st.write(f"**Name:** {user_data.get('name', 'N/A')}")
        st.write(f"**Age:** {user_data.get('age', 'N/A')}")
        st.write(f"**Gender:** {user_data.get('gender', 'N/A')}")
        st.write(f"**Weight:** {user_data.get('weight', 0.0)} kg")
        st.write(f"**Height:** {user_data.get('height', 0.0)} cm")
        st.write(f"**Estimated Calories:** {user_data.get('calories', 0.0):.2f} kcal/day")

        # Input fields for weight and height
        weight = st.number_input("Update your weight (kg):", min_value=0.0, step=0.1, value=user_data.get("weight", 0.0))
        height = st.number_input("Update your height (cm):", min_value=0.0, step=0.1, value=user_data.get("height", 0.0))

        # Predict calories using the ML model
        if weight > 0 and height > 0:
            gender = 0 if user_data.get("gender", "Male").lower() == "male" else 1
            age = user_data.get("age", 25)
            predicted_calories = model.predict([[weight, height, gender, age]])[0]
        else:
            predicted_calories = 0.0

        if st.button("Save Weight, Height, and Calories"):
            try:
                # Update the user's weight, height, and calories in the database (see point Supabase Guide Nr. 7)
                response = supabase.table("users").update({
                    "weight": weight,
                    "height": height,
                    "calories": predicted_calories
                }).eq("username", user_data["username"]).execute()
                if response.data:
                    # Update session state with the new data
                    st.session_state.user_data["weight"] = weight
                    st.session_state.user_data["height"] = height
                    st.session_state.user_data["calories"] = predicted_calories
                    st.success("Weight, height, and calories updated successfully!")
                else:
                    st.error("Failed to update weight, height, and calories.")
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

            # See Supabase Guide Nr. 6
            if st.button("Press twice to Login"):
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
            reg_age = st.number_input("Age", min_value=1, max_value=120, step=1, key="reg_age")
            reg_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="reg_gender")

            if st.button("Press twice to Register"):
                if reg_name and reg_username and reg_password and reg_age and reg_gender:
                    response = insert_user(reg_username, reg_password, reg_name, reg_age, reg_gender)
                    if isinstance(response, list):  # Successful registration returns a list of inserted rows
                        st.session_state.logged_in = True  # Mark user as logged in
                        st.session_state.user_data = {
                            "name": reg_name,
                            "username": reg_username,
                            "age": reg_age,
                            "gender": reg_gender,
                            "weight": 0.0,
                            "height": 0.0,
                            "calories": 0.0
                        }  # Store user data - see Supabase Guide Nr. 6
                        st.success("User registered successfully!")
                else:
                    st.error("Please fill in all fields (Name, Username, Password, Age, and Gender).")
    else:
        # Display profile if logged in
        display_profile(st.session_state.user_data)
