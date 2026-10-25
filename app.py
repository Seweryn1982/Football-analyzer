import streamlit as st
import pandas as pd
import numpy as np
import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Konfiguracja strony
st.set_page_config(
    page_title="Football Match Analyzer",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Football Match Analyzer & Predictor")
st.markdown("Aplikacja analizująca dzisiejsze spotkania i wyliczająca prawdopodobieństwa wyników (1X2) przy użyciu uczenia maszynowego.")

# ==========================================
# 1. TRENOWANIE MODELU
# ==========================================
@st.cache_resource
def train_model():
    historical_data = {
        'home_win_rate_last5': [0.8, 0.2, 0.6, 0.4, 1.0, 0.2, 0.6, 0.8, 0.0, 0.4],
        'away_win_rate_last5': [0.2, 0.6, 0.2, 0.4, 0.0, 0.8, 0.4, 0.2, 0.6, 0.2],
        'home_goals_scored_avg': [2.2, 1.0, 1.8, 1.2, 2.8, 0.8, 1.6, 2.0, 0.4, 1.0],
        'away_goals_scored_avg': [0.8, 1.6, 0.6, 1.0, 0.4, 2.2, 1.2, 0.8, 1.8, 0.8],
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
# 2. POBIERANIE DZISIEJSZEJ DATY I MECZÓW
# ==========================================
def get_todays_matches():
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    
    matches = [
        {
            'home_team': f'Mecz z dnia {today_str} (Gospodarz A)', 'away_team': 'Gość A',
            'home_win_rate_last5': 0.7, 'away_win_rate_last5': 0.3,
            'home_goals_scored_avg': 2.0, 'away_goals_scored_avg': 1.0,
            'home_unbeaten_streak': 4, 'away_unbeaten_streak': 1
        },
        {
            'home_team': f'Mecz z dnia {today_str} (Gospodarz B)', 'away_team': 'Gość B',
            'home_win_rate_last5': 0.5, 'away_win_rate_last5': 0.5,
            'home_goals_scored_avg': 1.4, 'away_goals_scored_avg': 1.5,
            'home_unbeaten_streak': 2, 'away_unbeaten_streak': 2
        }
    ]
    return today_str, matches

today_date, matches = get_todays_matches()

st.sidebar.header("Panel sterowania")
st.sidebar.info(f"📅 Dzisiejsza data: **{today_date}**")
league_choice = st.sidebar.selectbox("Wybierz ligę:", ["Premier League", "La Liga", "Serie A"])

st.subheader(f"Mecze i prognozy na dzisiaj ({today_date}) - {league_choice})")

if not matches:
    st.warning("Brak zaplanowanych spotkań na dzisiaj.")
else:
    for match in matches:
        features = np.array([[
            match['home_win_rate_last5'],
            match['away_win_rate_last5'],
            match['home_goals_scored_avg'],
            match['away_goals_scored_avg'],
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
                st.caption(f"Analiza dla bieżącej daty: {today_date}")
                
            with col2:
                st.metric(label="Szanse (1 - X - 2)", value=f"{home_prob}% | {draw_prob}% | {away_prob}%")
                
            with col3:
                st.success(f"🎯 Typ: **{best_pick}**\n\nPewność: **{max_prob}%**")
                
            st.divider()
