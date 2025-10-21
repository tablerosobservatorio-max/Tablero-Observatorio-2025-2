
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
from streamlit_extras.add_vertical_space import add_vertical_space

#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Simulación de Escenarios", layout="wide")
st.markdown("<h2 style='text-align: left;color: #39A8E0;'>Simulación de escenarios en salud mental</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Modelo Persona</h4>", unsafe_allow_html=True)
# ------------------------------------------------------------------------------
# Simulación de Escenarios
# ------------------------------------------------------------------------------
#df = pd.read_excel('data/Tabla_ModeloCiudad.xlsx')
df = pd.read_excel('data/Tabla_MPersonas.xlsx',sheet_name='Sheet1')

st.write("")

st.write("""Este modelo de personas está diseñado para estimar la probabilidad de 
que una persona desarrolle un cuadro clínico grave relacionado con enfermedades mentales.
El modelo se calcula en función de algunas variables sociodemográficas y del historial 
médico-psiquiátrico que el usuario puede seleccionar. La utilidad principal de este modelo radica en su capacidad para proporcionar una 
evaluación personalizada del riesgo, apoyando la identificación temprana de 
individuos que podrían requerir atención prioritaria o intervenciones preventivas 
más intensivas.""")


st.markdown("**Seleccione características generales del grupo de personas para el cual se desea simular el escenario**")



add_vertical_space(1)
a, b = st.columns([13.5,6.5])
with a:
  
  a1,a2,a3,a4=st.columns([5,3,4,1.5])
  with a1:
    Dpto_sel = st.pills("Departamento", 
                           ["Arauca","Casanare","Meta","Vichada"], 
                           selection_mode="single",
                            key="Dpto",default="Meta")
  with a2:
    Sexo_sel = st.pills("Sexo", ["Hombres","Mujeres"], 
                                selection_mode="single",key="Sexo",default="Hombres")
  with a3:                              
    G_Edad_sel = st.selectbox("Grupo de edad", 
                             ["Primera infancia","Infancia","Adolescencia",
                             "Adultez temprana","Adultez media","Adulto mayor"], 
                              key="G_Edad",index=2)
  st.write("")
  
  filtros = {
    'departamento': Dpto_sel,
    'sexo': Sexo_sel,
    'Edad_Cat': G_Edad_sel
    }
  
  # Aplicar filtro iterando y acumulando condiciones
  df_filtrado = df.copy()
  for col, val in filtros.items():
    # Filtrar solo las filas que tengan el valor seleccionado en la columna categorizada
    if val is not None:
      df_filtrado = df_filtrado[df_filtrado[col] == val]
  
  categorias_toggles = {
      "Consumo de Sustancias Psicoactivas":1,
      "Trastornos esquizotipicos y delirantes":2,
      "Retraso Mental":3,
      "Síndromes de comportamiento por alteraciones fisiológicas y fact. físicos":4,
      "Trastornos del estado del animo":5,
      "Trastornos del desarrollo psicológico":6,
      "Trastornos neuróticos, estrés y somatomorfos":7,
      "Trastornos hab. niñez y adolescencia":8,
      "Trastornos mentales orgánicos y sintomáticos":9,
      "Trastornos de personalidad y comportamiento en adultos":10
  }
  b1,b2=st.columns([2,11.5])
  
  with b2:
    toggles_valores = []  # para guardar categorías seleccionadas
    for categoria, codigo in categorias_toggles.items():
        # Mostrar un checkbox usando el nombre de la categoría como label
        estado = st.toggle(label=categoria, key=f"Grupo_{codigo}")
        if estado:
            toggles_valores.append(codigo)  # agregamos el identificador
  
    # Filtramos el DataFrame según los valores de grupo seleccionados
    if toggles_valores:
        df_filtrado = df_filtrado[df_filtrado['cod_grupo'].isin(toggles_valores)]
    else:
        # Si ningún checkbox activo, mostramos todo (sin filtro)
        df_filtrado = df_filtrado.copy()
        
with b:
    
  Prom_Score=round(100*df_filtrado['Prob_RandomForest'].mean(),1)
  
  add_vertical_space(5)
  fig2=osm.plot_gauge(Prom_Score, '#2A3180', "%", "PROBABILIDAD", 100)
  st.plotly_chart(fig2, use_container_width=True)


# enfermedades = ["Consum.Sust.Psicoact.","Esquizofrenia","Retr. Mental",
# "Síndr. Alterac. Fisiológ.Fact.Físicos",
# "Trast. Afect Estad.Animo",
# "Trast. Desarrollo Psico.",
# "Trast. Neurót. Estrés y Somatom.",
# "Trast.Habit. Niñez-Adolesc",
# "Trast.Ment.Orgán. Sintomát.",
# "Trast.Person.Comp.Adultos"]
# 
# # Crear toggles y guardar seleccionados
# seleccionados = []
# for enf in enfermedades:
#     if st.toggle(enf, key=f"toggle_{enf}"):
#         seleccionados.append(enf)
# 
# # Filtrar DataFrame según toggles activos
# if seleccionados:
#     df_filtrado = df_filtrado[df_filtrado['Enfermedad_Evento'].isin(seleccionados)]
# else:
#     # Si no hay toggle activo, mostrar todo (o vaciar df_filtrado según preferencia)
#     # df_filtrado = df_filtrado.copy()  # no filtra nada
#     pass
