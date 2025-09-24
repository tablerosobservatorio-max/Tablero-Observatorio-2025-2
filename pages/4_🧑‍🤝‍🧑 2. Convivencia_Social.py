# Cargando las Librerías:
# ======================
import math
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
from st_aggrid import AgGrid, GridOptionsBuilder
#import importlib

import modulo_osm as osm
#importlib.reload(osm)
# ----------------------------------------------------------
# Definicion de colores
# 0."Azul_os", 1."Rojo", 2."Azul_cl", 3."Gris", 4."Verde", 5."Naranja", 6."Morado"
P_Colores = ["#2A3180","#E5352B","#39A8E0","#9D9D9C","#009640","#F28F1C","#662681"]
st.session_state['P_Colores']=P_Colores
#-------------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Convivencia Social", layout="wide")
st.markdown("<h2 style='text-align: center;color: #39A8E0;'>CONVIVENCIA SOCIAL</h2>", unsafe_allow_html=True)
#-------------------------------------------------------------------------------

st.markdown("""
        <h3 style='text-align: center; color: #39A8E0;'>Introducción </h3>
        <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="text-align: justify; font-size: 16px; color: #000000;">
        La convivencia ciudadana es la capacidad de los ciudadanos para vivir juntos en armonía, respetando normas comunes y resolviendo conflictos de manera pacífica, lo cual es esencial para garantizar entornos seguros y el bienestar social. Esta sección examina indicadores clave que reflejan la realidad social y de salud en la región de Orinoquía, permitiendo entender mejor los factores que afectan la calidad de vida y el tejido social. Al analizar diferentes dimensiones —morbilidad, mortalidad y delitos reportados— se facilita la toma de decisiones informadas para promover una convivencia más segura, inclusiva y saludable.
        </div>
    """, unsafe_allow_html=True)

st.write("")

#-------------------------------------------------------------------------------
# LECTURA Y PREPARACION DE FUENTES DE DATOS
#-------------------------------------------------------------------------------

#@st.cache_data  # Esta linea permite acceder al df desde la memoria cache
df_tasas = osm.bd_tasas_mbt()
df_dlt = osm.bd_tasas_delitos()
#-------------------------------------------------------------------------------
st.markdown("""
        <h4 style='text-align: left; color: #39A8E0;'>MORBILIDAD Y MORTALIDAD EN EVENTOS DE CONVIVENCIA SOCIAL </h4>""", unsafe_allow_html=True)

st.write("Esta sección presenta datos de eventos asociados a la convivencia social \
en terminos generales de acuerdo a los grupos de eventos tanto en morbilidad como en mortalidad. ")

#-------------------------------------------------------------------------------
# FILTROS EN LA PAGINA
#-------------------------------------------------------------------------------

#  Se escoge los años comunes entre las tres bases
anios=df_tasas['anio'].unique()

st.write("")
  
col1,col2 = st.columns([6,4])  # columnas con proporciones

with col1:
  # Se crea el control de años
  anio_sel = st.pills("Año", anios, selection_mode="single",default=max(anios))
  
  st.write("")
  # Se crea el control para departamentos
  depto_sel=st.pills("Departamento", df_tasas['departamento'].unique(),
                    selection_mode="single",default='Meta')
  st.write("")
  
  # Se filtra la tabla con la seleccion del usuario
  df_tasas_f=df_tasas[(df_tasas['anio']==anio_sel) & (df_tasas['departamento']==depto_sel)]
  
  # Se crea la tabla para streamlit
  tabla_tasas, grid_options = osm.tabla_grupo_mbt(df_tasas_f)
  
  num_filas = len(tabla_tasas)
  alto_fila = 35  # altura aproximada de una fila en píxeles
  alto_total = alto_fila * (num_filas + 1)
  AgGrid(tabla_tasas, gridOptions=grid_options, 
         height=alto_total, 
         fit_columns_on_grid_load=True)
  
with col2:
  # Se crea el diagrama de dispersion MOrbilidad vs. Mortalidad
  G_Disp=osm.G_Disp3(tabla_tasas['Tasa Morb.'],
              tabla_tasas['Tasa Mort.'],
              tabla_tasas['Grupo'])

  st.plotly_chart(G_Disp, use_container_width=False) 


#-------------------------------------------------------------------------------
# FILTROS PARA DELITOS REPORTADOS POR LA POLICIA NACIONAL
#-------------------------------------------------------------------------------

st.markdown("##")
 
st.markdown("""
        <h4 style='text-align: left; color: #39A8E0;'>DELITOS REPORTADOS POR LA POLICIA NACIONAL </h4>""", unsafe_allow_html=True)
st.write("")
anios_dlt=df_dlt['anio'].unique()
anio_dlt_sel = st.pills("Año", anios_dlt, selection_mode="single",
                          default=max(anios_dlt))

df_dlt2=df_dlt[(df_dlt['anio']==anio_dlt_sel) & (df_dlt['departamento']==depto_sel)]

# Se crea la tabla para streamlit
tabla_tasas_dlt, grid_options = osm.tabla_grupo_dlt(df_dlt2)

col1, col2=st.columns(2)

with col1:
  
  num_filas = len(tabla_tasas_dlt)
  alto_fila = 35  # altura aproximada de una fila en píxeles
  alto_total = alto_fila * (num_filas + 1)
  AgGrid(tabla_tasas_dlt, gridOptions=grid_options, 
         height=alto_total, 
         fit_columns_on_grid_load=True)

with col2:
  tabla_tasas_dlt2 = pd.melt(tabla_tasas_dlt, 
                                id_vars=['Descripción delito'], 
                             value_vars=['Tasa Hombres', 'Tasa Mujeres', 'Tasa Total'],
                               var_name='Sexo', value_name='Tasa')
                               
  tabla_tasas_dlt2=tabla_tasas_dlt2[tabla_tasas_dlt2['Sexo']!='Tasa Total']
  tabla_tasas_dlt2['Sexo']=tabla_tasas_dlt2['Sexo'].replace({'Tasa Hombres': 'Hombres',
                                                     'Tasa Mujeres': 'Mujeres'})
  
  Graf=osm.diag_barras_apil(tabla_tasas_dlt2,'Descripción delito','Tasa','Sexo',
                                          'Tasa de delitos por sexo','',
                                          P_Colores[4:],bmode='stack',
                                          xlab="",ylab="Tasa x 100.000 hab.")
  st.plotly_chart(Graf, use_container_width=True)
  #st.dataframe(tabla_tasas_dlt2)
#-------------------------------------------------------------------------------


