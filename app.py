import datetime
import pandas as pd
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Calendario de Ciclo y Rendimiento Deportivo",
    page_icon="🩸",
    layout="wide"
)

# Estilos CSS personalizados para mejorar el diseño de las alertas y tarjetas
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 10px;
    }
    .alert-green { background-color: #d4edda; color: #155724; padding: 12px; border-radius: 8px; font-weight: bold; }
    .alert-yellow { background-color: #fff3cd; color: #856404; padding: 12px; border-radius: 8px; font-weight: bold; }
    .alert-red { background-color: #f8d7da; color: #721c24; padding: 12px; border-radius: 8px; font-weight: bold; }
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
            "clase_alerta": "alert-green"
        }
    elif dia > duracion_sangrado and dia <= 11:
        return {
            "fase": "Fase Folicular (Post-menstruación)",
            "sintomas": "Aumento progresivo de energía, mejor estado de ánimo, mayor claridad mental.",
            "ejercicio": "Entrenamientos de fuerza tradicionales, entrenamientos basados en potencia.",
            "pesas": "Hipertrofia y fuerza. Excelente momento para subir cargas de manera progresiva.",
            "running": "Entrenamientos de ritmo (tempo), rodajes de distancia a intensidad moderada.",
            "ciclismo": "Rodajes largos de resistencia (Zona 2 y 3) y entrenamientos de umbral.",
            "alerta": "🟡 Ventana fértil abriéndose. Probabilidad de embarazo moderada.",
            "clase_alerta": "alert-yellow"
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
            "clase_alerta": "alert-red"
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
            "clase_alerta": "alert-green"
        }

datos_hoy = obtener_datos_fase(dia_actual_ciclo)

# --- PANEL PRINCIPAL (PESTAÑAS INTERACTIVAS) ---
tab1, tab2 = st.tabs(["📊 Estado Actual y Recomendaciones", "📅 Calendario Mensual"])

with tab1:
    st.header(f"Hoy estás en el Día {dia_actual_ciclo} del ciclo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🔄 Fase Actual: **{datos_hoy['fase']}**")
        st.markdown(f"<div class='{datos_hoy['clase_alerta']}'>{datos_hoy['alerta']}</div>", unsafe_allow_html=True)
        
        st.write("")
        st.markdown("### 🤒 Posibles Síntomas de la Fase")
        st.info(datos_hoy['sintomas'])

    with col2:
        st.markdown("### 🏋️‍♀️ Guía de Entrenamiento Recomendado")
        st.markdown(f"**Funcional:** {datos_hoy['ejercicio']}")
        st.markdown(f"**Pesas:** {datos_hoy['pesas']}")
        st.markdown(f"**Running:** {datos_hoy['running']}")
        st.markdown(f"**Ciclismo:** {datos_hoy['ciclismo']}")

with tab2:
    st.header("📅 Consulta de Calendario")
    st.write("Visualiza la proyección de tus fases y ventanas de fertilidad para los próximos 28-35 días:")
    
    # Generación de la tabla de datos tipo calendario
    lista_calendario = []
    for i in range(1, duracion_ciclo + 1):
        fecha_bucle = fecha_inicio + datetime.timedelta(days=i-1)
        datos_bucle = obtener_datos_fase(i)
        
        # Simplificación de alertas de fertilidad para la tabla
        if "Máxima fertilidad" in datos_bucle['alerta']:
            alerta_tabla = "🔴 Alta (Ovulación)"
        elif "Ventana fértil" in datos_bucle['alerta']:
            alerta_tabla = "🟡 Moderada"
        else:
            alerta_tabla = "🟢 Baja (Infértil)"
            
        lista_calendario.append({
            "Fecha": fecha_bucle.strftime("%d-%m-%Y"),
            "Día": i,
            "Fase": datos_bucle['fase'].split(" (")[0], # Nombre limpio
            "Fertilidad / Riesgo": alerta_tabla,
            "Recomendación General": datos_bucle['ejercicio']
        })
        
    df_calendario = pd.DataFrame(lista_calendario)
    
    # Mostrar el dataframe interactivo
    st.dataframe(
        df_calendario, 
        use_container_width=True, 
        hide_index=True,
    )
    
    st.caption("Nota: Los cálculos de fertilidad son estimaciones algorítmicas basadas en el método del ritmo estándar y no sustituyen métodos anticonceptivos ni asesoría médica profesional.")
