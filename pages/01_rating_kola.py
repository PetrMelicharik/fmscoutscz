import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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

# převod date 1 na datum
database["Date_1"]=pd.to_datetime(database["Date_1"], errors="coerce").dt.date

today = datetime.today().date()

database_filtered = database[(today - database["Date_1"]) <= timedelta(days=7)]

# zobrazení top 30 ratingů
potw = database_filtered[["Jméno", "Příjmení", "team", "Pozice", "Rating_1", "Sofascore"]].sort_values("Rating_1", ascending=False)
st.dataframe(potw.head(30))