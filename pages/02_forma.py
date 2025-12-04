import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# nastavení stránky
st.set_page_config(page_title="FM Scouts CZ - forma", page_icon="⚽")

st.image("logo.jpg", width=150)
st.title("FM Scouts cz")
st.subheader("Aktuální forma - TOP50:")

# načtení Excelů
players = pd.read_excel("players.xlsx")
profiles = pd.read_excel("players_profiles.xlsx")
ratings = pd.read_excel("players_ratings.xlsx")
stats = pd.read_excel("players_stats.xlsx")

# merge všech tabulek
shortlist = pd.merge(players, profiles, on="id")
shortlist2 = pd.merge(shortlist, ratings, on="id")
database = pd.merge(shortlist2, stats, on="id")

# -----------------------------------------------------
# 🟦 FILTRACE PODLE DATUMU → pouze hráči s ratingem ≤ 7 dní
# -----------------------------------------------------

# najdeme všechny sloupce začínající na "Date_"
date_cols = [col for col in database.columns if col.startswith("Date_")]

# vytvoříme nový sloupec: nejnovější datum ratingu
database["last_rating_date"] = database[date_cols].max(axis=1)

# dnešní datum
today = datetime.today().date()

# filtrace: pouze hráči s ratingem mladším než 7 dní
database_filtered = database[
    (today - database["last_rating_date"]) <= timedelta(days=7)
]

# -----------------------------------------------------
# TABULKA TOP 50
# -----------------------------------------------------

form = database_filtered[
    ["Jméno", "Příjmení", "team", "Pozice", "avg_rating", "Sofascore"]
].sort_values("avg_rating", ascending=False)

st.dataframe(form.head(60))
