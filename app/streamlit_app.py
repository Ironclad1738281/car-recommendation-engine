import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load data
df = pd.read_csv("data/car_features.csv")

st.title("🚗 Car Recommendation Engine")

st.write(
    "Find cars that match your budget and performance preferences."
)

# User inputs
max_price = st.slider("Maximum Price ($)", 5000, 100000, 30000)
min_hp = st.slider("Minimum Horsepower", 100, 700, 200)
min_mpg = st.slider("Minimum Highway MPG", 10, 60, 25)

# Filter dataset
filtered = df[
    (df["MSRP"] <= max_price) &
    (df["Engine HP"] >= min_hp) &
    (df["highway MPG"] >= min_mpg)
].copy()

if filtered.empty:
    st.warning("No cars match those preferences.")
else:

    # Normalize ranking features
    scaler = MinMaxScaler()

    filtered["mpg_score"] = scaler.fit_transform(filtered[["highway MPG"]])
    filtered["hp_score"] = scaler.fit_transform(filtered[["Engine HP"]])
    filtered["pop_score"] = scaler.fit_transform(filtered[["Popularity"]])
    filtered["price_score"] = 1 - scaler.fit_transform(filtered[["MSRP"]])

    # Ranking formula
    filtered["final_score"] = (
        0.4 * filtered["mpg_score"]
        + 0.3 * filtered["hp_score"]
        + 0.2 * filtered["pop_score"]
        + 0.1 * filtered["price_score"]
    )

    top_cars = filtered.sort_values(
        by="final_score",
        ascending=False
    ).head(5)

    st.subheader("Top Recommended Cars")

    st.dataframe(
        top_cars[
            ["Make", "Model", "MSRP", "Engine HP", "highway MPG"]
        ]
    )