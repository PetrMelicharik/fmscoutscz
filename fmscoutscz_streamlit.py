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

# filtrování
pozice = st.multiselect("Vyber pozici:", options=database["Pozice"].unique())
narodnost = st.multiselect("Vyber národnost:", options=database["nationality"].unique())
liga = st.multiselect("Vyber ligu:", options=database["tournament_country"].unique())
team = st.multiselect("Vyber tým:", options=database["team"].dropna().unique())
contract = st.multiselect("Vyber délku smlouvy:", options=database["contract_until"].dropna().unique())

# Aplikace filtrů
filtered_db = database.copy()

if pozice:
    filtered_db = filtered_db[filtered_db["Pozice"].isin(pozice)]
if narodnost:
    filtered_db = filtered_db[filtered_db["nationality"].isin(narodnost)]
if liga:
    filtered_db = filtered_db[filtered_db["tournament_country"].isin(liga)]
if team:
    filtered_db = filtered_db[filtered_db["team"].isin(team)]
if contract:
    filtered_db = filtered_db[filtered_db["contract_until"].isin(contract)]


# zobrazení databáze na stránce
st.dataframe(
    filtered_db[["id", "Jméno", "Příjmení", "Pozice", "nationality", "birth_year", "team", "tournament_country", "market_value", "contract_until", "Transfermarkt", "Sofascore"]])