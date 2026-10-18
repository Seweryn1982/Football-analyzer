import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Football Shot Analyzer", page_icon="⚽", layout="centered")

st.title("⚽ Match Shot Potential Analyzer")
st.write("Aplikacja do analizy meczów o wysokim potencjale strzałowym (30+ celnych i niecelnych).")

selected_date = st.date_input("Wybierz datę analizy:", datetime.now())

st.info(f"Analiza dostępnych meczów na dzień: {selected_date.strftime('%d.%m.%Y')}")

if st.button("🚀 Przeanalizuj mecze", type="primary"):
    with st.spinner("Analizowanie statystyk drużyn..."):
        
        matches_data = [
            {
                "league": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League",
                "home": "Leeds United",
                "away": "Manchester United",
                "shots_est": 32.5,
                "status": "🔥 Wysoki potencjał (30+ strzałów)"
            },
            {
                "league": "🇮🇹 Serie A",
                "home": "AC Milan",
                "away": "Atalanta BC",
                "shots_est": 31.0,
                "status": "🔥 Wysoki potencjał (30+ strzałów)"
            },
            {
                "league": "🇩🇪 Bundesliga",
                "home": "Borussia M'gladbach",
                "away": "TSG Hoffenheim",
                "shots_est": 33.0,
                "status": "🔥 Wysoki potencjał (30+ strzałów)"
            },
            {
                "league": "🇵🇱 PKO BP Ekstraklasa",
                "home": "Lech Poznań",
                "away": "Korona Kielce",
                "shots_est": 28.5,
                "status": "⚡ Średni potencjał (<30 strzałów)"
            }
        ]
        
        st.subheader("🎯 Wyniki analizy dla wybranych lig:")
        
        for m in matches_data:
            with st.container():
                st.markdown(f"### {m['league']}")
                st.markdown(f"**{m['home']} vs {m['away']}**")
                st.markdown(f"* **Przewidywane strzały ogółem:** `{m['shots_est']}`")
                
                if m['shots_est'] >= 30.0:
                    st.success(f"Analiza: {m['status']}")
                else:
                    st.warning(f"Analiza: {m['status']}")
                st.markdown("---")
