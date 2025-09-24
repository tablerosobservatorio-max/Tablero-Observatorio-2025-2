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
st.session_state['P_Colores']=P_Colores
#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Modelos Analíticos", layout="wide")
st.markdown("<h2 style='text-align: left;color: #39A8E0;'>MODELOS ANALÍTICOS</h2>", unsafe_allow_html=True)

#-------------------------------------------------------------------------------


st.markdown("""
<div style='font-size:20px; text-align: justify; line-height:1.4'>
En esta sección encontrará los resultados y detalles de los modelos
predictivos desarrollados para anticipar aspectos críticos relacionados con la 
salud mental y la convivencia ciudadana en los municipios de la región de la 
Orinoquía, Colombia.

Los modelos que se presentan hacen uso de técnicas avanzadas de machine learning 
para ofrecer predicciones útiles y accionables:

<ul>
  <li><b>Modelo de Prevalencia por Municipio</b>: Estima el número medio esperado de casos 
de enfermedades mentales o eventos de convivencia ciudadana para cada municipio, 
aportando información clave para la planificación estratégica y la asignación 
efectiva de recursos en salud pública y bienestar social.</li>

  <li><b>Modelo de Propensión Individual</b>: Evalúa la probabilidad de que un individuo 
  en particular experimente la enfermedad o evento de convivencia, basándose en 
  un conjunto integrado de variables que incluyen antecedentes de otras 
  morbilidades, mortalidades, y factores sociodemográficos. Este modelo permite 
  apoyar intervenciones más focalizadas y personalizadas.</li>
</ul>

Esta página está diseñada para que los usuarios puedan explorar estos modelos de 
manera interactiva, visualizando tanto los resultados agregados como los detalles 
técnicos que sustentan las predicciones. El objetivo es facilitar la comprensión, 
validación y aplicación práctica de estas herramientas, contribuyendo a mejorar 
la toma de decisiones en salud pública regional.

Le invitamos a navegar en los diferentes apartados para conocer en profundidad 
la metodología, resultados y posibles escenarios que estos modelos ofrecen, con 
el fin de fortalecer las estrategias de prevención, atención y promoción en 
salud mental y convivencia ciudadana.

### ***Metodología***

A partir de los datos previamente depurados, normalizados y estructurados, 
se conformaron los datasets que caracterizan a los individuos, municipios y 
departamentos de la región. Se establecieron las variables predictoras 
— tasas de morbilidad/mortalidad, categorías etarias, distribución por sexo, 
proyecciones poblacionales e indicadores de convivencia— junto con la 
variable objetivo para cada nivel de análisis. 

Posteriormente, se aplicaron procesos de selección y transformación de 
variables para mitigar sesgos y garantizar consistencia.

Con estos insumos se entrenaron diversos modelos de Machine Learning 
(Random Forest, XGBoost, Regresión Logística y Redes Neuronales, etc.), 
implementando validación cruzada y optimización de hiperparámetros. 

El desempeño se evaluó mediante métricas como exactitud, sensibilidad, 
especificidad y F1-Score, seleccionando los modelos más robustos. 
Finalmente, se integraron visualizaciones dinámicas que permiten analizar 
resultados tanto a nivel agregado como individual, asegurando interpretabilidad 
y aplicabilidad de los modelos en contextos de salud pública regional.

</div>
""", unsafe_allow_html=True)

