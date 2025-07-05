import streamlit as st
import pandas as pd

st.title("FM Scouts cz")

players = pd.read_excel("players.xlsx")
profiles = pd.read_excel("players_profiles.xlsx")
ratings = pd.read_excel("players_ratings.xlsx")
stats = pd.read_excel("players_stats.xlsx")

shortlist = pd.merge(players, profiles, on="id")
shortlist2 = pd.merge(shortlist, ratings, on = "id")
database = pd.merge(shortlist2, stats, on="id")

main_page_db = database[["id", "Jméno", "Příjmení", "team", "Pozice", "nationality", "birth_year", "market_value", "contract_until", "Transfermarkt", "Sofascore"]]
main_page_db