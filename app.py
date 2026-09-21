import streamlit as st
from datetime import date, datetime
import pandas as pd

st.set_page_config(
    page_title="AI Food Waste Reduction Assistant",
    page_icon="🥗",
    layout="wide"
)

# -----------------------------
# Demo knowledge base / RAG-like layer
# -----------------------------
STORAGE_TIPS = {
    "Tomato": "Store ripe tomatoes at room temperature away from direct sunlight. Use promptly when very soft.",
    "Banana": "Keep bananas at room temperature. Separate very ripe bananas and consider using them in smoothies or baking.",
    "Milk": "Keep refrigerated and follow the package date and storage instructions. Do not consume if spoiled.",
    "Bread": "Keep sealed in a cool, dry place. Freeze extra bread if you will not use it soon.",
    "Rice": "Store uncooked rice in a cool, dry, sealed container.",
    "Potato": "Store in a cool, dark, dry and ventilated place; avoid prolonged exposure to light.",
    "Onion": "Store whole onions in a cool, dry, ventilated place away from potatoes.",
    "Apple": "Store according to variety and condition; refrigerate when appropriate and use damaged fruit promptly.",
    "Carrot": "Keep refrigerated and use softer carrots first.",
    "Spinach": "Keep refrigerated and use fresh leafy greens promptly."
}

DEFAULT_FOODS = [
    {"Food": "Tomato", "Quantity": "4", "Priority": "Use Soon", "Added": str(date.today())},
    {"Food": "Banana", "Quantity": "5", "Priority": "Use Soon", "Added": str(date.today())},
    {"Food": "Rice", "Quantity": "1 kg", "Priority": "Good", "Added": str(date.today())},
]

RECIPE_MAP = {
    frozenset(["Tomato", "Rice", "Onion"]): ("Tomato Rice", "Rice, tomato and onion can be combined into a simple tomato rice meal."),
    frozenset(["Banana", "Milk"]): ("Banana Smoothie", "Blend banana with milk; add other ingredients according to your preferences."),
    frozenset(["Potato", "Onion", "Tomato"]): ("Mixed Vegetable Curry", "Use the vegetables together in a simple cooked dish."),
    frozenset(["Tomato", "Onion"]): ("Tomato-Onion Salad", "Use fresh tomatoes and onions if they are in suitable condition."),
}

def get_priority(food, quantity):
    # Demo heuristic for the prototype. In a production system, this would use
    # actual dates, storage conditions and a validated food-safety knowledge base.
    if food in {"Tomato", "Banana", "Milk", "Spinach"}:
        return "Use Soon"
    return "Good"

def generate_recommendation(inventory):
    names = {row["Food"] for row in inventory}
    urgent = [row["Food"] for row in inventory if row["Priority"] == "Use Soon"]

    recipe = None
    for ingredients, value in RECIPE_MAP.items():
        if ingredients.issubset(names):
            recipe = value
            break

    if not recipe and len(names) >= 2:
        available = ", ".join(sorted(names)[:4])
        recipe = ("Custom Meal Idea", f"Consider a meal that uses some of your available ingredients: {available}.")

    return urgent, recipe

# -----------------------------
# Session state
# -----------------------------
if "inventory" not in st.session_state:
    st.session_state.inventory = DEFAULT_FOODS.copy()

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

# -----------------------------
# Header
# -----------------------------
st.title("🥗 AI Food Waste Reduction Assistant")
st.caption("A sustainability prototype aligned with SDG 12 — Responsible Consumption and Production.")

with st.expander("ℹ️ About this project"):
    st.write(
        "This prototype demonstrates how Generative AI, RAG-style knowledge retrieval, "
        "and an Agentic AI workflow could help users manage food inventory and reduce avoidable waste. "
        "The current demo uses a small local knowledge base and deterministic recommendations so it "
        "can run without an API key."
    )

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Add Food")
    food = st.selectbox(
        "Food item",
        sorted(STORAGE_TIPS.keys()) + ["Other"]
    )
    if food == "Other":
        food = st.text_input("Enter food name")
    quantity = st.text_input("Quantity", value="1")

    if st.button("➕ Add to inventory", use_container_width=True):
        if food.strip():
            st.session_state.inventory.append({
                "Food": food.strip().title(),
                "Quantity": quantity,
                "Priority": get_priority(food.strip().title(), quantity),
                "Added": str(date.today())
            })
            st.success("Added.")

    st.divider()
    st.header("Prototype Actions")
    if st.button("🤖 Analyze My Food", use_container_width=True):
        st.session_state.recommendations = generate_recommendation(st.session_state.inventory)

    if st.button("🗑️ Clear Inventory", use_container_width=True):
        st.session_state.inventory = []
        st.session_state.recommendations = None
        st.rerun()

# -----------------------------
# Dashboard
# -----------------------------
col1, col2, col3 = st.columns(3)
use_soon = sum(1 for x in st.session_state.inventory if x["Priority"] == "Use Soon")
col1.metric("Food items", len(st.session_state.inventory))
col2.metric("Use soon", use_soon)
col3.metric("Prototype meals", "3+" if st.session_state.inventory else "0")

st.subheader("📦 Current Food Inventory")

if st.session_state.inventory:
    df = pd.DataFrame(st.session_state.inventory)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Your inventory is empty. Add some food items from the sidebar.")

# -----------------------------
# AI / Agentic workflow
# -----------------------------
st.subheader("🤖 AI Recommendation")

if st.session_state.recommendations:
    urgent, recipe = st.session_state.recommendations

    if urgent:
        st.warning(
            "Prioritize these items: " + ", ".join(urgent) +
            ". Check their actual condition, package instructions and local food-safety guidance before consuming."
        )
    else:
        st.success("No prototype priority items were detected.")

    if recipe:
        st.markdown(f"### 🍽️ {recipe[0]}")
        st.write(recipe[1])

    st.markdown("### 📚 Retrieved sustainability/storage guidance")
    selected = urgent[:3] if urgent else [x["Food"] for x in st.session_state.inventory[:3]]
    for item in selected:
        tip = STORAGE_TIPS.get(item, "Follow the product label and appropriate food-safety guidance.")
        st.write(f"**{item}:** {tip}")

    st.markdown("### 🔄 Agent workflow")
    st.code(
        "1. Read food inventory\n"
        "2. Prioritize items needing attention\n"
        "3. Retrieve relevant knowledge (RAG)\n"
        "4. Generate a meal/action recommendation\n"
        "5. Present a sustainability tip",
        language="text"
    )
else:
    st.info("Click **Analyze My Food** to run the prototype AI workflow.")

# -----------------------------
# Optional image upload demo
# -----------------------------
st.subheader("📷 Optional Grocery Image Upload")
uploaded = st.file_uploader(
    "Upload a grocery/food image for the prototype demo",
    type=["png", "jpg", "jpeg"]
)
if uploaded:
    st.image(uploaded, caption="Uploaded image", use_container_width=True)
    st.info(
        "Image recognition is represented as an extension point in this prototype. "
        "A production version could connect a computer-vision model or multimodal AI service "
        "to identify food items automatically."
    )

# -----------------------------
# Project impact
# -----------------------------
st.subheader("🌱 Sustainability Impact")
st.write(
    "The prototype encourages users to use food already available before purchasing more, "
    "supports meal planning, and increases awareness of responsible consumption. "
    "Impact should be measured with real user testing rather than assumed from the prototype."
)

st.caption("Prototype for educational use • SDG 12 • AI for Sustainability")
