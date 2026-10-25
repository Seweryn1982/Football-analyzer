import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Konfiguracja strony
st.set_page_config(
    page_title="Football Match Analyzer - Wiele Lig",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Football Match Analyzer & Strzały Zespołów")
st.markdown("Aplikacja analizująca statystyki strzałów oraz formę ofensywną drużyn z podziałem na ligi europejskie.")

# ==========================================
# 1. TRENOWANIE MODELU (BAZA STRZAŁÓW)
# ==========================================
@st.cache_resource
def train_model():
    historical_data = {
        'home_shots_avg': [14.5, 9.0, 16.0, 11.5, 18.0, 8.5, 13.0, 15.5, 7.0, 12.0],
        'away_shots_avg': [10.0, 13.5, 9.5, 11.0, 8.0, 16.5, 12.0, 9.0, 14.0, 10.5],
        'home_shots_on_target_avg': [5.5, 3.0, 6.5, 4.0, 7.5, 2.5, 5.0, 6.0, 2.0, 4.5],
        'away_shots_on_target_avg': [3.5, 5.0, 3.0, 4.0, 2.5, 6.0, 4.5, 3.0, 5.5, 3.5],
        'home_unbeaten_streak': [5, 1, 3, 2, 7, 0, 4, 6, 0, 1],
        'away_unbeaten_streak': [0, 4, 1, 2, 0, 5, 2, 0, 3, 1],
        'result': [2, 0, 2, 1, 2, 0, 1, 2, 0, 1]  # 0: Goście, 1: Remis, 2: Gospodarze
    }
    
    df = pd.DataFrame(historical_data)
    X = df.drop('result', axis=1)
    y = df['result']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    return model, scaler

model, scaler = train_model()

# ==========================================
# 2. BAZA MECZÓW DLA RÓŻNYCH LIG
# ==========================================
def get_matches_by_league(league_name):
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    
    # Przykładowe mecze podzielone na wybrane ligi europejskie i polską
    database = {
        "Premier League (Anglia)": [
            {'home_team': 'Manchester United', 'away_team': 'Tottenham', 'home_shots_avg': 15.2, 'away_shots_avg': 13.8, 'home_shots_on_target_avg': 5.8, 'away_shots_on_target_avg': 5.1, 'home_unbeaten_streak': 3, 'away_unbeaten_streak': 2},
            {'home_team': 'Arsenal', 'away_team': 'Chelsea', 'home_shots_avg': 17.4, 'away_shots_avg': 12.0, 'home_shots_on_target_avg': 6.8, 'away_shots_on_target_avg': 4.2, 'home_unbeaten_streak': 6, 'away_unbeaten_streak': 1},
            {'home_team': 'Liverpool', 'away_team': 'Manchester City', 'home_shots_avg': 18.1, 'away_shots_avg': 17.5, 'home_shots_on_target_avg': 7.2, 'away_shots_on_target_avg': 7.0, 'home_unbeaten_streak': 5, 'away_unbeaten_streak': 4}
        ],
        "La Liga (Hiszpania)": [
            {'home_team': 'Real Madryt', 'away_team': 'Barcelona', 'home_shots_avg': 17.0, 'away_shots_avg': 16.5, 'home_shots_on_target_avg': 7.0, 'away_shots_on_target_avg': 6.8, 'home_unbeaten_streak': 5, 'away_unbeaten_streak': 5},
            {'home_team': 'Atletico Madryt', 'away_team': 'Villarreal', 'home_shots_avg': 14.0, 'away_shots_avg': 12.5, 'home_shots_on_target_avg': 5.2, 'away_shots_on_target_avg': 4.5, 'home_unbeaten_streak': 3, 'away_unbeaten_streak': 2}
        ],
        "Serie A (Włochy)": [
            {'home_team': 'Inter Mediolan', 'away_team': 'Juventus', 'home_shots_avg': 15.8, 'away_shots_avg': 13.0, 'home_shots_on_target_avg': 6.1, 'away_shots_on_target_avg': 4.8, 'home_unbeaten_streak': 4, 'away_unbeaten_streak': 3},
            {'home_team': 'AC Milan', 'away_team': 'AS Roma', 'home_shots_avg': 14.5, 'away_shots_avg': 13.2, 'home_shots_on_target_avg': 5.5, 'away_shots_on_target_avg': 4.6, 'home_unbeaten_streak': 2, 'away_unbeaten_streak': 3}
        ],
        "Bundesliga (Niemcy)": [
            {'home_team': 'Bayern Monachium', 'away_team': 'Borussia Dortmund', 'home_shots_avg': 19.2, 'away_shots_avg': 16.0, 'home_shots_on_target_avg': 8.0, 'away_shots_on_target_avg': 6.5, 'home_unbeaten_streak': 6, 'away_unbeaten_streak': 3},
            {'home_team': 'RB Lipsk', 'away_team': 'Bayer Leverkusen', 'home_shots_avg': 15.0, 'away_shots_avg': 15.5, 'home_shots_on_target_avg': 5.8, 'away_shots_on_target_avg': 6.0, 'home_unbeaten_streak': 3, 'away_unbeaten_streak': 4}
        ],
        "Ekstraklasa (Polska)": [
            {'home_team': 'Legia Warszawa', 'away_team': 'Lech Poznań', 'home_shots_avg': 14.2, 'away_shots_avg': 13.5, 'home_shots_on_target_avg': 5.1, 'away_shots_on_target_avg': 4.8, 'home_unbeaten_streak': 3, 'away_unbeaten_streak': 3},
            {'home_team': 'Raków Częstochowa', 'away_team': 'Jagiellonia Białystok', 'home_shots_avg': 13.8, 'away_shots_avg': 14.0, 'home_shots_on_target_avg': 4.9, 'away_shots_on_target_avg': 5.0, 'home_unbeaten_streak': 4, 'away_unbeaten_streak': 2}
        ]
    }
    
    return today_str, database.get(league_name, [])

# ==========================================
# 3. INTERFEJS UŻYTKOWNIKA (UI)
# ==========================================
st.sidebar.header("Panel sterowania")
today_str = datetime.date.today().strftime('%Y-%m-%d')
st.sidebar.info(f"📅 Dzisiejsza data: **{today_str}**")

league_choice = st.sidebar.selectbox(
    "Wybierz ligę:", 
    [
        "Premier League (Anglia)", 
        "La Liga (Hiszpania)", 
        "Serie A (Włochy)", 
        "Bundesliga (Niemcy)", 
        "Ekstraklasa (Polska)"
    ]
)

today_date, matches = get_matches_by_league(league_choice)

st.subheader(f"Mecze i prognozy: {league_choice} ({today_date})")

if not matches:
    st.warning("Brak zaplanowanych spotkań w tej lidze na dzisiaj.")
else:
    for match in matches:
        features = np.array([[
            match['home_shots_avg'],
            match['away_shots_avg'],
            match['home_shots_on_target_avg'],
            match['away_shots_on_target_avg'],
            match['home_unbeaten_streak'],
            match['away_unbeaten_streak']
        ]])
        
        features_scaled = scaler.transform(features)
        probabilities = model.predict_proba(features_scaled)[0]
        
        away_prob = round(probabilities[0] * 100, 1)
        draw_prob = round(probabilities[1] * 100, 1)
        home_prob = round(probabilities[2] * 100, 1)
        
        max_prob = max(home_prob, draw_prob, away_prob)
        if max_prob == home_prob:
            best_pick = f"Wygrana Gospodarzy ({match['home_team']})"
        elif max_prob == draw_prob:
            best_pick = "Remis"
        else:
            best_pick = f"Wygrana Gości ({match['away_team']})"

        with st.container():
            col1, col2, col3 = st.columns([3, 3, 2])
            
            with col1:
                st.markdown(f"### 🏟️ {match['home_team']} vs {match['away_team']}")
                st.caption(f"Śr. strzałów: Dom ({match['home_shots_avg']}) | Wyjazd ({match['away_shots_avg']})")
                st.caption(f"Strzały celne: Dom ({match['home_shots_on_target_avg']}) | Wyjazd ({match['away_shots_on_target_avg']})")
                
            with col2:
                st.metric(label="Szanse (1 - X - 2)", value=f"{home_prob}% | {draw_prob}% | {away_prob}%")
                
            with col3:
                st.success(f"🎯 Typ: **{best_pick}**\n\nPewność: **{max_prob}%**")
                
            st.divider()
