import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_plotly_events import plotly_events
import json

# Configurare pagină
st.set_page_config(
    page_title="Analiza Economică - Județele României",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pentru styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5em;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8em;
        color: #2E86C1;
        border-bottom: 2px solid #3498DB;
        padding-bottom: 10px;
        margin: 20px 0;
    }
    .info-box {
        
        border-left: 5px solid #3498DB;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .methodology-step {
        
        border: 1px solid #DEE2E6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .step-number {
        
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar pentru navigare
st.sidebar.title("📋 Navigare")
page = st.sidebar.selectbox(
    "Selectează secțiunea:",
    ["🏠 Home", "📊 Dashboard", "🔬 Metodologie"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Platformă interactivă pentru:**
- Scoring regional bazat pe date economice reale
- Analiza comparativă a județelor din România
- Explorarea dimensiunilor economice cheie: forță de muncă, urbanizare, stabilitate etc.
- Susținerea deciziilor strategice prin insight-uri vizuale""")

# Funcții pentru încărcarea datelor
@st.cache_data
def load_geojson():
    try:
        with open("../baze/ro.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Fișierul ro.json nu a fost găsit. Verifică calea către fișier.")
        return None

@st.cache_data
def load_main_data():
    try:
        return pd.read_csv("tabel_final.csv")
    except FileNotFoundError:
        st.error("Fișierul tabel_final.csv nu a fost găsit.")
        return None
    
@st.cache_data
def load_tooltip_data():
    try:
        return pd.read_csv("tabel_tooltip.csv")
    except FileNotFoundError:
        st.error("Fișierul tabel_tooltip.csv nu a fost găsit.")
        return None

@st.cache_data
def load_all_datasets():
    datasets = {}
    files = {
        'populatie': "../baze/populatie_2024.csv",
        'pop_activa': "../baze/populatia_activa_2023.csv",
        'firme': "../baze/numar_firme2023.csv",
        'firme_1000': "../baze/trenduri.csv",
        'somaj': "../baze/rata_somaj_2023.csv",
        'salarii': "../baze/salariul_mediu2023.csv"
    }
    
    for key, file_path in files.items():
        try:
            datasets[key] = pd.read_csv(file_path)
        except FileNotFoundError:
            st.warning(f"Fișierul {file_path} nu a fost găsit.")
            datasets[key] = None
    
    return datasets

# ===============================
# PAGINA HOME
# ===============================
if page == "🏠 Home":
    st.markdown('<h1 class="main-title">📊 Economic Scoreboard România</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Scopul Aplicației</h3>
        <p>O platformă interactivă care oferă o imagine de ansamblu asupra potențialului economic regional din România, 
            cu scoruri calculate din date actuale și indicatori economici esențiali.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">🔍 Ce vei găsi în aplicație</div>', unsafe_allow_html=True)
        st.markdown("""
        **📊 Dashboard Interactiv:**
        - **Hartă Interactivă**: Vizualizarea potențialului economic pe hartă
        - **Grafice Comparative**: Top județe după indicatori economici
        - **Tabel Rezumativ**: Date complete și posibilitate de export
        
        **📈 Dimensiuni Analizate:**
        - Piață locală
        - Forță de muncă
        - Competiție & intensitate economică
        - Infrastructură & urban
        - Stabilitate economică
        """)
    
    with col2:
        st.markdown('<div class="section-header">📋 Surse de Date</div>', unsafe_allow_html=True)
        st.markdown("""
        **🏛️ Instituții Oficiale:**
        - **INS** (Institutul Național de Statistică)
        
        """)
    
        st.markdown("""
    <div class="info-box">
        <h3>💡 Cum să folosești aplicația</h3>
        <p><strong>1. Dashboard:</strong> Explorează datele prin hărți interactive și grafice</p>
        <p><strong>2. Tabel Rezumativ:</strong> Consultă datele detaliate și exportă rezultatele</p>
        <p><strong>3. Metodologie:</strong> Înțelege cum au fost procesate și calculate datele</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistici rapide
    df = load_main_data()
    if df is not None:
        st.markdown('<div class="section-header">📊 Statistici Rapide</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Județe", len(df))
        with col2:
            st.metric("Potențial Maxim", f"{df['Potential'].max():.2f}")
        with col3:
            st.metric("Potențial Minim", f"{df['Potential'].min():.2f}")
        with col4:
            st.metric("Media Națională", f"{df['Potential'].mean():.2f}")

# ===============================
# PAGINA DASHBOARD
# ===============================
elif page == "📊 Dashboard":
    st.markdown('<h1 class="main-title">📊 Dashboard Economic Score</h1>', unsafe_allow_html=True)
    
    # Tab-uri pentru organizarea conținutului
    tab1, tab2, tab3 = st.tabs(["🗺️ Hartă Interactivă", "📊 Top Județe", "📋 Tabel Rezumativ"])
    
    with tab1:
        st.markdown('<div class="section-header">🗺️ Harta Interactivă a Potențialului Economic</div>', unsafe_allow_html=True)
        
        df = load_main_data()
        tooltip_df = load_tooltip_data()
        geojson_data = load_geojson()
        
        if df is not None and tooltip_df is not None and geojson_data is not None:
            # Combină datele de bază cu datele pentru tooltip
            df_combined = df.merge(tooltip_df, on='Judet', how='left')
            df_combined.rename(columns={"Potential_x": "Potential"}, inplace=True)
            # Creează hover template personalizat
            hover_template = (
                "<b>%{customdata[0]}</b><br>"
                "🏛️ <b>Regiune:</b> %{customdata[1]}<br>"
                "📊 <b>Potențial Economic:</b> %{customdata[2]:.2f}<br>"
                "🇷🇴 <b>Media Țării:</b> %{customdata[3]:.2f}<br>"
                "🏘️ <b>Media Regiunii:</b> %{customdata[4]:.2f}<br>"
                "📈 <b>vs Media Țării:</b> %{customdata[5]:+.2f}<br>"
                "📉 <b>vs Media Regiunii:</b> %{customdata[6]:+.2f}<br>"
                "<extra></extra>"
            )
            
            fig = px.choropleth(
                df_combined,
                geojson=geojson_data,
                locations="Judet",
                featureidkey="properties.name",
                color="Potential",  # Folosește coloana din df original
                color_continuous_scale="Viridis",
                title="Potențialul Economic al Județelor din România - Hover pentru detalii",
                hover_name="Judet",
                custom_data=[
                    'Judet', 'Regiune', 'Potential_y', 'Media Tarii', 
                    'Media Regiunii', 'Vs Media Tarii', 'Vs Media Regiunii'
                ]
            )
            
            # Actualizează hover template
            fig.update_traces(hovertemplate=hover_template)
            
            fig.update_geos(
                fitbounds="locations",
                visible=False,
                bgcolor='rgba(0,0,0,0)',
                projection_type='mercator'
            )
            
            fig.update_layout(
                width=1400,
                height=700,
                margin={"r":0, "t":50, "l":0, "b":0},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                geo=dict(bgcolor='rgba(0,0,0,0)'),
                legend=dict(
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='black',
                    borderwidth=1
                )
            )
            
            fig.update_traces(
                colorbar=dict(
                    title='Potențial Economic',
                    tickfont=dict(color='black'),
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='black',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Informații despre tooltip
            st.info("💡 **Interacțiune:** Fă hover peste orice județ pentru a vedea informații detaliate: regiune, comparații cu media națională și regională!")
            
            # Legendă pentru înțelegerea comparațiilor
            with st.expander("📖 Cum să interpretezi datele din hover"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **📊 Indicatori afișați:**
                    - **Potențial Economic**: Scorul calculat pentru județ
                    - **Media Țării**: Media națională (43.09)
                    - **Media Regiunii**: Media pentru regiunea din care face parte județul
                    """)
                with col2:
                    st.markdown("""
                    **📈 Comparații:**
                    - **vs Media Țării**: Diferența față de media națională
                    - **vs Media Regiunii**: Diferența față de media regională
                    """)
        
        else:
            st.error("Nu s-au putut încărca toate fișierele necesare pentru hartă (tabel_final.csv, tabel_tooltip.csv, ro.json).")
    
    
    with tab2:
        st.markdown('<div class="section-header">📊 Top Județe după Potențial Economic</div>', unsafe_allow_html=True)
        
        df = load_main_data()
        if df is not None:
            df["Potential"] = df["Potential"].round(2)
            df = df.sort_values("Potential", ascending=False)
            
            fig = px.bar(
                df,
                x="Judet",
                y="Potential",
                color="Potential",
                color_continuous_scale="Viridis",
                text="Potential",
                title="Clasificarea Județelor după Potențial Economic",
            )
            
            fig.update_layout(
                xaxis=dict(
                    categoryorder="total descending",
                    range=[-0.5, 9.5],
                    rangeslider=dict(
                        visible=True,
                        range=[0, len(df)-1]
                    ),
                    tickangle=-45,
                ),
                yaxis=dict(range=[0, df["Potential"].max() + 5]),
                height=700,
                margin=dict(l=60, r=60, t=80, b=180),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            fig.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"📊 Afișate primele 10 județe din {len(df)} total. Folosește slider-ul pentru a naviga prin toate județele.")
            
            # Top 5 și Bottom 5
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🏆 Top 5 Județe")
                top_5 = df.head(5)[['Judet', 'Potential']]
                for idx, row in top_5.iterrows():
                    st.write(f"**{row['Judet']}**: {row['Potential']:.2f}")
            
            with col2:
                st.subheader("📉 Ultimele 5 Județe")
                bottom_5 = df.tail(5)[['Judet', 'Potential']].sort_values('Potential', ascending=True)
                for idx, row in bottom_5.iterrows():
                    st.write(f"**{row['Judet']}**: {row['Potential']:.2f}")
    
    with tab3:
        st.markdown('<div class="section-header">📋 Tabel Rezumativ - Indicatori Economici</div>', unsafe_allow_html=True)
        
        datasets = load_all_datasets()
        
        # Verifică dacă toate dataset-urile au fost încărcate
        if all(df is not None for df in datasets.values()):
            # Curățare și preprocesare
            for key, df in datasets.items():
                if "Unnamed: 0" in df.columns:
                    df.drop(columns=["Unnamed: 0"], inplace=True)
                datasets[key] = df.groupby("Judet", as_index=False).mean(numeric_only=True)
            
            # Creare tabel rezumativ
            df_rezumat = datasets['populatie']
            for key in ['pop_activa', 'firme', 'firme_1000', 'somaj', 'salarii']:
                df_rezumat = df_rezumat.merge(datasets[key], on="Judet", how="left")
            
            # Redenumire coloane
            column_mapping = {
                "Populatie": "Populație 2024",
                "Pop_Activa_2023": "Populație Activă 2023",
                "Nr_Firme_2023": "Număr Firme 2023",
                "Firme_per_1000": "Firme la 1000 locuitori",
                "Rata_Somaj_2023": "Rată Șomaj 2023 (%)",
                "Salariu_Mediu_2023": "Salariu Mediu Net 2023 (RON)"
            }
            
            for old_col, new_col in column_mapping.items():
                if old_col in df_rezumat.columns:
                    df_rezumat = df_rezumat.rename(columns={old_col: new_col})
            
            # Afișare tabel
            st.dataframe(df_rezumat, use_container_width=True, hide_index=True)

            
            # Opțiuni de export
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Descarcă CSV",
                    data=df_rezumat.to_csv(index=False).encode('utf-8'),
                    file_name='tabel_rezumativ_economic.csv',
                    mime='text/csv',
                )
            
            with col2:
                # Pentru Excel
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_rezumat.to_excel(writer, index=False, sheet_name='Indicatori_Economici')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📥 Descarcă Excel",
                    data=excel_data,
                    file_name='tabel_rezumativ_economic.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            
            # Statistici despre tabel
            st.markdown("### 📈 Statistici Rapide")
            col1, col2, col3, col4, col5 = st.columns(5)

            numeric_cols = df_rezumat.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 0:
                with col1:
                    st.metric("Județe Analizate", len(df_rezumat))
                with col2:
                    if "Populație 2024" in df_rezumat.columns:
                        st.metric("Populație Totală", f"{df_rezumat['Populație 2024'].sum():,.0f}")
                with col3:
                    if "Numar Firme" in df_rezumat.columns:
                        st.metric("Total Firme", f"{df_rezumat['Numar Firme'].sum():,.0f}")
                with col4:
                    if "Salariul Mediu Net (RON)" in df_rezumat.columns:
                        st.metric("Salariul Mediu Național", f"{df_rezumat['Salariul Mediu Net (RON)'].mean():.0f} RON")
                with col5:
                    if "Rata Somaj (%)" in df_rezumat.columns:
                        st.metric("Rata Medie a Șomajului", f"{df_rezumat['Rata Somaj (%)'].mean():.2f}%")
            else:
                st.error("Nu s-au putut încărca toate bazele de date necesare pentru tabelul rezumativ.")

# ===============================
# PAGINA METODOLOGIE
# ===============================
elif page == "🔬 Metodologie":
    st.markdown('<h1 class="main-title">🔬 Metodologia de Dezvoltare</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>📋 Prezentare Generală</h3>
        <p>Această secțiune detaliază pas cu pas procesul de dezvoltare al aplicației de analiză economică, 
        de la colectarea datelor până la implementarea finală.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasul 1
    st.markdown("""
    <div class="methodology-step">
        <h3><span class="step-number">1</span>Colectarea și Organizarea Datelor</h3>
        <p><strong>Surse de date utilizate:</strong></p>
        <ul>
            <li><strong>populatie_2024.csv</strong> - Date despre populația pe județe (INS)</li>
            <li><strong>populatia_activa_2023.csv</strong> - Populația activă pe județe (INS)</li>
            <li><strong>numar_firme2023.csv</strong> - Numărul de firme înregistrate (INS)</li>
            <li><strong>trenduri.csv</strong> - Evolutia salariului mediu/ratei șomajului (Calcul realizat pe baza evoluției ratei șomajului și a salariului mediu (2019–2023), conform datelor INS.)</li>
            <li><strong>rata_somaj_2023.csv</strong> - Rata șomajului pe județe (INS)</li>
            <li><strong>salariul_mediu2023.csv</strong> - Salariul mediu net (INS)</li>
            <li><strong>venit_gosp_2024.csv</strong> - Venitul mediu lunar al unei gospodarii per Regiune (INS)</li>
            <li><strong>procent_urbanizare.csv</strong> - Procentul urbanizării fiecărui județ (INS)</li>
            <li><strong>firme_per_mie.csv</strong> - Numărul de firme per 1000 locuitori (Indicator construit folosind date din numar_firme2023.csv și populatie_2024.csv.)</li>
            <li><strong>ro.json</strong> - Coordonatele geografice ale județelor (simplemaps.com)</li>
        </ul>
        <p><strong>Provocări întâlnite:</strong> Standardizarea formatului datelor, eliminarea duplicatelor, 
        gestionarea valorilor lipsă.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasul 2
    st.markdown("""
    <div class="methodology-step">
        <h3><span class="step-number">2</span>Preprocesarea și Curățarea Datelor</h3>
        <p><strong>Operații efectuate:</strong></p>
        <ul>
            <li>Eliminarea coloanelor de index automat generate ("Unnamed: 0")</li>
            <li>Agregarea datelor prin gruparea după județ folosind media valorilor</li>
            <li>Standardizarea numelor județelor pentru consistență</li>
            <li>Scalarea Min-Max a fost aplicată tuturor indicatorilor pentru a construi un scor comparabil între județe.</li>
            <li>Gruparea variabilelor în funcție de dimensiunile economice pe care le reflectă, pentru o analiză structurată.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasul 3
    st.markdown("""
    <div class="methodology-step">
        <h3><span class="step-number">3</span>Calculul Indicatorului de Potențial Economic</h3>
        <p><strong>Formula utilizată:</strong></p>
        <p>Potențialul Economic = w1 * Piață locală + w2 * Forță de muncă + w3 * Competiție & intensitate economică + w4 * Infrastructură & urban + w5 * Stabilitate economică </p>
        <p><strong>Ponderile aplicate:</strong></p>
        <ul>
            <li>Piață locală: w1 = 25%</li>
            <li>Forță de muncă: w2 = 20%</li>
            <li>Competiție & intensitate economică: w3 = 25%</li>
            <li>Infrastructură & urban: w4 = 15%</li>
            <li>Stabilitate economică: w5 = 15%</li>
        </ul>
        <p><em>Nota: Valorile au fost normalizate pe scala 0-100 pentru comparabilitate. 
            Procentele (greutățile) au fost stabilite intern, pe baza importanței percepute a fiecărei dimensiuni în contextul analizei.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasul 4
    st.markdown("""
    <div class="methodology-step">
        <h3><span class="step-number">4</span>Dezvoltarea Componentelor de Vizualizare</h3>
        <p><strong>1. Harta Interactivă:</strong></p>
        <ul>
            <li>Utilizare Plotly Express cu date GeoJSON</li>
            <li>Scală de culori Viridis pentru diferențierea valorilor</li>
            <li>Configurare proiecție Mercator pentru România</li>
        </ul>
        <p><strong>2. Graficul Bar Chart:</strong></p>
        <ul>
            <li>Sortarea județelor descrescător după potențial</li>
            <li>Slider interactiv pentru navigarea prin toate județele</li>
            <li>Afișarea valorilor exacte pe fiecare bară</li>
        </ul>
        <p><strong>3. Tabelul Rezumativ:</strong></p>
        <ul>
            <li>Combinarea indicatorilor rezumativi într-un singur tabel</li>
            <li>Funcționalitate de export în CSV și Excel</li>
            <li>Calculul statisticilor sumare</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasul 5
    st.markdown("""
    <div class="methodology-step">
        <h3><span class="step-number">5</span>Integrarea în Aplicația Streamlit</h3>
        <p><strong>Arhitectura aplicației:</strong></p>
        <ul>
            <li><strong>Sidebar Navigation:</strong> Meniu pentru navigarea între secțiuni</li>
            <li><strong>Caching:</strong> Optimizarea încărcării datelor cu @st.cache_data</li>
            <li><strong>Responsive Design:</strong> Layout adaptat pentru diferite rezoluții</li>
            <li><strong>Error Handling:</strong> Gestionarea cazurilor când fișierele lipsesc</li>
        </ul>
        <p><strong>Tehnologii utilizate:</strong></p>
        <ul>
            <li>Streamlit - Framework pentru aplicații web</li>
            <li>Plotly - Vizualizări interactive</li>
            <li>Pandas - Manipularea datelor</li>
            <li>JSON - Procesarea datelor geografice</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasul 6
    st.markdown("""
    <div class="methodology-step">
        <h3><span class="step-number">6</span>Testare și Optimizare</h3>
        <p><strong>Aspecte testate:</strong></p>
        <ul>
            <li>Funcționalitatea tuturor componentelor interactive</li>
            <li>Compatibilitatea cu diferite browsere</li>
            <li>Responsivitatea pe dispozitive mobile</li>
        </ul>
        <p><strong>Optimizări implementate:</strong></p>
        <ul>
            <li>Caching pentru datele statice</li>
            <li>Lazy loading pentru componentele mari</li>
            <li>Compresie pentru fișierele de export</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Provocări și soluții
    st.markdown('<div class="section-header">⚡ Provocări Întâlnite și Soluții</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🚧 Provocări:**
        - **Date inconsistente**: Formate diferite între surse
        - **Performanță**: Încărcare lentă pentru hărți mari  
        """)
    
    with col2:
        st.markdown("""
        **✅ Soluții:**
        - **Standardizare**: Etapă de curățare și scalare a datelor, realizată după intervențiile manuale.
        - **Optimizare**: Caching și lazy loading
        """)
    
    # Concluzii
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Rezultate Obținute</h3>
        <p>Aplicația finală oferă o platformă completă pentru analiza potențialului economic al județelor din România, cu vizualizări interactive, export de date și metodologie transparentă. 
        Sistemul poate fi extins cu indicatori suplimentari și actualizări automate ale datelor.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px;'>
    📊 Platformă de analiză a potențialului economic al județelor din România</br>  
    🔄 Ultima actualizare: August 2025</br>  
    💼 Creat de NexZone | 🔧 Construit cu Streamlit
</div>
""", unsafe_allow_html=True)