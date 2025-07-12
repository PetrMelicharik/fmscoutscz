import streamlit as st
import pandas as pd

# nastavení stránky - kosmetická úprava
st.set_page_config(page_title="FM Scouts CZ", page_icon="⚽")

# záhlaví stránky
st.image("logo.jpg", width=150)
st.title("FM Scouts cz")
st.subheader("Databáze hráčů:")

# načtení excel souborů
players = pd.read_excel("players.xlsx")
profiles = pd.read_excel("players_profiles.xlsx")
ratings = pd.read_excel("players_ratings.xlsx")
stats = pd.read_excel("players_stats.xlsx")

# sjednocení souborů do databáze na základě id sloupce
shortlist = pd.merge(players, profiles, on="id")
shortlist2 = pd.merge(shortlist, ratings, on = "id")
database = pd.merge(shortlist2, stats, on="id")

# zobrazení databáze na stránce
main_page_db = database[["id", "Jméno", "Příjmení", "team", "Pozice", "nationality", "birth_year", "market_value", "contract_until", "Transfermarkt", "Sofascore"]]

# vyhledávání hráče podle jména
search_name = st.text_input("Hledat hráče podle příjmení")

if search_name:
    filtered_db = main_page_db[main_page_db["Příjmení"].str.contains(search_name, case=False, na=False)]
    st.dataframe(filtered_db)
else:
    st.dataframe(main_page_db)