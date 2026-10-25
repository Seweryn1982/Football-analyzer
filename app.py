import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# 1. Konfiguracja strony
st.set_page_config(page_title="Football Shot Analyzer", page_icon="⚽", layout="centered")

st.title("⚽ Match Shot Potential Analyzer")
st.write("Aplikacja do analizy dzisiejszych meczów pod kątem potencjału strzałowego (30+ celnych i niecelnych).")

# Wybór daty analizy (domyślnie dzisiejszy dzień)
selected_date = st.date_input("Wybierz datę analizy:", datetime.now())
formatted_date = selected_date.strftime('%d.%m.%Y')

st.info(f"Analiza spotkań na wybrany dzień: **{formatted_date}**")

# 2. Silnik Machine Learning do prognozy wyników (1X2)
@st.cache_resource
def get_trained_model():
    X_train = np.array([
        [15.5, 12.0, 0.8, 0.4, 4, 30.0],
        [10.0, 14.5, 0.2, 0.6, 2, 26.5],
        [18.0, 8.5,  1.0, 0.2, 5, 33.0],
        [12.5, 12.0, 0.4, 0.4, 3, 28.0],
        [8.0,  16.0, 0.0, 0.8, 1, 31.0],
        [14.0, 10.0, 0.6, 0.4, 3, 27.5],
        [16.5, 11.0, 0.8, 0.2, 4, 32.0],
        [9.5,  13.0, 0.2, 0.6, 2, 25.0]
    ])
    y_train = np.array([2, 0, 2, 1, 0, 2, 2, 0])
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y_train)
    return model, scaler

model, scaler = get_trained_model()

# 3. Główna akcja analizy dla dzisiejszego dnia
if st.button("🚀 Przeanalizuj dzisiejsze mecze", type="primary"):
    with st.spinner(f"Pobieranie i analizowanie spotkań na dzień {formatted_date}..."):
        
        # Generujemy mecze dopasowane do bieżącego dnia i wybranej daty
        matches_data = [
            {
                "league": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (Anglia)",
                "home": f"Gospodarz PL ({formatted_date})",
                "away": f"Gość PL ({formatted_date})",
                "home_form_shots": 16.5,
                "away_form_shots": 14.2,
                "home_win_rate_5": 0.8,
                "away_win_rate_5": 0.4,
                "h2h_avg_shots": 31.5,
                "last_match_home": "Wysoka aktywność w pressingu w ostatnich 5 kolejkach",
                "last_match_away": "Stabilna gra w defensywie, dużo strzałów z dystansu",
                "h2h_summary": "W bezpośrednich pojedynkach padają średnio ponad 3 strzały na bramkę na mecz"
            },
            {
                "league": "🇪🇸 La Liga (Hiszpania)",
                "home": f"Gospodarz La Liga ({formatted_date})",
                "away": f"Gość La Liga ({formatted_date})",
                "home_form_shots": 17.8,
                "away_form_shots": 12.5,
                "home_win_rate_5": 1.0,
                "away_win_rate_5": 0.2,
                "h2h_avg_shots": 30.2,
                "last_match_home": "Dominacja w posiadaniu piłki i stałych fragmentach",
                "last_match_away": "Skupienie na kontratakach i szybkich skrzydłach",
                "h2h_summary": "Historycznie mecze między tymi ekipami cechują się otwartą grą"
            },
            {
                "league": "🇮🇹 Serie A (Włochy)",
                "home": f"Gospodarz Serie A ({formatted_date})",
                "away": f"Gość Serie A ({formatted_date})",
                "home_form_shots": 15.0,
                "away_form_shots": 16.2,
                "home_win_rate_5": 0.6,
                "away_win_rate_5": 0.6,
                "h2h_avg_shots": 32.0,
                "last_match_home": "Solidna gra formacji ofensywnej u siebie",
                "last_match_away": "Agresywny pressing na połowie rywala",
                "h2h_summary": "Ostatnie mecze H2H przynosiły wymianę ciosów i grad strzałów"
            },
            {
                "league": "🇩🇪 Bundesliga (Niemcy)",
                "home": f"Gospodarz Bundesliga ({formatted_date})",
                "away": f"Gość Bundesliga ({formatted_date})",
                "home_form_shots": 18.5,
                "away_form_shots": 15.8,
                "home_win_rate_5": 0.8,
                "away_win_rate_5": 0.6,
                "h2h_avg_shots": 33.8,
                "last_match_home": "Bardzo wysoka intensywność biegowa i celność",
                "last_match_away": "Ofensywne nastawienie wyjazdowe",
                "h2h_summary": "Pojedynki w tej parze regularnie przekraczają linię 30 strzałów"
            },
            {
                "league": "🇵🇱 PKO BP Ekstraklasa (Polska)",
                "home": f"Gospodarz Ekstraklasa ({formatted_date})",
                "away": f"Gość Ekstraklasa ({formatted_date})",
                "home_form_shots": 14.8,
                "away_form_shots": 13.5,
                "home_win_rate_5": 0.6,
                "away_win_rate_5": 0.4,
                "h2h_avg_shots": 28.5,
                "last_match_home": "Silne wsparcie trybun i wysoki współczynnik xG",
                "last_match_away": "Duża liczba strzałów z dystansu",
                "h2h_summary": "Zacięte spotkania ligowe z dużą walką w środku pola"
            }
        ]
        
        st.subheader(f"🎯 Wyniki analizy na dzień: {formatted_date}")
        
        for m in matches_data:
            shots_est = round((m['home_form_shots'] + m['away_form_shots'] + m['h2h_avg_shots']) / 2, 1)
            
            features = np.array([[
                m['home_form_shots'], m['away_form_shots'],
                m['home_win_rate_5'], m['away_win_rate_5'],
                int(m['home_win_rate_5'] * 5), shots_est
            ]])
            features_scaled = scaler.transform(features)
            probs = model.predict_proba(features_scaled)[0]
            
            away_p, draw_p, home_p = round(probs[0]*100, 1), round(probs[1]*100, 1), round(probs[2]*100, 1)

            with st.container():
                st.markdown(f"### {m['league']}")
                st.markdown(f"### 🏟️ **{m['home']} vs {m['away']}**")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"📊 **Forma (Śr. strzałów):**\n* Gospodarz: `{m['home_form_shots']}`\n* Gość: `{m['away_form_shots']}`")
                    st.markdown(f"🕒 **Ostatnie mecze:**\n* {m['last_match_home']}\n* {m['last_match_away']}")
                
                with c2:
                    st.markdown(f"⚔️ **Analiza H2H:**\n* Śr. strzałów w H2H: `{m['h2h_avg_shots']}`\n* {m['h2h_summary']}")
                    st.markdown(f"🎲 **Szanse 1X2:** `{home_p}%` | `{draw_p}%` | `{away_p}%`")
                
                st.markdown(f"🎯 **Przewidywane strzały ogółem:** `{shots_est}`")
                
                if shots_est >= 30.0:
                    st.success(f"Analiza: 🔥 Wysoki potencjał (30+ strzałów) na dzień {formatted_date}")
                else:
                    st.warning(f"Analiza: ⚡ Średni potencjał (<30 strzałów) na dzień {formatted_date}")
                st.markdown("---")
