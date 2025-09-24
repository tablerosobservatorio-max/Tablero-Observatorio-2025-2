
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

# ------------------------------------------------------------------------------
# Simulación de Escenarios
# ------------------------------------------------------------------------------
#df = pd.read_excel('data/Tabla_ModeloCiudad.xlsx')
df = pd.read_excel('data/Tabla_MPersonas.xlsx')

st.write("")

st.write("""Este modelo de personas está diseñado para estimar la probabilidad de 
que una persona desarrolle un cuadro clínico grave relacionado con enfermedades mentales.
El modelo se calcula en función de algunas variables sociodemográficas y del historial 
médico-psiquiátrico que el usuario puede seleccionar. La utilidad principal de este modelo radica en su capacidad para proporcionar una 
evaluación personalizada del riesgo, apoyando la identificación temprana de 
individuos que podrían requerir atención prioritaria o intervenciones preventivas 
más intensivas.""")


st.sidebar.markdown("**Seleccione características generales del grupo de personas para el cual se desea simular el escenario**")

Dpto_sel = st.sidebar.pills("Departamento", 
                           ["Arauca","Casanare","Meta","Vichada"], 
                           selection_mode="single",
                            key="Dpto",default="Meta")

Sexo_sel = st.sidebar.pills("Sexo", ["Hombres","Mujeres"], 
                            selection_mode="single",key="Sexo",default="Hombres")

G_Edad_sel = st.sidebar.selectbox("Grupo de edad", 
                           ["Primera infancia","Infancia","Adolescencia",
                           "Adultez temprana","Adultez media","Adulto mayor"], 
                            key="G_Edad",index=2)


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
  "Consumo de sustancias psicoactivas":["Alcohol", "Alucinogenos", "Cannnabinoides", 
                                         "Cocaina", "Disolventes Volatiles", 
                                         "Multiples drogas y alucinogenos", 
                                         "Opiaceos", "Sedantes o hipnóticos", "Tabaco",
                                         "Otros estimulantes incluida la cafeina"],
  "Trastornos esquizotipicos y delirantes":["Esquizofrenia", "Psicosis no orgánica no especificada", 
                   "Trastorno esquizotípico","Trastornos delirantes persistentes", 
                   "Trastornos esquizoafectivos", 
                   "Trastornos psicóticos agudos y transitorios", 
                   "Otros trastornos psicóticos no orgánicos"],
  "Retraso mental":["Leve", "Moderado", "Muy fuerte","Profundo", "No especificado"],
 "Síndromes de comportamiento por alteraciones fisiológicas y fact. físicos": ["Abuso de sustancias no dependientes", 
                                             "Disfunción sexual, no causada por un trastorno orgánico o una enfermedad", 
                                             "Factores psicológicos y conductuales asociados a trastornos o enfermedades clasificados en otra parte", 
                                             "Síndromes conductuales no especificados asociados a alteraciones fisiológicas y factores físicos", 
                                             "Trastornos de la alimentación", 
                                             "Trastornos del sueño no orgánicos", 
                                             "Trastornos mentales y del comportamiento asociados al puerperio, no clasificados en otra parte"],
 "Trastornos del estado del animo":  ["Episodio depresivo", "Episodio maníaco", 
                               "Persistentes","Trastorno afectivo bipolar", 
                               "Trastorno depresivo recurrente","Otros trastornos"], 

"Trastornos del desarrollo psicológico.":["Trastorno específico del desarrollo de la función motora", 
                            "Trastorno no especificado del desarrollo psicológico", 
                            "Trastornos específicos del desarrollo de las habilidades escolares", 
                            "Trastornos específicos del desarrollo del habla y el lenguaje", 
                            "Trastornos generalizados del desarrollo", 
                            "Trastornos mixtos específicos del desarrollo",
                            "Otros trastornos del desarrollo psicológico"], 
                            
"Trastornos neuróticos, estrés y somatomorfos":["Reacción al estrés severo y trastornos de adaptación", 
                                    "Trastorno obsesivo-compulsivo", 
                                    "Trastornos de ansiedad fóbica", 
                                    "Trastornos disociativos", 
                                    "Trastornos somatomorfos",
                                    "Otros trastornos de ansiedad", 
                                    "Otros trastornos neuróticos"], 
"Trastornos hab. niñez y adolescencia":["Trastornos de conducta", "Trastornos de tics", 
                              "Trastornos del funcionamiento social con inicio específico en la infancia y la adolescencia", 
                              "Trastornos emocionales de inicio específico en la infancia", 
                              "Trastornos hipercinéticos", 
                              "Trastornos mixtos de la conducta y las emociones",
                              "Otros trastornos conductuales y emocionales"],
"Trastornos mentales orgánicos y sintomáticos":["Delirio no inducido por el alcohol y otras sustancias psicoactivas", 
                              "Demencia en la enfermedad de Alzheimer", 
                              "Demencia en otras enfermedades clasificadas en otra parte", 
                              "Demencia no especificada", 
                              "Demencia vascular", 
                              "Síndrome amnésico orgánico, no inducido por el alcohol y otros sustancias psicoactivas", 
                              "Trastorno mental orgánico o sintomático no especificado", 
                              "Trastornos de la personalidad y del comportamiento debidos a enfermedades cerebrales, daños y disfunción",
                              "Otro trastornos mentales debidos a daño y disfunción cerebral y a enfermedad física"], 

"Trastornos de personalidad y comportamiento en adultos":["Cambios de personalidad duraderos, no atribuibles a daño cerebral y enfermedad", 
                            "Trastorno no especificado de la personalidad y el comportamiento en la edad adulta", 
                            "Trastornos de hábitos e impulsos", 
                            "Trastornos de identidad de género", 
                            "Trastornos de la preferencia sexual", 
                            "Trastornos específicos de la personalidad", 
                            "Trastornos mixtos y otros trastornos de la personalidad", 
                            "Trastornos psicológicos y conductuales asociados con el desarrollo y la orientación sexual", 
                            "Otros trastornos de la personalidad y el comportamiento en la edad adulta"]
  }

toggles_valores = {}  # para guardar estados

col1, col2 = st.columns([5,5])

with col1:
  
  # Almacenar toggles activos
  enfermedades_seleccionadas = []
  
  for categoria, toggles in categorias_toggles.items():
      with st.expander(categoria):
          for i, tog in enumerate(toggles):
              estado = st.toggle(tog, key=f"{categoria}_{tog}_{i}")
              if estado:
                  enfermedades_seleccionadas.append(tog)
  
  # Ahora filtrar el DataFrame según los toggles activos
  if enfermedades_seleccionadas:
      df_filtrado = df_filtrado[df_filtrado['Enfermedad_Evento'].isin(enfermedades_seleccionadas)]
  else:
      # Si ningún toggle activo, mostrar todos (sin filtro)
      df_filtrado = df_filtrado.copy()
  
with col2:
  Prom_Score=round(100*df_filtrado['Prob_RandomForest'].mean(),1)
  
  st.write("")
  st.write("")
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
