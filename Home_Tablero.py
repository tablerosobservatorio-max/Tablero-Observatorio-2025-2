

# 📦 Cargando librerías necesarias
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

# 🧭 Configurar la página
st.set_page_config(page_title="Observatorio de Salud Mental", page_icon="📈", layout="wide")

# ===============================
# 📋 Menú lateral con navegación
with st.sidebar:
    selected = option_menu(
        menu_title="Menú Principal",
        options=["Inicio", "Análisis", "Datos"],
        icons=["house", "bar-chart", "table"],
        default_index=0
    )

# ======================================
# Nuevo comentario1
# Nuevo comentario2 

# 🏠 Página de inicio / presentación
if selected == "Inicio":
    st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>📊 Observatorio de Salud Mental de la Orinoquia Colombiana</h1>", unsafe_allow_html=True)

    st.markdown("""
        <h3 style='text-align: center; color: #333333;'>Análisis exploratorio, y modelamiento de enfermedades de Salud Mental (2018 - 2022)</h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: justify; font-size: 18px; color: #444444;">
        Este tablero interactivo tiene como objetivo mostrar la distribución de enfermedades más relevantes reportadas
        por los subsectores del país durante los años 2018 - 2022. Con visualizaciones dinámicas, métricas clave
        y comparaciones por departamento, buscando facilitar la toma de decisiones informadas en salud pública.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("##")

    # ===============================
    
    
    #st.image("MENTAL2.png", width=200, caption="Observatorio de Salud Mental")
    #st.markdown("<h2 style='text-align: center;'>Observatorio de Salud Mental</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])  # crea 3 columnas (izq, centro, der) 
    with col2:     # usamos solo la columna del medio 
        st.image("Observatorio_Imagen1.png", width=450) 
    #st.markdown("<h2 style='text-align: center;'>Observatorio de Salud Mental</h2>", unsafe_allow_html=True)
    
    
    st.markdown("##")
    
    
    
    
    
    
    
    # ===============================
    # 🔹 Recuadro elegante informativo
    st.markdown("""
    <div style="border: 2px solid #4B8BBE; padding: 20px; border-radius: 15px; background-color: #F5F5F5;">
        <h4 style="color: #4B8BBE;">🔎 ¿Qué encontrarás en este tablero?</h4>
        <ul style="color: #333333; font-size: 16px;">
            <li>Estadísticas por grupo de enfermedad</li>
            <li>Tendencias por departamento</li>
            <li>Comparaciones por tasa ajustada</li>
            <li>Visualizaciones interactivas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Otras páginas (dejar en blanco por ahora)
elif selected == "Análisis":
    st.markdown("🚧 Página en construcción: Aquí irán los gráficos analíticos...")

elif selected == "Datos":
    st.markdown("📄 Aquí podrás explorar los datos fuente...")





#st.sidebar.image("data/Logo_UNILLANOS.png",caption="")      # LOGO
st.sidebar.image("Logo_UNILLANOS.png",caption="")            # LOGO













# PARA EJECUTAR EL DASHBOARD, CORRER LAS SIGUIENTES LÍNEAS EN C:
# Invoca la carpeta donde está ubicado el archivo:  --->

# cd C:\Users\cesar\Downloads\TABLERO_STREAMLIT_DASHBOARD\DASHBOARD_STREAMLIT_COMPLETO




# Invocando el archivo: ---->
# python streamlit_app.py (este comando no corrió... entonces ejecutar el siguiente: ----> )

# streamlit run Home_Tablero.py



























