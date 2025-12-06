import streamlit as st
import pandas as pd

# nastavení stránky - kosmetická úprava
st.set_page_config(page_title="FM Scouts CZ - forma", page_icon="⚽")

# záhlaví stránky
st.image("logo.jpg", width=100)
st.title("FM Scouts cz")
st.subheader("Nejlepší střelci:")

# načtení excel souborů
players = pd.read_excel("players.xlsx")
profiles = pd.read_excel("players_profiles.xlsx")
ratings = pd.read_excel("players_ratings.xlsx")
stats = pd.read_excel("players_stats.xlsx")

# sjednocení souborů do databáze na základě id sloupce
shortlist = pd.merge(players, profiles, on="id")
shortlist2 = pd.merge(shortlist, ratings, on = "id")
database = pd.merge(shortlist2, stats, on="id")

# zobrazení top 20 střelců
stats = database[["Jméno", "Příjmení", "team", "Pozice", "goals", "Sofascore"]].sort_values("goals", ascending=False)
st.dataframe(stats.head(20))

# zobrazení top 20 asistentů
st.subheader("Nejlepší nahrávači:")
stats = database[["Jméno", "Příjmení", "team", "Pozice", "assists", "Sofascore"]].sort_values("assists", ascending=False)
st.dataframe(stats.head(20))

# zobrazení top 20 v bodech
st.subheader("Kanadské bodování:")
stats = database[["Jméno", "Příjmení", "team", "Pozice", "goalsAssistsSum", "Sofascore"]].sort_values("goalsAssistsSum", ascending=False)
st.dataframe(stats.head(20))