import datetime
import pandas as pd
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Calendario de Ciclo y Rendimiento Deportivo",
    page_icon="🩸",
    layout="wide"
)

# Estilos CSS avanzados para las tarjetas del calendario dinámico
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 10px;
    }
    .alert-green { background-color: #d4edda; color: #155724; padding: 12px; border-radius: 8px; font-weight: bold; margin-bottom: 15px; }
    .alert-yellow { background-color: #fff3cd; color: #856404; padding: 12px; border-radius: 8px; font-weight: bold; margin-bottom: 15px; }
    .alert-red { background-color: #f8d7da; color: #721c24; padding: 12px; border-radius: 8px; font-weight: bold; margin-bottom: 15px; }
    
    /* Estilos para los cuadros del calendario */
    .dia-box {
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 10px;
        min-height: 100px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
        color: #333333;
    }
    .box-menstruacion { background-color: #f8d7da; border: 2px solid #f5c6cb; }
    .box-folicular { background-color: #e2f0d9; border: 2px solid #c5e1a5; }
    .box-ovulacion { background-color: #fff3cd; border: 2px solid #ffeeba; }
    .box-lutea { background-color: #e8daef; border: 2px solid #d7bde2; }
    
    .dia-numero { font-size: 1.2rem; font-weight: bold; margin-bottom: 2px; }
    .dia-fecha { font-size: 0.75rem; opacity: 0.8; margin-bottom: 5px; }
    .dia-fase { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

st.title("🩸 Monitor de Ciclo Menstrual y Entrenamiento")
st.subheader("Optimiza tus pesas, running y ciclismo según tu biología")

# --- BARRA LATERAL: INPUTS DEL USUARIO ---
st.sidebar.header("⚙️ Configuración del Ciclo")

# Inputs de fecha requeridos
fecha_inicio = st.sidebar.date_input("Fecha de inicio del último ciclo:", datetime.date.today())
duracion_ciclo = st.sidebar.slider("Duración promedio del ciclo (días):", min_value=21, max_value=35, value=28)

# Simulación de fecha de finalización (para estimar duración del sangrado)
fecha_fin_sangrado = st.sidebar.date_input("Fecha de finalización del sangrado (estimada o real):", fecha_inicio + datetime.timedelta(days=5))
duracion_sangrado = (fecha_fin_sangrado - fecha_inicio).days

# --- LÓGICA DE PROCESAMIENTO ---
fecha_actual = datetime.date.today()
dias_desde_inicio = (fecha_actual - fecha_inicio).days
dia_actual_ciclo = (dias_desde_inicio % duracion_ciclo) + 1

# Determinar datos según el día del ciclo
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
    st.write("Cada cuadro representa un día de tu ciclo. Los colores te indican la fase y nivel de riesgo/fertilidad.")
    
    # Leyenda de colores explicativa
    leyenda_cols = st.columns(4)
    leyenda_cols[0].markdown("<div style='background-color:#f8d7da; padding:5px; border-radius:5px; text-align:center; font-size:0.85rem; font-weight:bold;'>🟥 Menstruación (Infértil)</div>", unsafe_allow_html=True)
    leyenda_cols[1].markdown("<div style='background-color:#e2f0d9; padding:5px; border-radius:5px; text-align:center; font-size:0.85rem; font-weight:bold;'>🟩 Folicular (Fértil Moderado)</div>", unsafe_allow_html=True)
    leyenda_cols[2].markdown("<div style='background-color:#fff3cd; padding:5px; border-radius:5px; text-align:center; font-size:0.85rem; font-weight:bold;'>🟨 Ovulación (Máxima Fertilidad)</div>", unsafe_allow_html=True)
    leyenda_cols[3].markdown("<div style='background-color:#e8daef; padding:5px; border-radius:5px; text-align:center; font-size:0.85rem; font-weight:bold;'>🟪 Fase Lútea (Infértil)</div>", unsafe_allow_html=True)
    
    st.write("")
    
    # Crear la cuadrícula de 7 columnas (como una semana real)
    columnas_calendario = st.columns(7)
    
    for i in range(1, duracion_ciclo + 1):
        # Determinar en qué columna va el día actual (de 0 a 6)
        indice_columna = (i - 1) % 7
        
        fecha_bucle = fecha_inicio + datetime.timedelta(days=i-1)
        datos_bucle = obtener_datos_fase(i)
        
        # Formatear el cuadro en HTML para inyectar en Streamlit
        html_cuadro = f"""
        <div class="dia-box {datos_bucle['clase_box']}">
            <div class="dia-numero">Día {i}</div>
            <div class="dia-fecha">{fecha_bucle.strftime('%d %b')}</div>
            <div class="dia-fase">{datos_bucle['fase']}</div>
        </div>
        """
        
        # Dibujar el cuadro en la columna correspondiente
        with columnas_calendario[indice_columna]:
            st.markdown(html_cuadro, unsafe_allow_html=True)
            
            # Botón expandible debajo de cada cuadro para ver detalles rápidos de entrenamiento
            with st.expander("🔍 Deporte"):
                st.caption(f"**Ej. Funcional:** {datos_bucle['ejercicio']}")
                st.caption(f"**Pesas:** {datos_bucle['pesas']}")
                st.caption(f"**Running:** {datos_bucle['running']}")
                st.caption(f"**Ciclismo:** {datos_bucle['ciclismo']}")

    st.write("")
    st.caption("Nota: Los cálculos de fertilidad son estimaciones algorítmicas basadas en el método del ritmo estándar y no sustituyen métodos anticonceptivos ni asesoría médica profesional.")
