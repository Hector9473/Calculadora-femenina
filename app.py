import datetimeimport datetime
import pandas as pd
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Calendario de Ciclo y Rendimiento Deportivo",
    page_icon="🩸",
    layout="wide"
)

# --- PALETA DE COLORES AVANZADA Y ESTILOS UI ---
st.markdown("""
    <style>
    /* Estilos generales del contenedor principal */
    .reportview-container {
        background-color: #FAFAFB;
    }
    
    /* Alertas del Estado Actual */
    .alert-green { background-color: #E8F5E9; color: #1B5E20; padding: 14px; border-radius: 10px; font-weight: bold; border-left: 5px solid #4CAF50; margin-bottom: 15px; }
    .alert-yellow { background-color: #FFFDE7; color: #F57F17; padding: 14px; border-radius: 10px; font-weight: bold; border-left: 5px solid #FBC02D; margin-bottom: 15px; }
    .alert-red { background-color: #FFEBEE; color: #B71C1C; padding: 14px; border-radius: 10px; font-weight: bold; border-left: 5px solid #EF5350; margin-bottom: 15px; }
    
    /* Estilos para la cuadrícula del calendario (Modern Cards) */
    .dia-box {
        padding: 14px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 12px;
        min-height: 110px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
        transition: transform 0.2s;
        color: #2C3E50;
    }
    .dia-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    
    /* Clases específicas de la paleta mejorada */
    .box-menstruacion { background-color: #FFE0E0; border: 1px solid #FFA7A7; }
    .box-folicular { background-color: #E6F4EA; border: 1px solid #A8DABC; }
    .box-ovulacion { background-color: #FFF9C4; border: 1px solid #FFF176; }
    .box-lutea { background-color: #EDE7F6; border: 1px solid #D1C4E9; }
    
    /* Tipografías dentro de las tarjetas */
    .dia-numero { font-size: 1.3rem; font-weight: 800; color: #1A252C; margin-bottom: 2px; }
    .dia-fecha { font-size: 0.8rem; font-weight: 600; opacity: 0.7; text-transform: uppercase; margin-bottom: 6px; }
    .dia-fase { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
    
    /* Texto de Leyendas */
    .leyenda-item {
        padding: 8px; 
        border-radius: 8px; 
        text-align: center; 
        font-size: 0.85rem; 
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩸 Monitor de Ciclo Menstrual y Entrenamiento")
st.subheader("Optimiza tus pesas, running y ciclismo según tu biología")

# --- BARRA LATERAL: INPUTS DEL USUARIO ---
st.sidebar.header("⚙️ Configuración del Ciclo")

fecha_inicio = st.sidebar.date_input("Fecha de inicio del último ciclo:", datetime.date.today())
duracion_ciclo = st.sidebar.slider("Duración promedio del ciclo (días):", min_value=21, max_value=35, value=28)

fecha_fin_sangrado = st.sidebar.date_input("Fecha de finalización del sangrado:", fecha_inicio + datetime.timedelta(days=5))
duracion_sangrado = (fecha_fin_sangrado - fecha_inicio).days

# --- LÓGICA DE PROCESAMIENTO ---
fecha_actual = datetime.date.today()
dias_desde_inicio = (fecha_actual - fecha_inicio).days
dia_actual_ciclo = (dias_desde_inicio % duracion_ciclo) + 1

def obtener_datos_fase(dia):
    if dia <= duracion_sangrado:
        return {
            "fase": "Menstruación",
            "sintomas": "Cólicos, fatiga, sensibilidad mamaria, dolor lumbar, niveles bajos de energía.",
            "ejercicio": "Yoga suave, movilidad articular, estiramientos y caminata regenerativa.",
            "pesas": "Descarga. Cargas muy ligeras o peso corporal. Evitar valsalva/altas presiones.",
            "running": "Caminatas a paso ligero o trotes muy suaves en Zona 1.",
            "ciclismo": "Rodar suave en plano, cadencia alta y baja resistencia en rodillo o estática.",
            "alerta": "🟢 Días de fertilidad muy baja.",
            "clase_alerta": "alert-green",
            "clase_box": "box-menstruacion"
        }
    elif dia > duracion_sangrado and dia <= 11:
        return {
            "fase": "Fase Folicular",
            "sintomas": "Aumento progresivo de energía, mejor estado de ánimo, mayor claridad mental.",
            "ejercicio": "Entrenamientos de fuerza tradicionales, entrenamientos basados en potencia.",
            "pesas": "Hipertrofia y fuerza. Excelente momento para subir cargas de manera progresiva.",
            "running": "Entrenamientos de ritmo (tempo), rodajes de distancia a intensidad moderada.",
            "ciclismo": "Rodajes largos de resistencia (Zona 2 y 3) y entrenamientos de umbral.",
            "alerta": "🟡 Ventana fértil abriéndose. Probabilidad de embarazo moderada.",
            "clase_alerta": "alert-yellow",
            "clase_box": "box-folicular"
        }
    elif dia >= 12 and dia <= 16:
        return {
            "fase": "Ovulación",
            "sintomas": "Pico máximo de energía, mayor confianza, aumento de la temperatura basal.",
            "ejercicio": "Alta intensidad (HIIT), circuitos pliométricos y esfuerzos máximos.",
            "pesas": "Fuerza máxima (Récords Personales / PRs). El cuerpo tolera el máximo estrés mecánico.",
            "running": "Series cortas de velocidad, intervalos de alta intensidad (VO2 máx).",
            "ciclismo": "Sprints, entrenamientos de intervalos de alta intensidad (HIIT) o subidas explosivas.",
            "alerta": "❌ ALERTA: Máxima fertilidad. Riesgo muy alto de embarazo si buscas evitarlo.",
            "clase_alerta": "alert-red",
            "clase_box": "box-ovulacion"
        }
    else:
        return {
            "fase": "Fase Lútea",
            "sintomas": "Retención de líquidos, antojos, susceptibilidad al estrés, posible Síndrome Premenstrual (SPM).",
            "ejercicio": "Pilates, entrenamientos de estabilidad, cardio de baja a moderada intensidad.",
            "pesas": "Mantener cargas moderadas. Priorizar técnica y conexión mente-músculo sobre el peso.",
            "running": "Rodajes puramente aeróbicos y regenerativos. Menos volumen kilométrico.",
            "ciclismo": "Ciclismo aeróbico estable, evitar entrenamientos extenuantes de alta intensidad.",
            "alerta": "🟢 Fase infértil avanzada. Probabilidad de embarazo muy baja.",
            "clase_alerta": "alert-green",
            "clase_box": "box-lutea"
        }

datos_hoy = obtener_datos_fase(dia_actual_ciclo)

# --- PANEL PRINCIPAL (PESTAÑAS INTERACTIVAS) ---
tab1, tab2 = st.tabs(["📊 Estado Actual y Recomendaciones", "📅 Calendario Visual Cuadriculado"])

with tab1:
    st.header(f"Hoy estás en el Día {dia_actual_ciclo} del ciclo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🔄 Fase Actual: **{datos_hoy['fase']}**")
        st.markdown(f"<div class='{datos_hoy['clase_alerta']}'>{datos_hoy['alerta']}</div>", unsafe_allow_html=True)
        
        st.markdown("### 🤒 Posibles Síntomas de la Fase")
        st.info(datos_hoy['sintomas'])

    with col2:
        st.markdown("### 🏋️‍♀️ Guía de Entrenamiento Recomendado")
        st.markdown(f"**Funcional:** {datos_hoy['ejercicio']}")
        st.markdown(f"**Pesas:** {datos_hoy['pesas']}")
        st.markdown(f"**Running:** {datos_hoy['running']}")
        st.markdown(f"**Ciclismo:** {datos_hoy['ciclismo']}")

with tab2:
    st.header("📅 Vista de Calendario por Bloques")
    st.write("Cada cuadro representa un día de tu ciclo. Los colores te indican la fase metabólica y el nivel de fertilidad.")
    
    # Leyenda de colores interactiva y estilizada con CSS
    leyenda_cols = st.columns(4)
    with leyenda_cols[0]: st.markdown("<div class='leyenda-item' style='background-color:#FFE0E0; color:#B71C1C;'>🌸 Menstruación</div>", unsafe_allow_html=True)
    with leyenda_cols[1]: st.markdown("<div class='leyenda-item' style='background-color:#E6F4EA; color:#1B5E20;'>🌱 Fase Folicular</div>", unsafe_allow_html=True)
    with leyenda_cols[2]: st.markdown("<div class='leyenda-item' style='background-color:#FFF9C4; color:#F57F17;'>🔥 Ovulación</div>", unsafe_allow_html=True)
    with leyenda_cols[3]: st.markdown("<div class='leyenda-item' style='background-color:#EDE7F6; color:#4A148C;'>🧘‍♀️ Fase Lútea</div>", unsafe_allow_html=True)
    
    st.write("")
    
    # Crear la cuadrícula adaptada de 7 columnas
    columnas_calendario = st.columns(7)
    
    for i in range(1, duracion_ciclo + 1):
        indice_columna = (i - 1) % 7
        fecha_bucle = fecha_inicio + datetime.timedelta(days=i-1)
        datos_bucle = obtener_datos_fase(i)
        
        # Inyección HTML del cuadro con los nuevos colores de borde y fondo
        html_cuadro = f"""
        <div class="dia-box {datos_bucle['clase_box']}">
            <div class="dia-numero">{i}</div>
            <div class="dia-fecha">{fecha_bucle.strftime('%d %b')}</div>
            <div class="dia-fase" style="color: inherit;">{datos_bucle['fase']}</div>
        </div>
        """
        
        with columnas_calendario[indice_columna]:
            st.markdown(html_cuadro, unsafe_allow_html=True)
            with st.expander("🔍 Deporte"):
                st.caption(f"**Funcional:** {datos_bucle['ejercicio']}")
                st.caption(f"**Pesas:** {datos_bucle['pesas']}")
                st.caption(f"**Running:** {datos_bucle['running']}")
                st.caption(f"**Ciclismo:** {datos_bucle['ciclismo']}")

    st.write("")
    st.caption("Nota: Los cálculos de fertilidad son estimaciones algorítmicas basadas en el método del ritmo estándar y no sustituyen métodos anticonceptivos ni asesoría médica profesional.")

import pandas as pd
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Calendario de Ciclo y Rendimiento Deportivo",
    page_icon="🩸",
    layout="wide"
)

# --- PALETA DE COLORES AVANZADA Y ESTILOS UI ---
st.markdown("""
    <style>
    .reportview-container {
        background-color: #FAFAFB;
    }
    
    /* Alertas del Estado Actual */
    .alert-green { background-color: #E8F5E9; color: #1B5E20; padding: 14px; border-radius: 10px; font-weight: bold; border-left: 5px solid #4CAF50; margin-bottom: 15px; }
    .alert-yellow { background-color: #FFFDE7; color: #F57F17; padding: 14px; border-radius: 10px; font-weight: bold; border-left: 5px solid #FBC02D; margin-bottom: 15px; }
    .alert-red { background-color: #FFEBEE; color: #B71C1C; padding: 14px; border-radius: 10px; font-weight: bold; border-left: 5px solid #EF5350; margin-bottom: 15px; }
    
    /* Estilos para la cuadrícula del calendario (Modern Cards) */
    .dia-box {
        padding: 14px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 12px;
        min-height: 110px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
        transition: transform 0.2s;
    }
    .dia-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    
    /* Clases específicas de la paleta mejorada (Fondos y Bordes) */
    .box-menstruacion { background-color: #FFE0E0; border: 1px solid #FFA7A7; }
    .box-folicular { background-color: #E6F4EA; border: 1px solid #A8DABC; }
    .box-ovulacion { background-color: #FFF9C4; border: 1px solid #FFF176; }
    .box-lutea { background-color: #EDE7F6; border: 1px solid #D1C4E9; }
    
    /* Clases para el color del texto según la fase */
    .txt-menstruacion { color: #B71C1C; }
    .txt-folicular { color: #1B5E20; }
    .txt-ovulacion { color: #F57F17; }
    .txt-lutea { color: #4A148C; }
    
    /* Tipografías dentro de las tarjetas */
    .dia-numero { font-size: 1.3rem; font-weight: 800; color: #1A252C; margin-bottom: 2px; }
    .dia-fecha { font-size: 0.8rem; font-weight: 600; opacity: 0.7; text-transform: uppercase; margin-bottom: 6px; color: #2C3E50; }
    .dia-fase { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
    
    /* Texto de Leyendas */
    .leyenda-item {
        padding: 8px; 
        border-radius: 8px; 
        text-align: center; 
        font-size: 0.85rem; 
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📅 Calendario de Ciclo Menstrual y Entrenamiento")
st.subheader("Optimiza tus pesas, running, ciclismo y nutrición según tu biología")

# --- BARRA LATERAL: INPUTS DEL USUARIO ---
st.sidebar.header("⚙️ Configuración del Ciclo")

fecha_inicio = st.sidebar.date_input("Fecha de inicio del último ciclo:", datetime.date.today())
duracion_ciclo = st.sidebar.slider("Duración promedio del ciclo (días):", min_value=21, max_value=35, value=28)

fecha_fin_sangrado = st.sidebar.date_input("Fecha de finalización del sangrado:", fecha_inicio + datetime.timedelta(days=5))
duracion_sangrado = (fecha_fin_sangrado - fecha_inicio).days

# --- LÓGICA DE PROCESAMIENTO ---
fecha_actual = datetime.date.today()
dias_desde_inicio = (fecha_actual - fecha_inicio).days
dia_actual_ciclo = (dias_desde_inicio % duracion_ciclo) + 1

def obtener_datos_fase(dia):
    if dia <= duracion_sangrado:
        return {
            "fase": "Menstruación",
            "emoji": "🩸",
            "sintomas": "Cólicos, fatiga, sensibilidad mamaria, dolor lumbar, niveles bajos de energía.",
            "ejercicio": "Yoga suave, movilidad articular, estiramientos y caminata regenerativa.",
            "pesas": "Descarga. Cargas muy ligeras o peso corporal. Evitar pujar con el aire atrapado (hacer fuerza sosteniendo la respiración).",
            "running": "Caminatas a paso ligero o trotes muy suaves en Zona 1.",
            "ciclismo": "Rodar suave en plano, cadencia alta y baja resistencia en rodillo o estática.",
            "macros": "Priorizar hierro y alimentos antiinflamatorios. Carbohidratos complejos moderados, proteínas estables y grasas saludables (Omega 3).",
            "alerta": "🟢 Días de fertilidad muy baja.",
            "clase_alerta": "alert-green",
            "clase_box": "box-menstruacion",
            "clase_txt": "txt-menstruacion"
        }
    elif dia > duracion_sangrado and dia <= 11:
        return {
            "fase": "Fase Folicular",
            "emoji": "🌱",
            "sintomas": "Aumento progresivo de energía, mejor estado de ánimo, mayor claridad mental.",
            "ejercicio": "Entrenamientos de fuerza tradicionales, entrenamientos basados en potencia.",
            "pesas": "Hipertrofia y fuerza. Excelente momento para subir cargas de manera progresiva.",
            "running": "Entrenamientos de ritmo (tempo), rodajes de distancia a intensidad moderada.",
            "ciclismo": "Rodajes largos de resistencia (Zona 2 y 3) y entrenamientos de umbral.",
            "macros": "Alta sensibilidad a la insulina. Ideal para aumentar carbohidratos complejos (energía para entrenar pesado), proteínas altas para recuperación muscular y grasas bajas.",
            "alerta": "🟡 Ventana fértil abriéndose. Probabilidad de embarazo moderada.",
            "clase_alerta": "alert-yellow",
            "clase_box": "box-folicular",
            "clase_txt": "txt-folicular"
        }
    elif dia >= 12 and dia <= 16:
        return {
            "fase": "Ovulación",
            "emoji": "🔥",
            "sintomas": "Pico máximo de energía, mayor confianza, aumento de la temperatura basal.",
            "ejercicio": "Alta intensidad (HIIT), circuitos pliométricos y esfuerzos máximos.",
            "pesas": "Fuerza máxima (Récords Personales / PRs). El cuerpo tolera el máximo estrés mecánico.",
            "running": "Series cortas de velocidad, intervalos de alta intensidad (VO2 máx).",
            "ciclismo": "Sprints, entrenamientos de intervalos de alta intensidad (HIIT) o subidas explosivas.",
            "macros": "Gasto metabólico elevándose. Mantener carbohidratos altos antes del ejercicio, asegurar buen aporte de proteína para prevenir degradación y grasas moderadas.",
            "alerta": "❌ ALERTA: Máxima fertilidad. Riesgo muy alto de embarazo si buscas evitarlo.",
            "clase_alerta": "alert-red",
            "clase_box": "box-ovulacion",
            "clase_txt": "txt-ovulacion"
        }
    else:
        return {
            "fase": "Fase Lútea",
            "emoji": "🧘‍♀️",
            "sintomas": "Retención de líquidos, antojos, susceptibilidad al estrés, posible Síndrome Premenstrual (SPM).",
            "ejercicio": "Pilates, entrenamientos de estabilidad, cardio de baja a moderada intensidad.",
            "pesas": "Mantener cargas moderadas. Priorizar técnica y conexión mente-músculo sobre el peso.",
            "running": "Rodajes puramente aeróbicos y regenerativos. Menos volumen kilométrico.",
            "ciclismo": "Ciclismo aeróbico estable, evitar entrenamientos extenuantes de alta intensidad.",
            "macros": "Mayor uso de grasas como combustible. Aumentar grasas saludables (aguacate, frutos secos), mantener proteínas altas para saciedad y disminuir ligeramente carbohidratos.",
            "alerta": "🟢 Fase infértil avanzada. Probabilidad de embarazo muy baja.",
            "clase_alerta": "alert-green",
            "clase_box": "box-lutea",
            "clase_txt": "txt-lutea"
        }

datos_hoy = obtener_datos_fase(dia_actual_ciclo)

# --- PANEL PRINCIPAL (PESTAÑAS INTERACTIVAS) ---
tab1, tab2 = st.tabs(["📊 Estado Actual y Recomendaciones", "📅 Calendario Visual Cuadriculado"])

with tab1:
    st.header(f"Hoy estás en el Día {dia_actual_ciclo} del ciclo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🔄 Fase Actual: **{datos_hoy['emoji']} {datos_hoy['fase']}**")
        st.markdown(f"<div class='{datos_hoy['clase_alerta']}'>{datos_hoy['alerta']}</div>", unsafe_allow_html=True)
        
        st.markdown("### 🤒 Posibles Síntomas de la Fase")
        st.info(datos_hoy['sintomas'])
        
        st.markdown("### 🥑 Recomendación de Macronutrientes")
        st.success(datos_hoy['macros'])

    with col2:
        st.markdown("### 🏋️‍♀️ Guía de Entrenamiento Recomendado")
        st.markdown(f"**Funcional:** {datos_hoy['ejercicio']}")
        st.markdown(f"**Pesas:** {datos_hoy['pesas']}")
        st.markdown(f"**Running:** {datos_hoy['running']}")
        st.markdown(f"**Ciclismo:** {datos_hoy['ciclismo']}")

with tab2:
    st.header("📅 Vista de Calendario por Bloques")
    st.write("Cada cuadro representa un día de tu ciclo. Los colores e iconos te indican la fase metabólica y el nivel de fertilidad.")
    
    # Leyenda de colores interactiva y estilizada con CSS
    leyenda_cols = st.columns(4)
    with leyenda_cols: st.markdown("<div class='leyenda-item' style='background-color:#FFE0E0; color:#B71C1C;'>🩸 Menstruación</div>", unsafe_allow_html=True)
    with leyenda_cols: st.markdown("<div class='leyenda-item' style='background-color:#E6F4EA; color:#1B5E20;'>🌱 Fase Folicular</div>", unsafe_allow_html=True)
    with leyenda_cols: st.markdown("<div class='leyenda-item' style='background-color:#FFF9C4; color:#F57F17;'>🔥 Ovulación</div>", unsafe_allow_html=True)
    with leyenda_cols: st.markdown("<div class='leyenda-item' style='background-color:#EDE7F6; color:#4A148C;'>🧘‍♀️ Fase Lútea</div>", unsafe_allow_html=True)
    
    st.write("")
    
    # Crear la cuadrícula adaptada de 7 columnas
    columnas_calendario = st.columns(7)
    
    for i in range(1, duracion_ciclo + 1):
        indice_columna = (i - 1) % 7
        fecha_bucle = fecha_inicio + datetime.timedelta(days=i-1)
        datos_bucle = obtener_datos_fase(i)
        
# Inyección HTML del cuadro con emojis y clases de texto dinámicas por color de fasehtml_cuadro = f"""{i}{fecha_bucle.strftime('%d %b')}{datos_bucle['emoji']} {datos_bucle['fase']}"""with columnas_calendario[indice_columna]:st.markdown(html_cuadro, unsafe_allow_html=True)with st.expander("🔍 Detalles"):st.caption(f"Funcional: {datos_bucle['ejercicio']}")st.caption(f"Pesas: {datos_bucle['pesas']}")st.caption(f"Running: {datos_bucle['running']}")st.caption(f"Ciclismo: {datos_bucle['ciclismo']}")st.caption(f"Nutrición: {datos_bucle['macros']}")st.write("")st.caption("Nota: Los cálculos de fertilidad son estimaciones algorítmicas basadas en el método del ritmo estándar y no sustituyen métodos anticonceptivos ni asesoría médica profesional.")
