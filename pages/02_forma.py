import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# nastavení stránky
st.set_page_config(page_title="FM Scouts CZ - forma", page_icon="⚽")

st.image("logo.jpg", width=100)
st.title("FM Scouts cz")
st.subheader("Aktuální forma - TOP30:")

# načtení Excelů
players = pd.read_excel("players.xlsx")
profiles = pd.read_excel("players_profiles.xlsx")
ratings = pd.read_excel("players_ratings.xlsx")
stats = pd.read_excel("players_stats.xlsx")

# merge všech tabulek
shortlist = pd.merge(players, profiles, on="id")
shortlist2 = pd.merge(shortlist, ratings, on="id")
database = pd.merge(shortlist2, stats, on="id")

# limit pro stáří dat = 70 dní
limit_date = datetime.now() - timedelta(days=70)

# seznam sloupců s daty
date_cols = [f"Date_{i}" for i in range(1, 8)]

# převedení textových dat ve formátu YYYY-MM-DD na datetime
for col in date_cols:
    database[col] = pd.to_datetime(database[col], errors="coerce")

# hráč musí mít alespoň 1 datum
database = database[database[date_cols].notna().any(axis=1)]

# vytvoření masky: povolujeme hodnoty NaT + datumy neza starší než limit
mask = (database[date_cols].isna()) | (database[date_cols] >= limit_date)

# hráč projde pouze pokud *všechny jeho datumy (kromě NaT)* jsou v limitu
database = database[mask.all(axis=1)]

# výsledek ↓↓↓
form = database[["Jméno", "Příjmení", "team", "Pozice", "avg_rating", "Sofascore"]]\
        .sort_values("avg_rating", ascending=False)

st.dataframe(form.head(30))
