import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# --- Nastavení stránky ---
st.set_page_config(page_title="FM Scouts CZ - Detail hráče", page_icon="⚽")

# --- Záhlaví ---
st.image("logo.jpg", width=150)
st.title("FM Scouts CZ")
st.subheader("Detail hráče")

# --- Načtení dat ---
players = pd.read_excel("players.xlsx")
profiles = pd.read_excel("players_profiles.xlsx")
ratings = pd.read_excel("players_ratings.xlsx")
stats = pd.read_excel("players_stats.xlsx")

# Sloučení všech tabulek
database = (
    players
    .merge(profiles, on="id")
    .merge(ratings, on="id")
    .merge(stats, on="id")
)

# --- Vyhledávací pole ---
search_name = st.text_input("🔍 Zadej jméno hráče:")

if search_name:
    # Filtrace podle jména nebo příjmení
    results = database[
        database["Jméno"].str.contains(search_name, case=False, na=False) |
        database["Příjmení"].str.contains(search_name, case=False, na=False)
    ]

    if not results.empty:
        player_names = results["Jméno"] + " " + results["Příjmení"]
        selected_player = st.selectbox("Vyber hráče:", player_names)

        if selected_player:
            player_data = results[
                (results["Jméno"] + " " + results["Příjmení"]) == selected_player
            ].iloc[0]

            st.markdown(f"### {player_data['Jméno']} {player_data['Příjmení']}")
            st.markdown(
                f"**Tým:** {player_data.get('team', 'Neznámý')} | "
                f"**Pozice:** {player_data.get('Pozice', 'N/A')} | "
                f"**Liga:** {player_data.get('tournament_country', 'N/A')}"
            )

            # --- STATISTIKY ---
            st.subheader("📊 Statistiky hráče")

            stats_cols = [
                "appearances", "minutesPlayed", "goals", "expectedGoals", "assists", "expectedAssists",
                "goalsAssistsSum", "totalShots", "shotsOnTarget", "goalsFromInsideTheBox",
                "goalsFromOutsideTheBox", "scoringFrequency", "bigChancesCreated", "totalPasses",
                "keyPasses", "accuratePasses", "passToAssist", "accurateCrosses", "successfulDribbles",
                "aerialDuelsWon", "clearances", "totwAppearances", "rating"
            ]

            # Slovník pro české názvy
            stats_czech = {
                "appearances": "Zápasy",
                "minutesPlayed": "Odehrané minuty",
                "goals": "Góly",
                "expectedGoals": "xG",
                "assists": "Asistence",
                "expectedAssists": "xA",
                "goalsAssistsSum": "Góly + Asistence",
                "totalShots": "Celkem střel",
                "shotsOnTarget": "Střely na bránu",
                "goalsFromInsideTheBox": "Góly z vápna",
                "goalsFromOutsideTheBox": "Góly z dálky",
                "scoringFrequency": "Frekvence skórování",
                "bigChancesCreated": "Vytvořené šance",
                "totalPasses": "Celkem přihrávek",
                "keyPasses": "Klíčové přihrávky",
                "accuratePasses": "Přesné přihrávky",
                "passToAssist": "Přihrávky k asistenci",
                "accurateCrosses": "Přesné centry",
                "successfulDribbles": "Úspěšné driblinky",
                "aerialDuelsWon": "Vyhrané hlavičky",
                "clearances": "Odvody míče",
                "totwAppearances": "Zápasy TOTW",
                "rating": "Průměrné hodnocení"
            }

            # Připravení hodnot a formátování
            stats_data = []
            for col in stats_cols:
                val = player_data.get(col, np.nan)
                if pd.isna(val):
                    formatted_val = "NaN"
                else:
                    if col in ["expectedGoals", "expectedAssists", "rating"]:
                        formatted_val = f"{val:.2f}"
                    else:
                        formatted_val = f"{int(val)}"
                stats_data.append({"Statistika": stats_czech.get(col, col), "Hodnota": formatted_val})

            st.table(pd.DataFrame(stats_data))

            # --- PIZZA CHART ---
            st.subheader("🍕 Herní profil hráče (procentuální statistiky)")

            pizza_cols = [
                "accuratePassesPercentage", "successfulDribblesPercentage", "accurateCrossesPercentage",
                "aerialDuelsWonPercentage", "totalDuelsWonPercentage", "goalConversionPercentage",
                "accurateLongBallsPercentage", "groundDuelsWonPercentage"
            ]

            pizza_labels = [
                "Přesné přihrávky %", "Úspěšné driblinky %", "Přesné centry %",
                "Vyhrané hlavičky %", "Vyhrané souboje %", "Úspěšnost střel %",
                "Přesné dlouhé míče %", "Vyhrané pozemní souboje %"
            ]

            pizza_data = [player_data.get(col, np.nan) for col in pizza_cols]

            if all(pd.isna(pizza_data)):
                st.info("Procentuální statistiky nejsou dostupné.")
            else:
                values = [v if not pd.isna(v) else 0 for v in pizza_data]
                N = len(pizza_labels)
                angles = [n / float(N) * 2 * pi for n in range(N)]
                values += values[:1]
                angles += angles[:1]

                # --- Výběr barvy podle pozice ---
                pozice = str(player_data.get("Pozice", "")).lower()
                if "brankář" in pozice or "gk" in pozice:
                    color = "#ff7f0e"  # oranžová
                elif any(x in pozice for x in ["obránce", "cb", "rb", "lb", "df"]):
                    color = "#1f77b4"  # modrá
                elif any(x in pozice for x in ["záložník", "cm", "dm", "mf"]):
                    color = "#2ca02c"  # zelená
                elif any(x in pozice for x in ["útočník", "fw", "st", "w"]):
                    color = "#d62728"  # červená
                else:
                    color = "#9467bd"  # fialová default

                # --- Graf ---
                fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
                ax.set_ylim(0, 100)
                ax.set_theta_offset(pi / 2)
                ax.set_theta_direction(-1)

                plt.xticks(angles[:-1], pizza_labels, color='black', size=10)
                ax.set_rgrids([20, 40, 60, 80, 100], color="lightgrey")

                ax.plot(angles, values, linewidth=2.5, linestyle='solid', color=color)
                ax.fill(angles, values, alpha=0.35, color=color)

                # popisky hodnot
                for angle, value in zip(angles[:-1], values[:-1]):
                    ax.text(
                        angle, value + 3, f"{value:.1f}%", color="black",
                        fontsize=9, ha='center', va='center', fontweight='bold'
                    )

                ax.spines['polar'].set_visible(False)
                ax.grid(True, color="lightgrey", linestyle="--", linewidth=0.8)
                ax.set_facecolor("#f9f9f9")

                st.pyplot(fig)

    else:
        st.warning("❌ Hráč nenalezen. Zkus jiné jméno.")
