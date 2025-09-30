import streamlit as st
from collections import defaultdict
import datetime

# Mappatura lettere → nomi reali
mapping = {
    "M": "Matrone",
    "A": "Ancora",
    "B": "Balzano",
    "G": "Garofalo",
    "S": "Sorrentino",
    "T": "Tufano"
}
sostituti = ["A", "B", "G", "S", "T"]

# Stato persistente dei turni
if "turni" not in st.session_state:
    st.session_state.turni = {c: 0 for c in sostituti}

if "data_corrente" not in st.session_state:
    st.session_state.data_corrente = datetime.date(2025, 9, 11)  # inizio scuola Campania

# Giorni di vacanza
vacanze = [
    (datetime.date(2025, 11, 1), datetime.date(2025, 11, 1)),
    (datetime.date(2025, 12, 23), datetime.date(2026, 1, 6)),
    (datetime.date(2026, 4, 2), datetime.date(2026, 4, 7)),
    (datetime.date(2025, 12, 8), datetime.date(2025, 12, 8)),
    (datetime.date(2026, 4, 25), datetime.date(2026, 4, 25)),
    (datetime.date(2026, 5, 1), datetime.date(2026, 5, 1)),
    (datetime.date(2026, 6, 2), datetime.date(2026, 6, 2))
]

fine_scuola = datetime.date(2026, 6, 6)

def giorno_valido(data):
    # escludi sabato/domenica
    if data.weekday() in (5, 6):
        return False
    # escludi vacanze
    for start, end in vacanze:
        if start <= data <= end:
            return False
    return True

def prossimo_giorno(data):
    next_day = data + datetime.timedelta(days=1)
    while not giorno_valido(next_day) and next_day <= fine_scuola:
        next_day += datetime.timedelta(days=1)
    return next_day

st.title("Gestione Turni – Calendario Scolastico Campania 2025/26")

oggi = st.session_state.data_corrente
st.write(f"📅 Data di oggi: **{oggi.strftime('%d/%m/%Y')}**")

presenti = st.multiselect(
    "Seleziona i presenti oggi:",
    list(mapping.keys()),
    format_func=lambda x: mapping[x]
)

if st.button("Assegna sostituto per oggi"):
    if "M" not in presenti:
        candidati = [p for p in presenti if p in sostituti]
        if candidati:
            min_turni = min(st.session_state.turni[c] for c in candidati)
            candidati_min = [c for c in candidati if st.session_state.turni[c] == min_turni]
            scelto = sorted(candidati_min)[0]
            st.session_state.turni[scelto] += 1
            st.success(f"Sostituto di **{mapping['M']}**: **{mapping[scelto]}**")
        else:
            st.error("⚠ Nessun sostituto disponibile oggi!")
    else:
        st.info(f"{mapping['M']} è presente — nessuna sostituzione necessaria.")

if st.button("Vai al giorno successivo"):
    st.session_state.data_corrente = prossimo_giorno(st.session_state.data_corrente)

st.subheader("Turni cumulativi")
for c in sostituti:
    st.write(f"{mapping[c]}: {st.session_state.turni[c]} turni")
