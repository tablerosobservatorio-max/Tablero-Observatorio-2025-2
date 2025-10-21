
# ===========================================
# Evaluación de propensión a esquizofrenia
# Niveles: Departamento, Municipio, Persona
# Modelos: Random Forest, XGBoost, NN, Scoring
# Visualización: Mapa de calor
# ===========================================

import math as mt
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import modulo_osm as osm

#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Simulación de Escenarios", layout="wide")
st.markdown("<h2 style='text-align: left;color: #39A8E0;'>Simulación de escenarios en salud mental</h2>", unsafe_allow_html=True)
#st.write("")
st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Modelo Ciudad</h4>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Simulación de Escenarios
# ------------------------------------------------------------------------------
df = pd.read_excel('data/Tabla_ModeloCiudad.xlsx')
df = pd.read_excel('data/Tabla_ModeloCiudad_Cat.xlsx',sheet_name='Tabla_Base')
df2 = pd.read_excel('data/Tabla_ModeloCiudad_Cat.xlsx',sheet_name='Tabla_Graf')

st.write("")

st.write("""En esta plataforma, se presenta un modelo de Machine Learning desarrollado
para estimar la probabilidad de que un municipio presente casos de enfermedades mentales. 
Este modelo utiliza información básica y accesible para el usuario, como niveles de 
incidencia en diferentes grupos de enfermedades mentales, cantidad de decesos asociados 
y el total de personas diagnosticadas con trastornos mentales en la región.
A partir de estos datos observables, el modelo simula diferentes escenarios para 
calcular un valor predictivo del riesgo o propensión a la presencia de enfermedades 
mentales en el municipio, lo que facilita la identificación temprana de áreas que 
podrían requerir atención prioritaria y recursos adicionales.
Esta herramienta busca apoyar la toma de decisiones informadas en salud pública, 
permitiendo a los gestores, académicos y responsables de políticas diseñar 
estrategias más efectivas, focalizadas y basadas en evidencia para mejorar la 
prevención, atención y seguimiento de la salud mental en los diferentes 
territorios.""")


Niveles2 = ["Bajo", "Alto"]
Niveles3 = ["Bajo", "Medio", "Alto"]

st.markdown("**Seleccione los niveles de las variables de interés para simular la probabilidad de enfermedades mentales a nivel de ciudad**")

a,b=st.columns([13.5,6.5])

with a:
  
  a1, a2=st.columns(2)
  with a1:
    NH_Sel = st.segmented_control("Numero de Hombres con enfermedades mentales", 
                             ["0 - 17","18 - 50","51 -120","121 o más"], 
                             selection_mode="single", key="NH_Sel")
  with a2:
    NM_Sel = st.segmented_control("Numero de Mujeres con enfermedades mentales", 
                             ["0 - 17","18 - 50","51 -120","121 o más"], 
                             selection_mode="single", key="NM_Sel")
  st.write("")                           
  c1, c2,c3=st.columns(3)
  with c1:
    MT_Sel = st.segmented_control("Numero de casos mortales", 
                                         sorted(df['Cat_Mortalidad'].unique()), 
                                         selection_mode="single", key="MT_Sel") 
    CS_Sel = st.segmented_control("Consumo de Sustancias", ["0 - 2","3 - 9","10 o más"], selection_mode="single", key="CS_Sel")
    SQ_Sel = st.segmented_control("Esquizofrenia", ["0 - 5","6 - 21","22 o más"], selection_mode="single", key="SQ_Sel")
    RM_Sel = st.segmented_control("Retraso Mental", ["0 - 3","4 - 14","15 o más"], selection_mode="single", key="RM_Sel")
  with c2: 
    SC_Sel = st.segmented_control("Síndromes del Comportamiento", ["0 - 2","3 - 10","11 o más"], selection_mode="single", key="SC_Sel")
    TM_Sel = st.segmented_control("Trastornos Mentales", ["0 - 2","3 - 14","15 o más"], selection_mode="single", key="TM_Sel")
    TA_Sel = st.segmented_control("Trastornos Afectivos", ["0 - 12","13 - 48","49 o más"], selection_mode="single", key="TA_Sel")
    TP_Sel = st.segmented_control("Trastornos de Personalidad", ["0 - 3","4 o más"], selection_mode="single", key="TP_Sel")
  with c3:
    TN_Sel = st.segmented_control("Trastornos de la Niñez", ["0 - 3","4 - 20","21 o más"], selection_mode="single", key="TN_Sel")
    TD_Sel = st.segmented_control("Trastornos del Desarrollo", ["0 - 5","6 - 34","35 o más"], selection_mode="single", key="TD_Sel")
    TR_Sel = st.segmented_control("Trastornos Neuróticos", ["0 - 12","13 - 60","61 o más"], selection_mode="single", key="TR_Sel")
  
  filtros = {
    'Cat_Tot_Hombres': NH_Sel,
    'Cat_Tot_Mujeres': NM_Sel,
    'Cat_Mortalidad': MT_Sel,
    'Cat_ConsumoSustancias': CS_Sel,
    'Cat_Esquizofrenia': SQ_Sel,
    'Cat_RetrasoMental': RM_Sel,
    'Cat_SindromComportam': SC_Sel,
    'Cat_TrastornosMentales': TM_Sel,
    'Cat_TrastornosAfectivos': TA_Sel,
    'Cat_TrastornosPersonalidad': TP_Sel,
    'Cat_TrastornosNiñez': TN_Sel,
    'Cat_TrastornoDesarrollo': TD_Sel,
    'Cat_TrastornosNeuróticos': TR_Sel
    }
  
      # Aplicar filtro iterando y acumulando condiciones
  df_filtrado = df.copy()
  for col, val in filtros.items():
    # Filtrar solo las filas que tengan el valor seleccionado en la columna categorizada
    if val is not None:
      df_filtrado = df_filtrado[df_filtrado[col] == val]
  
  
  n_reg=df_filtrado.shape[0]
  Prom_Score=round(100*df_filtrado['Score_Unico_Ordinal'].mean(),1)


#st.write("")

#,b=st.columns(2)
with b:
  st.write("")
  fig2=osm.plot_gauge(Prom_Score, '#2A3180', "%", "PROBABILIDAD", 100)
  st.plotly_chart(fig2, use_container_width=True)
  
# with b:
#   Tabla_DM=df2.groupby(['Departamento','Municipio'])['Score'].mean().reset_index()
#   Dpto_sel=st.pills('Departamento',Tabla_DM['Departamento'].unique(),selection_mode="single", key="Dpto_Sel",default='Meta')
#   Tabla_Mun=Tabla_DM[Tabla_DM['Departamento']==Dpto_sel][['Municipio','Score']]
#   Tabla_Mun['Probabilidad']=round(100*Tabla_Mun['Score'],1)
#   Tabla_Mun=Tabla_Mun[['Municipio','Probabilidad']]
#   st.markdown("""<h4 style='text-align: left; color: #39A8E0;'>Probabilidad por Municipio </h4>""",
#       unsafe_allow_html=True)
#   
#   st.dataframe(Tabla_Mun,hide_index=True)

  



