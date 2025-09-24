# Cargando las Librerías:
# ==============================================================================

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import numpy as np
import modulo_osm as osm

# ----------------------------------------------------------
# Definicion de colores
# 0."Azul_os", 1."Rojo", 2."Azul_cl", 3."Gris", 4."Verde", 5."Naranja", 6."Morado"
P_Colores = ["#2A3180","#E5352B","#39A8E0","#9D9D9C","#009640","#F28F1C","#662681"]
#st.session_state['P_Colores']=P_Colores
#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Convivencia Social", layout="wide")
st.markdown("<h2 style='text-align: left;color: #39A8E0;'>CONVIVENCIA SOCIAL - MORBILIDAD</h2>", unsafe_allow_html=True)

#-------------------------------------------------------------------------------
#st.markdown("""
#        <div style="text-align: justify; font-size: 18px; color: #444444;">
#        Esta sección presenta datos de morbilidad, para enfermedades y problemas\ 
#        de salud que afectan a la población relacionada con factores que influyen\ 
#        en la convivencia social, incluyendo problemáticas de salud mental y\ 
#       condiciones asociadas. La información permite identificar las principales \
#        afectaciones en salud que pueden incidir en dinámicas sociales y el \
#        bienestar colectivo.
#        </div>""", unsafe_allow_html=True)

#-------------------------------------------------------------------------------
# LECTURA Y PREPARACION DE FUENTES DE DATOS
#-------------------------------------------------------------------------------
df_mb2 = osm.bd_morbilidad('Morbilidad2')

df_pob2 = osm.bd_poblacion('Pob2',2024)
df_pob2=df_pob2[df_pob2['region']=='Orinoquía'].reset_index(drop=True)

df_mb3 = osm.bd_morbilidad('Morbilidad3')
#st.session_state['df_mb3'] = df_mb3

df_pob3 = osm.bd_poblacion('Pob3',2024)
#df_pob=df_pob[df_pob['region']=='Orinoquía'].reset_index(drop=True)
#st.session_state['df_pob3'] = df_pob3

#-------------------------------------------------------------------------------
# FILTROS
#-------------------------------------------------------------------------------


col1, col2 = st.columns([4,6])

with col1:
  # 1. Botones por departamento
  depto_sel=st.pills("Departamento", df_pob2['departamento'].unique(), 
                       selection_mode="single",default='Meta')
  df_mb2_f = df_mb2[df_mb2["departamento"] == depto_sel]
  
    # 2. Crear un selector para que el usuario elija uno o varios grupos
  grupos = df_mb2_f['grupo'].unique().tolist()
  grupo_sel = st.selectbox("Selecciona un grupo de evento", grupos)
  df_mb2_f = df_mb2_f[df_mb2["grupo"] == grupo_sel]
  
with col2:
  #  2. Botones por año
  anios=sorted(df_mb3['anio'].unique()) 
  anio_sel = st.pills("Año", anios, selection_mode="single",default=max(anios))
    # 3. Crear un selector para el evento
  eventos = df_mb2_f['Enfermedad_Evento'].unique().tolist()
  eventos.insert(0, "Todos")
  evento_sel = st.selectbox("Seleccione el evento de interes", eventos)

#-------------------------------------------------------------------------------
# Contenido Morbilidad
#-------------------------------------------------------------------------------

Total_casos=df_mb3[(df_mb3['grupo']==grupo_sel) & (df_mb3['anio']==anio_sel)]['Total'].sum()
Total_Pob=df_pob3[df_pob3['anio']==anio_sel]['Total'].sum()
Tasa_grupo_ORQ=(Total_casos/Total_Pob).round(1)


# 2. Filtrar el DataFrame según la selección del usuario

if evento_sel != "Todos":
  df_mb2_f = df_mb2_f[df_mb2_f["Enfermedad_Evento"] == evento_sel]

df_pob2_f = df_pob2.copy()
df_pob2_f=df_pob2_f[df_pob2_f['departamento']==depto_sel]
total_pob=df_pob2_f['Total'].sum()

df_mb2_ft=df_mb2_f.groupby(['anio','sexo'])['Total'].sum().reset_index()

Total_casos_depto=df_mb2_f[df_mb2_f['anio']==anio_sel]['Total'].sum()
Tasa_grupo_depto=(Total_casos_depto/total_pob).round(1)
# Tarjetas con indiadores relevantes
#-------------------------------------------------------------------------------




col1, col2 = st.columns(2)
with col1:
  st.markdown("<h3 style='text-align: left;color: #39A8E0;'>Casos por edad</h3>", unsafe_allow_html=True)
  G_bar=osm.diag_barras_apil(df_mb2_f[df_mb2_f['anio']==anio_sel],'nombre_cat_edad','Total',
                                'sexo','','subtitulo',P_Colores[4:],xlab='Edad',ylab='No. de casos')
  st.plotly_chart(G_bar, use_container_width=True)
with col2:
  st.markdown("<h3 style='text-align: left;color: #39A8E0;'>Tendencia por años</h3>", unsafe_allow_html=True)
  G_Lineas=osm.diag_lineas(df_mb2_ft,'anio','Total','sexo','','N. Casos',P_Colores[4:])
  st.plotly_chart(G_Lineas, use_container_width=True)
  
  
#-------------------------------------------------------------------------------
# Diagrama de radar usando tasa por municipio por sexo y filtro por año
#-------------------------------------------------------------------------------

# Filtrado de la base y calculo de las tasas por municipio

#depto_sel='Meta'
#grupo_sel='Agresiones'
#anio_sel=2022

df_mb3_f=df_mb3[(df_mb3['departamento']==depto_sel) & (df_mb3['grupo']==grupo_sel) & (df_mb3['anio']==anio_sel)]
df_pob3_f=df_pob3[(df_pob3['departamento']==depto_sel) & (df_pob3['anio']==anio_sel)]

df_mb3_f2=df_mb3_f.groupby(['id_mpio','municipio','sexo'])['Total'].sum().reset_index()
df_pob3_f.rename(columns={'Total':'pob10'},inplace=True)
df_mb3_f2=df_mb3_f2[['id_mpio','municipio','sexo','Total']].merge(df_pob3_f[['municipio','sexo','pob10']], on=['municipio','sexo'])
df_mb3_f2['Tasa_mb'] = (df_mb3_f2['Total'] / df_mb3_f2['pob10']).round(1)

#col1, col2 = st.columns(2)
Tabla_Tasas= df_mb3_f2.pivot(index=['id_mpio','municipio'],columns='sexo',values='Tasa_mb').reset_index()
Tabla_Tasas = Tabla_Tasas.rename(columns={'municipio': 'Municipio'})
#with col1:
G_bar2=osm.diag_barras_apil_h(df_mb3_f2,'Tasa_mb','municipio','sexo',
                              '', grupo_sel,
                              P_Colores[4:],bmode='group',ylab='Municipios',xlab='Tasa x 100.000 hab.')
G_bar2.update_traces(
    hovertemplate=(
        f"Municipio: %{{y}}<br>"
        f"Tasa Morbilidad: %{{x:.2f}}<extra></extra>"
    )
)

col1, col2 = st.columns(2)
with col1:

  st.markdown("<h3 style='text-align: left;color: #39A8E0;'>Morbilidad por municipio</h3>", unsafe_allow_html=True)
  Mp_cr=osm.mapa_crp(df_mb3_f2,'Tasa_mb','data/mapa_gj2.geojson','Tasa morbilidad')
  st.plotly_chart(Mp_cr, use_container_width=True)
with col2:
  st.markdown("<h3 style='text-align: left;color: #39A8E0;'>Tasas de morbilidad por municipio y sexo</h3>", unsafe_allow_html=True)
  
  st.plotly_chart(G_bar2, use_container_width=True)

#----------------------------------------------------------------------------------------------------------------
#st.write("")
#st.write("")
st.markdown("##")

st.markdown("<h3 style='text-align: left;color: #39A8E0;'>EVENTOS DE CONVIVENCIA SOCIAL</h3>", unsafe_allow_html=True)
st.write("")

st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Accidentes de Transporte</h4>", unsafe_allow_html=True)
#----------------------------------------------------------------------------------------------------------------
st.write("")

df_mb2_Accid=df_mb2[df_mb2['grupo']=='Accidentes de transporte']
anio_max=df_mb2_Accid['anio'].max()
Total_casos_Accid=df_mb2_Accid[df_mb2['anio']==anio_max].groupby('departamento')['Total'].sum()
df_pob2['departamento']=df_pob2['departamento'].astype('object')

Total_Pob=df_pob2[df_pob2['anio']==anio_max].groupby('departamento')['Total'].sum()
Tasas_Accid=(Total_casos_Accid/Total_Pob).round(1)


# Definicion de colores
# 0."Azul_os", 1."Rojo", 2."Azul_cl", 3."Gris", 4."Verde", 5."Naranja", 6."Morado"
#P_Colores = ["#2A3180","#E5352B","#39A8E0","#9D9D9C","#009640","#F28F1C","#662681"]

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: #F28F1C;
        border: 3px solid #009640";
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        font-size: 1.5rem;
        color: #2A3180;
    /* Centrar contenido */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    </style>
     """, unsafe_allow_html=True)
# 
# 
#     /* Asegurar que los textos hijos también estén centrados */
#     div[data-testid="stMetric"] > div {
#         width: 100%;
#         text-align: center;
#     }
a,b,c,d,e,f =st.columns(6)

with b:
  st.metric('Arauca',Tasas_Accid[0],border=True)
with c:
  st.metric('Casanare',Tasas_Accid[1],border=True)
with d:
  st.metric('Meta',Tasas_Accid[2],border=True)
with e:
  st.metric('Vichada',Tasas_Accid[3],border=True)
  
st.write("")


Tabla_Accid=df_mb2_Accid.groupby('Enfermedad_Evento')['Total'].sum().reset_index()
G_Donut=osm.diag_donut(Tabla_Accid['Enfermedad_Evento'], Tabla_Accid['Total'], titulo="", 
colores=["#2A3180","#E5352B","#39A8E0","#9D9D9C"])




col1, col2 =st.columns(2)

with col1:
  st.plotly_chart(G_Donut, use_container_width=True)
with col2:
  T_Accid_sel=st.pills("Tipo de accidente",df_mb2_Accid['Enfermedad_Evento'].unique(), 
                                       selection_mode="single", key="TAcc_Sel",default='Acc. Transporte terrestre')
  df_mb2_Accid_f=df_mb2_Accid[df_mb2_Accid['Enfermedad_Evento']==T_Accid_sel]

  G_bar3=osm.diag_barras(df_mb2_Accid_f,'Total','Detalle',T_Accid_sel,P_Colores[4:],
                              ylab='Vehículo',xlab='No. Casos')

  st.plotly_chart(G_bar3, use_container_width=True)



