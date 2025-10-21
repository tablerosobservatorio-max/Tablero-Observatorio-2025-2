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
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import modulo_osm as osm
from streamlit_extras.add_vertical_space import add_vertical_space
from st_aggrid import AgGrid, GridOptionsBuilder
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
# LECTURA Y PREPARACION DE FUENTES DE DATOS
#-------------------------------------------------------------------------------

df_mb2 =osm.bd_morbilidad('Morbilidad2')

df_pob2 = osm.bd_poblacion('Pob2',2024)
df_pob2=df_pob2[df_pob2['region']=='Orinoquía'].reset_index(drop=True)

df_mb3 = osm.bd_morbilidad('Morbilidad3')

df_pob3 = osm.bd_poblacion('Pob3',2024)

#-------------------------------------------------------------------------------
# FILTROS
#-------------------------------------------------------------------------------

col1, col2 = st.columns([4,6])

with col1:
  # 1. Botones por departamento
  # Agregar opción "Todos" como primer elem
    opciones = ["Toda la región"] + list(df_pob2['departamento'].unique())
    
    # Selector que puede tener "Todos" para sin filtro
    depto_sel = st.pills("Departamento", opciones, selection_mode="single", default="Toda la región")
    
    df_pob2_f = df_pob2.copy()
    if depto_sel == "Toda la región":
        df_mb2_f = df_mb2.copy()  # Sin filtro, todo el dataframe
        df_pob2_f = df_pob2.copy()
    else:
        df_mb2_f = df_mb2[df_mb2["departamento"] == depto_sel]
        df_pob2_f = df_pob2[df_pob2['departamento'] == depto_sel]
  
    # 2. Crear un selector para que el usuario elija uno o varios grupos
    grupos = df_mb2_f['grupo'].unique().tolist()
    grupo_sel = st.selectbox("Selecciona un grupo de evento", grupos)
    df_mb2_f = df_mb2_f[df_mb2_f["grupo"] == grupo_sel]
  
with col2:
  #  2. Botones por año
  anios=sorted(df_mb3['anio'].unique()) 
  anio_sel = st.pills("Año", anios, selection_mode="single",default=max(anios))
    # 3. Crear un selector para el evento
  eventos = df_mb2_f['Enfermedad_Evento'].unique().tolist()
  eventos.insert(0, "Todos")
  evento_sel = st.selectbox("Seleccione el evento de interes", eventos)


Total_casos=df_mb2[(df_mb2['anio']==anio_sel) & (df_mb2['grupo']==grupo_sel)].groupby('departamento')['Total'].sum()
df_pob2['departamento']=df_pob2['departamento'].astype('object')

Total_Pob=df_pob2[df_pob2['anio']==anio_sel].groupby('departamento')['Total'].sum()
Tasas=(Total_casos/Total_Pob).round(1)


st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: #39A8E0;
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
#-------------------------------------------------------------------------------
#  TARJETAS DE TASAS POR DEPARTAMENTO
st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Tasas de morbilidad total por departamento</h4>", 
  unsafe_allow_html=True)
#----------------------------------------------------------------------------------------------------------------
st.write("")

a,b,c,d,e,f =st.columns([3,1.6,1.6,1.6,1.6,3])

with b:
  st.metric('Arauca',Tasas[0],border=True)
with c:
  st.metric('Casanare',Tasas[1],border=True)
with d:
  st.metric('Meta',Tasas[2],border=True)
with e:  
  st.metric('Vichada',Tasas[3],border=True)

st.write("")
#-------------------------------------------------------------------------------
# Contenido Morbilidad
#-------------------------------------------------------------------------------
st.write("")

# Total_casos=df_mb3[(df_mb3['grupo']==grupo_sel) & (df_mb3['anio']==anio_sel)]['Total'].sum()
# Total_Pob=df_pob3[df_pob3['anio']==anio_sel]['Total'].sum()
# Tasa_grupo_ORQ=(Total_casos/Total_Pob).round(1)


# 2. Filtrar el DataFrame según la selección del usuario

if evento_sel != "Todos":
  df_mb2_f = df_mb2_f[df_mb2_f["Enfermedad_Evento"] == evento_sel]

total_pob=df_pob2_f['Total'].sum()

df_mb2_ft=df_mb2_f.groupby(['anio','sexo'])['Total'].sum().reset_index()

Total_casos_depto=df_mb2_f[df_mb2_f['anio']==anio_sel]['Total'].sum()
Tasa_grupo_depto=(Total_casos_depto/total_pob).round(1)

# Tarjetas con indiadores relevantes
#-------------------------------------------------------------------------------

col1, col2 = st.columns(2)
with col1:
  st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Casos por edad</h4>", unsafe_allow_html=True)
  G_bar=osm.diag_barras_apil(df_mb2_f[df_mb2_f['anio']==anio_sel],'nombre_cat_edad','Total',
                                'sexo','','subtitulo',P_Colores[4:],xlab='Edad',ylab='No. de casos')
  st.plotly_chart(G_bar, use_container_width=True)
with col2:
  st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Tendencia por años</h4>", unsafe_allow_html=True)
  G_Lineas=osm.diag_lineas(df_mb2_ft,'anio','Total','sexo','','N. Casos',P_Colores[4:])
  st.plotly_chart(G_Lineas, use_container_width=True)
  
  
#-------------------------------------------------------------------------------
# Mapa coropletico de tasas de morbilidad
#-------------------------------------------------------------------------------

# Filtrado de la base y calculo de las tasas por municipio
if depto_sel == "Toda la región":
  df_mb3_f=df_mb3[(df_mb3['grupo']==grupo_sel) & (df_mb3['anio']==anio_sel)]
  df_pob3_f=df_pob3[df_pob3['anio']==anio_sel]
else:
  df_mb3_f=df_mb3[(df_mb3['departamento']==depto_sel) & (df_mb3['grupo']==grupo_sel) & (df_mb3['anio']==anio_sel)]
  df_pob3_f=df_pob3[(df_pob3['departamento']==depto_sel) & (df_pob3['anio']==anio_sel)]

df_mb3_f2=df_mb3_f.groupby(['id_mpio','municipio','sexo'])['Total'].sum().reset_index()
df_pob3_f.rename(columns={'Total':'pob10'},inplace=True)

df_mb3_f2=df_mb3_f2[['id_mpio','municipio','sexo','Total']].merge(df_pob3_f[['municipio','sexo','pob10']], on=['municipio','sexo'])
df_mb3_f2['Tasa_mb'] = (df_mb3_f2['Total'] / df_mb3_f2['pob10']).round(1)


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

# Mapa
col1, col2 = st.columns(2)
with col1:

  st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Morbilidad por municipio</h4>", unsafe_allow_html=True)
  Mp_cr=osm.mapa_crp(df_mb3_f2,'Tasa_mb','data/mapa_gj2.geojson','Tasa morbilidad')
  st.plotly_chart(Mp_cr, use_container_width=True)
with col2:
  st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Tasas de morbilidad por municipio y sexo</h4>", unsafe_allow_html=True)
  
  st.plotly_chart(G_bar2, use_container_width=True)

#----------------------------------------------------------------------------------------------------------------
add_vertical_space(3)

st.markdown("<h4 style='text-align: left;color: #39A8E0;'>Detalle del evento</h4>", unsafe_allow_html=True)
#----------------------------------------------------------------------------------------------------------------
st.write("")
# Datos diagrama de sectores dinamico
df_dc=pd.read_excel('data/Tabla_Subsectores_CS.xlsx',sheet_name='mb')
# Filtro del grupo de enfermedad o evento
df_dc_f=df_dc[df_dc['grupo']==grupo_sel]
# Filtro del año
df_dc_f=df_dc_f[(df_dc_f['Año']==0) | (df_dc_f['Año']==anio_sel)]

# Datos de la tabla
df_dll=pd.read_excel('data/Tabla_Tasa_Detalle.xlsx',sheet_name='mb')

if depto_sel == "Toda la región":
  Total_casos2=df_dll[
  (df_dll['anio']==anio_sel) & (df_dll['grupo']==grupo_sel)
  ].groupby(['Detalle'])[['Hombres','Mujeres','Total','PobH','PobM','Pob']].sum().reset_index()
else:
  Total_casos2=df_dll[
  (df_dll['anio']==anio_sel) & (df_dll['grupo']==grupo_sel) &(df_dll['departamento']==depto_sel)
  ].groupby('Detalle')[['Hombres','Mujeres','Total','PobH','PobM','Pob']].sum().reset_index()


Total_casos2['Tasa Hombres']=round(Total_casos2['Hombres']/Total_casos2['PobH'],2)
Total_casos2['Tasa Mujeres']=round(Total_casos2['Mujeres']/Total_casos2['PobM'],2)
Total_casos2['Tasa Total']=round(Total_casos2['Total']/Total_casos2['Pob'],2)
Tasas_finales=Total_casos2.drop(columns=['PobH','PobM','Pob']
).sort_values(by='Tasa Total', ascending=False)

gb = GridOptionsBuilder.from_dataframe(Tasas_finales)
gb.configure_pagination(enabled=True)
gb.configure_default_column(sortable=True, filter=True, resizable=True)
gb.configure_grid_options(domLayout='normal')

gridOptions = gb.build()

a,b=st.columns([4,6])

with a:
  Graf_dc=osm.diag_sectores_dinamico(df_dc_f,"")
  st.plotly_chart(Graf_dc, use_container_width=True) 
with b:
  st.write("")
  # Mostrar la tabla interactiva
  AgGrid(
    Tasas_finales,
    gridOptions=gridOptions,
    enable_enterprise_modules=False,
    update_mode='MODEL_CHANGED',
    height=500,
    fit_columns_on_grid_load=True
  )


