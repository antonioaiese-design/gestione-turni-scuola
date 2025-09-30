import streamlit as st
from collections import defaultdict

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

st.title("Gestione Turni – Sostituzione di Matrone")

presenti = st.multiselect(
    "Seleziona i presenti oggi:",
    list(mapping.keys()),
    format_func=lambda x: mapping[x]
)

if st.button("Assegna sostituto"):
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

st.subheader("Turni cumulativi")
for c in sostituti:
    st.write(f"{mapping[c]}: {st.session_state.turni[c]} turni")
