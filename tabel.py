import streamlit as st
import pandas as pd

st.title("Tabel Rezumativ - Indicatori Economici Județe")
st.write("Această aplicație combină mai multe baze de date într-un tabel rezumativ interactiv.")

# =============================
# 1. Încărcare baze de date
# =============================

populatie = pd.read_csv("../baze/populatie_2024.csv")  # coloane: Judet, Populatie_2024
pop_activa = pd.read_csv("../baze/populatia_activa_2023.csv")  # coloane: Judet, Pop_Activa_2023
firme = pd.read_csv("../baze/numar_firme2023.csv")  # coloane: Judet, Nr_Firme_2023
firme_1000 = pd.read_csv("../baze/trenduri.csv")  # coloane: Judet, Firme_per_1000
somaj = pd.read_csv("../baze/rata_somaj_2023.csv")  # coloane: Judet, Rata_Somaj_2023
salarii = pd.read_csv("../baze/salariul_mediu2023.csv")  # coloane: Judet, Salariu_Mediu_2023

# =============================
# 2. Curatare și preprocesare date
# =============================

for df in [populatie, pop_activa, firme, firme_1000, somaj, salarii]:
    if "Unnamed: 0" in df.columns:
        df.drop(columns=["Unnamed: 0"], inplace=True)

# Daca Exista mai multe randuri pe judet, se face agregare prin medie
populatie = populatie.groupby("Judet", as_index=False).mean(numeric_only=True)
pop_activa = pop_activa.groupby("Judet", as_index=False).mean(numeric_only=True)
firme = firme.groupby("Judet", as_index=False).mean(numeric_only=True)
firme_1000 = firme_1000.groupby("Judet", as_index=False).mean(numeric_only=True)
somaj = somaj.groupby("Judet", as_index=False).mean(numeric_only=True)
salarii = salarii.groupby("Judet", as_index=False).mean(numeric_only=True)

# =============================
# 3. Creare tabel rezumativ
# =============================

df_rezumat = populatie \
    .merge(pop_activa, on="Judet", how="left") \
    .merge(firme, on="Judet", how="left") \
    .merge(firme_1000, on="Judet", how="left") \
    .merge(somaj, on="Judet", how="left") \
    .merge(salarii, on="Judet", how="left") \

st.subheader("Tabel Rezumativ Județe")
st.dataframe(df_rezumat)

# =============================
# 4. Redenumire coloane pentru claritate   
# =============================

df_rezumat = df_rezumat.rename(columns={
    "Populatie": "Populație 2024",
    "Pop_Activa_2023": "Populație Activă 2023",
    "Nr_Firme_2023": "Număr Firme 2023",
    "Firme_per_1000": "Firme la 1000 locuitori",
    "Rata_Somaj_2023": "Rată Șomaj 2023 (%)",
    "Salariu_Mediu_2023": "Salariu Mediu 2023 (RON)"
})
# 4. Opțiune de descărcare Excel
# =============================
st.download_button(
    label="Descarcă tabelul în Excel",
    data=df_rezumat.to_csv(index=False).encode('utf-8'),
    file_name='tabel_rezumativ.csv',
    mime='text/csv',
)