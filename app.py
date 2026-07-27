from datetime import date, datetime, timedelta
import calendar
import streamlit as st

# Configuración de la interfaz con enfoque estético y limpio
st.set_page_config(
    page_title="Flow Calendar | Sincronización Menstrual",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS avanzados para mejorar legibilidad, contraste y diseño tipo Google Calendar
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FAFAFB;
    }
    
    .main-title {
        color: #1A1C1E;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 5px;
    }
    
    .subtitle {
        color: #5C6066;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    
    /* Tarjeta de Estado Actual Mejorada */
    .status-card {
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 25px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    
    /* Bloques de Deporte */
    .sport-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        height: 100%;
    }
    
    /* Contenedores del Calendario */
    .calendar-header-day {
        text-align: center;
        font-weight: 600;
        color: #4A5568;
        padding: 10px 0;
        background-color: #EDF2F7;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    
    .calendar-cell {
        border-radius: 10px;
        padding: 10px;
        text-align: left;
        height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    
    .calendar-cell:hover {
        transform: translateY(-2px);
    }
    
    .day-number {
        font-size: 14px;
        font-weight: 600;
        color: #2D3748;
    }
    
    .phase-tag {
        font-size: 11px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 4px;
        text-align: center;
        margin-top: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Paleta de Colores de Alto Contraste y Accesibilidad Visual (Texto Oscuro sobre Fondos Pastel Claros)
PHASES_DATA = {
    "Menstrual": {"emoji": "🩸", "bg": "#FFF0F2", "text": "#C52233", "border": "#FFB3BC", "tag_bg": "#FFCCD2"},
    "Folicular": {"emoji": "🌱", "bg": "#EBFBEE", "text": "#1E7E34", "border": "#A3E6B3", "tag_bg": "#C2F0D0"},
    "Ovulación": {"emoji": "✨", "bg": "#FFF9E6", "text": "#B27B00", "border": "#FFE082", "tag_bg": "#FFEAA7"},
    "Lútea":     {"emoji": "🍂", "bg": "#F3E8FF", "text": "#6B21A8", "border": "#D8B4FE", "tag_bg": "#E9D5FF"}
}

# --- BARRA LATERAL: ENTRADA DE DATOS OPTIMIZADA ---
st.sidebar.markdown("### ⚙️ Datos de tu Ciclo")
st.sidebar.markdown("Ingresa las fechas exactas de tu **último ciclo terminado** para calcular tus métricas reales.")

# Inputs precisos de inicio y fin de ciclo anterior
last_start = st.sidebar.date_input("📆 Inicio del último ciclo", value=date.today() - timedelta(days=28))
last_end = st.sidebar.date_input("📆 Fin de ese mismo ciclo", value=date.today() - timedelta(days=1))

# Cálculo dinámico de la duración del ciclo basándose en las entradas del usuario
if last_end > last_start:
    calculated_cycle_length = (last_end - last_start).days + 1
    st.sidebar.success(f"⏱️ Duración calculada: **{calculated_cycle_length} días**")
else:
    calculated_cycle_length = 28
    st.sidebar.warning("⚠️ La fecha de fin debe ser posterior al inicio. Usando 28 días por defecto.")

period_length = st.sidebar.slider("🩸 Duración del sangrado (días actuales)", 3, 7, 5)

# --- CÁLCULOS DEL ESTADO ACTUAL ---
today = date.today()
# Días transcurridos desde el inicio del último ciclo registrado
days_since_start = (today - last_start).days % calculated_cycle_length
current_cycle_day = days_since_start + 1

# Determinar fase actual, síntomas y rutinas deportivas
if current_cycle_day <= period_length:
    fase = "Menstrual"
    sintomas = "Cólicos leves, cansancio corporal, menor resistencia cardiovascular."
    funcional = "Enfócate en movilidad articular profunda, estiramientos de espalda baja y Yoga Nidra."
    ciclismo = "Rodaje regenerativo en zonas de potencia bajas (Zona 1), cadencia libre en plano."
    running = "Sustituye por caminata a ritmo ágil o trote de muy baja intensidad. Escucha tus pulsaciones."
elif current_cycle_day <= 13:
    fase = "Folicular"
    sintomas = "Aumento notable de energía, mejor recuperación muscular, enfoque mental agudo."
    funcional = "Entrenamientos de fuerza pesada, levantamientos olímpicos complejos e hipertrofia."
    ciclismo = "Sesiones de intervalos (VO2 Máx), series en subida y acumulación de vatios altos."
    running = "Series de velocidad en pista, cambios de ritmo (fartlek) y entrenamientos de potencia."
elif current_cycle_day <= 16:
    fase = "Ovulación"
    sintomas = "Pico de energía máximo, fuerza muscular óptima, alta tolerancia al esfuerzo."
    funcional = "Circuitos funcionales de alta intensidad (HIIT), Crossfit y cargas máximas (1RM)."
    ciclismo = "Fondos exigentes de larga distancia, ritmo de competencia o contrarreloj."
    running = "Carreras de tempo (ritmo umbral) o tiradas largas buscando mejores tiempos personales."
else:
    fase = "Lútea"
    sintomas = "Retención hídrica, fatiga progresiva, propensión al estrés o inflamación (SME)."
    funcional = "Rutinas estables con peso corporal, Pilates avanzado y fortalecimiento de Core estable."
    ciclismo = "Rutas puramente aeróbicas y continuas (Zona 2). Evita picos bruscos de fatiga."
    running = "Trote base controlado por sensaciones. Trail running en entornos naturales y tranquilos."

cfg = PHASES_DATA[fase]

# --- VISTA PRINCIPAL ---
st.markdown('<h1 class="main-title">🌸 Flow Calendar</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Monitoreo menstrual de alto contraste y planificación deportiva inteligente.</p>', unsafe_allow_html=True)

# Tarjeta Resumen Actual con Alta Legibilidad
st.markdown(f"""
    <div class="status-card" style="background-color: {cfg['bg']}; border-left: 6px solid {cfg['text']}; border-color: {cfg['border']};">
        <h2 style="color: {cfg['text']}; margin: 0 0 10px 0; font-size: 1.5rem;">
            {cfg['emoji']} Hoy estás en la <b>Fase {fase}</b> (Día {current_cycle_day} del ciclo)
        </h2>
        <p style="color: #2D3748; margin: 0; font-size: 1.05rem;">
            <b>Síntomas y estado:</b> {sintomas}
        </p>
    </div>
""", unsafe_allow_html=True)

# Sección de Deporte estructurada en columnas legibles
st.markdown("### 🎯 Sincronización de Entrenamiento de Rendimiento")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="sport-card">
        <h4 style="color: #4A5568; margin-top:0;">🧘‍♀️ Entrenamiento Funcional</h4>
        <p style="color: #4A5568; font-size: 14px; line-height: 1.5;">{funcional}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="sport-card">
        <h4 style="color: #4A5568; margin-top:0;">🚴‍♀️ Ciclismo</h4>
        <p style="color: #4A5568; font-size: 14px; line-height: 1.5;">{ciclismo}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="sport-card">
        <h4 style="color: #4A5568; margin-top:0;">🏃‍♀️ Running</h4>
        <p style="color: #4A5568; font-size: 14px; line-height: 1.5;">{running}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- CALENDARIO ESTILO GOOGLE CALENDAR MEJORADO ---
st.markdown("### 📅 Vista de Calendario Mensual")

now = datetime.now()
cal = calendar.monthcalendar(now.year, now.month)
month_name = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][now.month - 1]

st.markdown(f"#### {month_name} {now.year}")

# Cabeceras de los días de la semana estilizadas
weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
header_cols = st.columns(7)
for idx, day_name in enumerate(weekdays):
    header_cols[idx].markdown(f'<div class="calendar-header-day">{day_name}</div>', unsafe_allow_html=True)

# Renderizado de las celdas del mes estilo bloques
for week in cal:
    cols = st.columns(7)
    for idx, day in enumerate(week):
        with cols[idx]:
            if day == 0:
                # Días vacíos del mes anterior/siguiente
                st.markdown('<div style="height: 90px; background-color: #F7FAFC; border-radius: 10px; border: 1px dashed #E2E8F0;"></div>', unsafe_allow_html=True)
            else:
                # Calcular fase para cada día individual en base a los datos guardados
                cell_date = date(now.year, now.month, day)
                cell_diff = (cell_date - last_start).days % calculated_cycle_length + 1
                
                if cell_diff <= period_length:
                    c_fase = "Menstrual"
                elif cell_diff <= 13:
                    c_fase = "Folicular"
                elif cell_diff <= 16:
                    c_fase = "Ovulación"
                else:
                    c_fase = "Lútea"
                
                c_cfg = PHASES_DATA[c_fase]
                
                # Borde especial de color si la celda renderizada corresponde al día de hoy
                is_today_border = "border: 2.5px solid #2B6CB0; box-shadow: 0 4px 10px rgba(43,108,176,0.15);" if day == today.day else f"border: 1px solid {c_cfg['border']};"
                
                st.markdown(f"""{day}{c_cfg['emoji']}{c_fase}""", unsafe_allow_html=True)
