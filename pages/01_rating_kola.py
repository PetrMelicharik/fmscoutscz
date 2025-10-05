import streamlit as st
import pandas as pd

# nastavení stránky - kosmetická úprava
st.set_page_config(page_title="FM Scouts CZ - ratings", page_icon="⚽")

# záhlaví stránky
st.image("logo.jpg", width=150)
st.title("FM Scouts cz")
st.subheader("Nejlepší ratingy kola - TOP50:")

# načtení excel souborů
players = pd.read_excel("players.xlsx")
profiles = pd.read_excel("players_profiles.xlsx")
ratings = pd.read_excel("players_ratings.xlsx")
stats = pd.read_excel("players_stats.xlsx")

# sjednocení souborů do databáze na základě id sloupce
shortlist = pd.merge(players, profiles, on="id")
shortlist2 = pd.merge(shortlist, ratings, on = "id")
database = pd.merge(shortlist2, stats, on="id")

# zobrazení top 50 ratingů
potw = database[["Jméno", "Příjmení", "team", "Pozice", "Rating_1", "Sofascore"]].sort_values("Rating_1", ascending=False)
st.dataframe(potw.head(60))