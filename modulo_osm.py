import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import math
from urllib.request import urlopen
import json
import numpy as np
import random
from st_aggrid import AgGrid, GridOptionsBuilder

#===============================================================================
#  LECTURA DE ARCHIVOS
#===============================================================================

# Tablas para Morbilidad
# ------------------------------------------------------------------------------
def bd_morbilidad(Tabla):
    df = pd.read_excel('data/Vistas_DB2.xlsx',sheet_name=Tabla)
    # Convertir año a numerico
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['grupo'] = df['grupo'].str.strip()  
    df['departamento']=df['departamento'].str.strip()
    df['departamento']=pd.Categorical(df['departamento'])
    df=df[df['componente']=='Conv. Social']
    #df=df.drop('componente',axis=1)
    return df
#-------------------------------------------------------------------------------
# Tablas para Mortalidad
# ------------------------------------------------------------------------------
def bd_mortalidad(Tabla):
    df = pd.read_excel('data/Vistas_DB2.xlsx',sheet_name=Tabla)
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['grupo'] = df['grupo'].str.strip()  
    df['departamento']=df['departamento'].str.strip()
    df['departamento']=pd.Categorical(df['departamento'])
    df=df[df['componente']=='Conv. Social']
    #df=df.drop('componente',axis=1)
    return df
#-------------------------------------------------------------------------------
# Tablas Población
# ------------------------------------------------------------------------------
def bd_poblacion(tabla,año):
    df = pd.read_excel('data/Vistas_DB2.xlsx',sheet_name=tabla)
    # Convertir año a numeric
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df=df[df['anio']<=año]
    df['departamento']=pd.Categorical(df['departamento'])
    
    return df
# ------------------------------------------------------------------------------
def bd_tasas_mbt():
    df = pd.read_excel('data/Tabla_Tasa_Grupo.xlsx')
    # Convertir año a numeric
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    
    return df
# ------------------------------------------------------------------------------
def bd_tasas_delitos():
    df = pd.read_excel('data/Tabla_Tasa_Delitos.xlsx')
    # Convertir año a numeric
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    
    return df
#-------------------------------------------------------------------------------
# Tablas Delitos Policia Nacional
# ------------------------------------------------------------------------------
def bd_ponal():
    df = pd.read_excel('data/Vistas_DB2.xlsx',sheet_name='Delitos')
    # Convertir año a categórica
    df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
    df['departamento']=pd.Categorical(df['departamento'])
    df=df[df['region']=='Orinoquía']
    return df
#-------------------------------------------------------------------------------
def Datos_Modelo_Personas():
  
  df = pd.read_excel('data/Tabla_Modelo_Personas.xlsx',sheet_name='Tab_PROBABILIDADES_PERSONAS')
  df2=df.copy()
  df2=df.groupby(['sexo', 'Edad_Cat', 'departamento', 'grupo',
  'Enfermedad_Evento', 'Detalle'])['Prob_RandomForest'].mean().reset_index()
  df2['Prob_RandomForest']=df2['Prob_RandomForest'].round(6)
  
  df2.to_excel("Tabla_MPersonas.xlsx",index=False)
  return(df2)
  
#===============================================================================
# TABLAS
#===============================================================================
def tabla_tasas(anio):
  
  df_mb = bd_morbilidad('Morbilidad2')
  df_mt = bd_mortalidad('Mortalidad2')
  df_pob = bd_poblacion('Pob2',anio)
  # Función para hacer la agregacion y preparacion de la taba fuente de conv. social
  
  # Filtrado y agregacion
  mb=df_mb[df_mb['region']=='Orinoquía'].groupby(['anio','departamento','grupo'])['Total'].sum().reset_index()
  mb.rename(columns={'Total': 'Casos_mb'}, inplace=True)
  mt=df_mt[df_mt['region']=='Orinoquía'].groupby(['anio','departamento','grupo'])['Total'].sum().reset_index()
  mt.rename(columns={'Total': 'Casos_mt'}, inplace=True)
  pob=df_pob[df_pob['region']=='Orinoquía'].groupby(['anio','departamento'])['Total'].sum().reset_index()
  pob.rename(columns={'Total': 'pob'}, inplace=True)
  tb_final=pd.merge(mb,mt, on=['anio','departamento','grupo'],how='inner')
  tb_final=pd.merge(tb_final,pob, on=['anio','departamento'],how='inner')
  
  tb_final['tasa_mb']=(tb_final['Casos_mb']/tb_final['pob']).round(2)
  tb_final['tasa_mt']=(tb_final['Casos_mt']/tb_final['pob']).round(2)
  
  tb_final.to_excel('Tabla_Tasa_Grupo.xlsx',index=False)
  
  return(tb_final)
#-------------------------------------------------------------------------------
def tabla_grupo(df, total_pob, index_col, values_col):
    
    # Validar que index_col y values_col existen en df
    if index_col not in df.columns:
        raise KeyError(f"Columna '{index_col}' no existe en el DataFrame.")
    if values_col not in df.columns:
        raise KeyError(f"Columna '{values_col}' no existe en el DataFrame.")
    
    # Crear pivot_table
    tabla = pd.pivot_table(
        df,
        values=values_col,
        index=index_col,
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    # Validar que values_col está en tabla
    if values_col not in tabla.columns:
        raise KeyError(f"Columna '{values_col}' no está presente tras pivot_table. Columnas: {tabla.columns.tolist()}")

    # Calcular total de casos
    total_casos = tabla[values_col].sum()
    if total_casos == 0:
        # Evitar división por cero
        raise ValueError("El total de casos es cero. No se puede calcular porcentajes ni tasas.")

    # Agregar columnas %(porcentaje) y Tasa
    tabla['(%)'] = (tabla[values_col] / total_casos * 100).round(2)
    if total_pob!=0:
      tabla['Tasa'] = (tabla[values_col] / total_pob).round(2)
    else:
      tabla['Tasa'] = 0

    # Renombrar para presentación
    col_rename = {
        index_col: 'Grupo',
        values_col: 'Número de Casos',
        'Tasa': 'Tasa x 100000 Hab.'
    }
    tabla = tabla.rename(columns=col_rename)
    
    # Aplicar estilo pandas
    tabla = tabla.style \
        .set_properties(
            subset=['Número de Casos', '(%)', 'Tasa x 100000 Hab.'],
            **{'text-align': 'center'}
        ) \
        .set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'center')]}
        ]) \
        .format({
            '(%)': '{:.2f}',
            'Tasa x 100000 Hab.': '{:.2f}',
            'Número de Casos': '{:,.0f}'
        })

    return tabla
#-------------------------------------------------------------------------------
def tabla_grupo_mbt(df):
  
  tabla=df[['grupo','Casos_mb','Casos_mt','tasa_mb','tasa_mt']].copy() 

  tabla['% Casos_mb']=(100*tabla['Casos_mb']/tabla['Casos_mb'].sum()).round(2)
  tabla['% Casos_mt']=(100*tabla['Casos_mt']/tabla['Casos_mt'].sum()).round(2)
  
  tabla = tabla.loc[:, ['grupo', 'Casos_mb','% Casos_mb','tasa_mb','Casos_mt',
       '% Casos_mt', 'tasa_mt']]
  
  # Renombrar para presentación
  col_rename = {
      'grupo':'Grupo',
      'Casos_mb':'Casos Morbilidad',
      '% Casos_mb':'(%)',
      'tasa_mb':'Tasa Morb.',
      'Casos_mt':'Casos Mortalidad',
      '% Casos_mt':'(%) ',
      'tasa_mt':'Tasa Mort.'
  }
  tabla = tabla.rename(columns=col_rename)

  # Construir opciones de la grilla con estilos para centrar columnas
  gb = GridOptionsBuilder.from_dataframe(tabla)
    
  for col in ['Casos Morbilidad', '(%)', 'Tasa Morb.',
                'Casos Mortalidad', '(%)', 'Tasa Mort.']:
        gb.configure_column(col, cellStyle={'textAlign': 'center'})
    
  grid_options = gb.build()

  return tabla, grid_options
#-------------------------------------------------------------------------------
def tabla_grupo_dlt(df):
  
  tabla=df[['desc_delito','Tasa_H','Tasa_M','Tasa_T']].copy()
  
  # Renombrar para presentación
  col_rename = {
      'desc_delito':'Descripción delito',
      'Tasa_H':'Tasa Hombres',
      'Tasa_M':'Tasa Mujeres',
      'Tasa_T':'Tasa Total'
  }
  tabla = tabla.rename(columns=col_rename)

  # Construir opciones de la grilla con estilos para centrar columnas
  gb = GridOptionsBuilder.from_dataframe(tabla)
    
  for col in ['Tasa Hombres', 'Tasa Mujeres', 'Tasa Total']:
        gb.configure_column(col, cellStyle={'textAlign': 'center'})
    
  grid_options = gb.build()

  return tabla, grid_options
#===============================================================================
# GRAFICAS
#===============================================================================
def diag_lineas(df,vx,vy,grupos,titulo,ylab,colores):
  
  df[vx]=pd.to_numeric(df[vx], errors='coerce')
  a_min=df[vx].min()-1
  a_max=df[vx].max()+1
  n=df[grupos].nunique()
  
  # Crear gráfico de líneas con Plotly Express
  fig = px.line(df,x=vx,y=vy,color=grupos,markers=True,
                title=titulo,
                color_discrete_sequence=colores)
  
  # Personalizar marcadores para que tengan borde del color de la línea y fondo blanco
  fig.update_traces(
      marker=dict(size=10,
                color='white',          # fondo blanco
                line=dict(width=2)      # borde que tomará el color de la línea
      )
  )
  
    # Ajustar eje x para mostrar todos los años y con rango fijo
  fig.update_xaxes(
      dtick=1,
      range=[a_min,a_max],
      tickmode='linear'
  )
  
  fig.update_xaxes(title_text="")
  fig.update_yaxes(title_text=ylab)
  
  return(fig)
#------------------------------------------------------------------------------
def diag_barras_apil(df,vx,vy,grupos,titulo,subt,colores,bmode='stack',xlab="",ylab=""):
  #width=800, height=600
  n=df[grupos].nunique()
  colores_sel=colores[:n]
  fig = px.bar(df,x=vx,y=vy,
              color=grupos,
              barmode=bmode,
              color_discrete_sequence=colores_sel,
              title=titulo,
              #text=vy,
              custom_data=[df[grupos]])
  fig.update_layout(xaxis_title=xlab,yaxis_title=ylab )
  
  return(fig) 
#-------------------------------------------------------------------------------
def diag_barras_apil_h(df,vx,vy,grupos,titulo,subt,colores,bmode='stack',xlab="",ylab="", width=800, height=600):
  
  n=df[grupos].nunique()
  colores_sel=colores[:n]
  fig = px.bar(df,x=vx,y=vy,
              color=grupos,
              barmode=bmode,
              color_discrete_sequence=colores_sel,
              title=titulo,
              orientation='h',
              text=vx,
              custom_data=[df[grupos]])
  fig.update_layout(
        xaxis_title=xlab,
        yaxis_title=ylab,
        width=width,
        height=height,
        margin={"r":0, "t":0, "l":0, "b":0}
    )
  
  return(fig) 
#-------------------------------------------------------------------------------
def diag_barras(df, vx, vy, titulo, subt, colores=None, xlab="", ylab="", width=800, height=600):
    fig = px.bar(
        df,
        x=vx,
        y=vy,
        color_discrete_sequence=colores,
        title=titulo,
        orientation='h'
        
    )
    fig.update_layout(
        xaxis_title=xlab,
        yaxis_title=ylab,
        width=width,
        height=height,
        margin={"r":0, "t":0, "l":0, "b":0},
        showlegend=False  # No mostrar leyenda porque no hay grupos
    )
    #fig.update_traces(textposition='auto')
    return fig

#fig.update_traces(textposition='outside')
  #for trace in fig.data:
  #      trace.text = trace.y if hasattr(trace, 'y') else None  # texto con el valor de la barra
  #      trace.textposition = 'inside'   # texto dentro de la barra (centro)
  #      trace.textfont = dict(color='white')  # texto blanco
#-------------------------------------------------------------------------------
# Funcion para la creacion del mapa coropletico por municipios
def mapa_crp(df,vy,ruta_geoj,Medida):
  
  # se lee el archivo simple con el listado de municipios de la region
  mpio_orinoquia=pd.read_csv("data/municipios.csv",sep=',')
  mpio_orinoquia['id_mpio']=mpio_orinoquia['id_mpio'].astype('Int64')
  
  # Lectura del archivo en formato GeoJson
  with open(ruta_geoj, 'r', encoding='utf-8') as f:
    mapa_gj2 = json.load(f)
  
  # Hacer merge con df2_f para incluir todos los municipios de mun_region
  df_completo = pd.merge(
    mpio_orinoquia,
    df[['id_mpio',vy]],
    on='id_mpio',
    how='left')
  
  # Rellenar NaN en Total con 0
  df_completo[vy] = df_completo[vy].fillna(0)
  
  escala_color = [
    [0, '#c6cbc8'],    # muy claro (blanco rosado)
    [0.5, '#1a6b3c'],  # color base medio
    [1, '#003f1b']]     # más oscuro
  
  
  fig = px.choropleth_mapbox(
    df_completo,
    geojson=mapa_gj2,
    locations='id_mpio',  # la columna del DataFrame que coincide con el identificador GeoJSON
    color=vy,       # la variable a colorear
    featureidkey="properties.mpio_cdpmp", # ajusta según tu geojson
    color_continuous_scale=escala_color,
    range_color=(0, max(df_completo[vy])),
    mapbox_style="carto-positron",
    zoom=5.5,
    center={"lat": 4.88, "lon": -71},
    opacity=0.5,
    labels={vy:Medida}
    )
  fig.update_layout(
    width=800,  # ancho en píxeles, ajusta a tu gusto
    height=500, # alto en píxeles
    margin={"r":0, "t":0, "l":0, "b":0}
    )
  
  fig.update_traces(
    hovertemplate=(
        "%{customdata[0]}<br>" +
        "%{customdata[1]} (%{location})<br>" +
        "Tasa Morbilidad: %{z}<extra></extra>"
    ),
    customdata=df_completo[['departamento', 'municipio']].values
  )
  return(fig)
#===============================================================================
def plot_metric(label, vy, prefix="", suffix="", show_graph=False, color_graph="",color_area="",yvisible=True):
    fig = go.Figure()

    if show_graph:
        
        fig.add_trace(
            go.Scatter(x=vy.index,y=vy,
                #random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_area,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=True, fixedrange=True)
    fig.update_yaxes(visible=yvisible, fixedrange=True)
    fig.update_layout(
        title=label,
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=120,
    )

    return(fig)
#-------------------------------------------------------------------------------
def plot_gauge(indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 46,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "black",
                'steps': [
                    {'range': [0, 30], 'color': '#ffde3b'},
                    {'range': [30, 70], 'color': '#F28F1C'},
                    {'range': [70, 100], 'color': '#f94144'}]
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        #paper_bgcolor="lightgrey",
        height=250,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    return(fig)
#-------------------------------------------------------------------------------  
def diag_donut(categorias, valores, titulo="", colores=None):
  fig = go.Figure(data=[go.Pie(labels=categorias, values=valores, hole=0.5, marker=dict(colors=colores))])
  fig.update_layout(
        title_text=titulo,
        legend=dict(
            orientation="h",   # Horizontal
            x=0.5,            # Posición horizontal central
            y=-0.1,           # Posición vertical debajo del gráfico
            xanchor='center', # Anclaje horizontal centrado
            yanchor='top'     # Anclaje vertical arriba
        )
      )
  return fig
#-------------------------------------------------------------------------------
def Diag_Dispersion(x,y,nombres):
  
    
  fig = go.Figure()
  
  # Puntos con etiquetas, texto arriba centrado, sin leyenda
  fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers+text',
        text=nombres,
        textposition='top center',
        marker=dict(color='blue'),
        showlegend=False
  ))
  
  maximo = 1.4*max(x.max(), y.max())
  rango = [0, maximo]
  
  # Recta identidad desde (0,0) hasta máximo
  fig.add_trace(go.Scatter(
        x=rango,
        y=rango,
        mode='lines',
        line=dict(color='red', dash='dash'),
        showlegend=False
  ))
  
  fig.update_layout(
        title='Morbilidad vs Mortalidad',
        xaxis=dict(
            title='Tasa de morbilidad',
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror='ticks',
            range=rango,       # rango X inicia en 0
            showgrid=True,
            gridcolor='gray',
            griddash='dot',
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2
        ),
        yaxis=dict(
            title='Tasa de mortalidad',
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror='ticks',
            range=rango,       # rango Y inicia en 0
            showgrid=True,
            gridcolor='gray',
            griddash='dot',
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2
            
        ),
        width=600,
        height=500,
        plot_bgcolor='white',
        margin=dict(l=50, r=50, t=50, b=50)
    )


  return fig
#-------------------------------------------------------------------------------
def G_Disp2(x,y,nombres):
    
    max_lim = 1.2*max(x.max(), y.max())
    
    plt.figure(figsize=(4,4))
    ax = sns.scatterplot(x=x, y=y, color='blue')
    
    # Graficar recta identidad
    ax.plot([0, max_lim], [0, max_lim], color='red', linestyle='--')
    
    # Añadir etiquetas a cada punto
    for i, label in enumerate(nombres):
        ax.text(x.iloc[i], y.iloc[i], label, fontsize=9, ha='center', va='bottom')

    # Ajustar límites e igualar relación aspecto
    ax.set_xlim(0, max_lim)
    ax.set_ylim(0, max_lim)
    ax.set_aspect('equal', adjustable='box')
    
    # Etiquetas de los ejes
    ax.set_xlabel("Tasa de morbilidad")
    ax.set_ylabel("Tasa de mortalidad")
    
    # Personalizar eje para estilo matemático
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    

    # Mostrar grid líneas gris punteadas
    ax.grid(True, linestyle=':', color='gray')
    
    plt.title("Morbilidad vs Mortalidad")
    plt.show()
#-------------------------------------------------------------------------------
def G_Disp3(x, y, nombres):
    max_lim = 1.1*max(x.max(), y.max())
    
    fig = go.Figure()
    
    # Puntos azules con etiquetas en top center
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers+text',
        text=nombres,
        textposition='top center',
        marker=dict(color='blue'),
        showlegend=False
    ))
    
    # Recta identidad roja discontinua
    fig.add_trace(go.Scatter(
        x=[0, max_lim],
        y=[0, max_lim],
        mode='lines',
        line=dict(color='red', dash='dash'),
        showlegend=False
    ))
    
    # Opciones de layout con grid dotted gris al 30% y sin borde externo
    fig.update_layout(
        title="Morbilidad vs Mortalidad",
        xaxis_title="Tasa de morbilidad",
        yaxis_title="Tasa de mortalidad",
        showlegend=False,
        width=500,
        height=500,
        plot_bgcolor='white',
        xaxis=dict(
            range=[0, max_lim],
            constrain='domain',
            showgrid=True,
            gridcolor='rgba(128,128,128,0.3)',  # gris 30% opacidad
            gridwidth=1,
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='rgba(128,128,128,0.3)',
            showline=False,  # sin borde externo
            mirror=False
        ),
        yaxis=dict(
            range=[0, max_lim],
            scaleanchor='x',
            scaleratio=1,
            showgrid=True,
            gridcolor='rgba(128,128,128,0.3)',
            gridwidth=1,
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='rgba(128,128,128,0.3)',
            showline=False,
            mirror=False
        )
    )
    
    return fig

