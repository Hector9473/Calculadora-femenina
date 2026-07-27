from datetime import date, datetime, timedelta
import calendar
import streamlit as st

# Configuración de la página con estética limpia
st.set_page_config(
    page_title="Ciclo Vital | Calendario Menstrual",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS personalizados para simular la estética minimalista de Google Calendar
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .phase-card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .calendar-day {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        background-color: white;
        min-height: 80px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar para modificar fechas y parámetros
st.sidebar.markdown("## ⚙️ Configuración del Ciclo")
last_period = st.sidebar.date_input(
    "📅 Último inicio de periodo", value=date.today() - timedelta(days=14)
)
cycle_length = st.sidebar.slider(
    "Duración promedio del ciclo (días)", 21, 35, 28
)
period_length = st.sidebar.slider("Duración del sangrado (días)", 3, 7, 5)

# Cálculo de fases del ciclo actual
today = date.today()
days_since_start = (today - last_period).days % cycle_length
current_cycle_day = days_since_start + 1

# Definición de Fases, Emojis, Síntomas y Deporte
if current_cycle_day <= period_length:
    fase_nombre = "Fase Menstrual"
    emoji = "🩸"
    color = "#ffebee"
    sintomas = (
        "Fatiga, cólicos leves a moderados, sensibilidad, energía baja."
    )
    funcional = "Movilidad suave, yoga restaurativo, estiramientos y caminatas."
    ciclismo = "Suave y plano, sin exigencia de vatios altos ni sprints."
    running = (
        "Trote muy ligero o descanso activo; escucha a tu cuerpo sin forzar."
    )
elif current_cycle_day <= 13:
    fase_nombre = "Fase Folicular"
    emoji = "🌱"
    color = "#e8f5e9"
    sintomas = "Aumento paulatino de energía, claridad mental, optimismo."
    funcional = "Entrenamiento de fuerza progresivo, hipertrofia y potencia."
    ciclismo = (
        "Rutas moderadas a largas, excelente momento para acumular base."
    )
    running = "Carreras de distancia constante o intervalos moderados."
elif current_cycle_day <= 16:
    fase_nombre = "Fase de Ovulación"
    emoji = "✨"
    color = "#fff3e0"
    sintomas = (
        "Pico máximo de energía, mayor libido, sociabilidad y confianza."
    )
    funcional = (
        "HIIT, Crossfit, levantamiento de pesas pesado (máximo rendimiento)."
    )
    ciclismo = "Entrenamientos de alta intensidad, crono o escalada."
    running = "Series rápidas, velocidad y marcas personales."
else:
    fase_nombre = "Fase Lútea"
    emoji = "🍂"
    color = "#f3e5f5"
    sintomas = (
        "Posible cambios de humor, retención de líquidos, antojos (SME)."
    )
    funcional = "Pilates, fuerza con cargas moderadas, evitar sobreentrenar."
    ciclismo = "Rodajes aeróbicos estables, bajar la intensidad progresivamente."
    running = "Trotes suaves, trail running contemplativo o trote-caminata."

# Interfaz Principal
st.title("🌸 Ciclo Vital & Wellness Tracker")
st.markdown(
    "Monitorea tu ciclo menstrual, sincroniza tus entrenamientos y cuida tu bienestar con una vista clara."
)

# Tarjeta Resumen Actual
st.markdown(
    f"""
    <div class="phase-card" style="background-color: {color}; border-left: 6px solid #d81b60;">
        <h2>{emoji} Hoy estás en la {fase_nombre} (Día {current_cycle_day} del ciclo)</h2>
        <p><b>Síntomas comunes:</b> {sintomas}</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sección de Recomendación de Deportes
st.markdown("### 🎯 Sincronización de Entrenamiento")
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"🧘‍♀️ **Funcional**\n\n{funcional}")
with col2:
    st.success(f"🚴‍♀️ **Ciclismo**\n\n{ciclismo}")
with col3:
    st.warning(f"🏃‍♀️ **Running**\n\n{running}")

# Simulación de Calendario Tipo Google Calendar del Mes Actual
st.markdown("### 📅 Vista de Calendario Mensual")
now = datetime.now()
cal = calendar.monthcalendar(now.year, now.month)
month_name = calendar.month_name[now.month]

st.markdown(f"#### {month_name} {now.year}")

# Cabeceras de días de la semana
weekdays = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
header_cols = st.columns(7)
for idx, day_name in enumerate(weekdays):
    header_cols[idx].markdown(f"**{day_name}**")

# Renderizar semanas del mes
for week in cal:
    cols = st.columns(7)
    for idx, day in enumerate(week):
        with cols[idx]:
            if day == 0:
                st.markdown(
                    "<div style='color: #ccc; padding: 10px;'>-</div>",
                    unsafe_allow_html=True,
                )
            else:
                # Calcular fase aproximada para cada día del mes actual en pantalla
                d_date = date(now.year, now.month, day)
                d_diff = (d_date - last_period).days % cycle_length + 1

                # Asignar emoji según día del ciclo
                if d_diff <= period_length:
                    d_emoji = "🩸"
                elif d_diff <= 13:
                    d_emoji = "🌱"
                elif d_diff <= 16:
                    d_emoji = "✨"
                else:
                    d_emoji = "🍂"

                is_today = "border: 2px solid #ff4b4b;" if day == today.day else ""
                st.markdown(
                    f"""
                    <div style="border: 1px solid #e0e0e0; border-radius: 6px; padding: 5px; text-align: center; background: white; {is_today} height: 60px;">
                        <span style="font-size: 12px; font-weight: bold;">{day}</span><br>
                        <span style="font-size: 18px;">{d_emoji}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
