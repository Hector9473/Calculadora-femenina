import streamlit as st
from datetime import datetime, timedelta
import calendar

# Configuración de la página de Streamlit
st.set_page_config(page_title="Rendimiento y Ciclo Menstrual", page_icon="🩸", layout="centered")

# Diccionario dinámico con la información de cada fase
# Los días se calculan en proporción a la duración del ciclo elegido
def obtener_datos_fase(fase, duracion_ciclo):
    # Ajuste dinámico de días aproximados según la duración del ciclo
    if duracion_ciclo == 28:
        limites = {"Menstrual": (1, 5), "Folicular": (6, 13), "Ovulatoria": (14, 15), "Lútea": (16, 28)}
    elif duracion_ciclo == 30:
        limites = {"Menstrual": (1, 5), "Folicular": (6, 14), "Ovulatoria": (15, 16), "Lútea": (17, 30)}
    else: # 32 días
        limites = {"Menstrual": (1, 6), "Folicular": (7, 15), "Ovulatoria": (16, 17), "Lútea": (18, 32)}
        
    inicio, fin = limites[fase]
    
    detalles = {
        "Menstrual": {
            "hormonas": "Estrógenos y progesterona en niveles muy bajos.",
            "rendimiento": "Energía reducida, mayor sensación de fatiga, pero buena tolerancia al dolor inicial.",
            "sintomas": ["Cólicos abdominales", "Cansancio o flojera", "Dolor lumbar", "Retención de líquidos leve"],
            "recomendaciones": {
                "Funcional": "Movilidad articular, yoga suave, estiramientos y ejercicios de baja intensidad sin impacto.",
                "Gym": "Ejercicios con cargas livianas a moderadas, priorizando repeticiones altas si tienes energía, o descanso activo.",
                "Running": "Trote suave o caminata ligera. Evita entrenamientos de alta intensidad (HIIT) o fondos largos.",
                "Ciclismo": "Rodajes suaves y llanos en zona 1-2. Evita subidas exigentes o series de potencia."
            }
        },
        "Folicular": {
            "hormonas": "Los estrógenos empiezan a subir progresivamente.",
            "rendimiento": "Alto nivel de energía, optimismo, mayor fuerza, recuperación rápida y alta capacidad anaeróbica.",
            "sintomas": ["Aumento gradual de la vitalidad", "Mejor estado de ánimo", "Piel más clara"],
            "recomendaciones": {
                "Funcional": "Entrenamientos dinámicos, pliometría, circuitos de alta intensidad y fuerza funcional.",
                "Gym": "Momento ideal para buscar marcas personales (PR), levantar pesas pesadas e hipertrofia.",
                "Running": "Series de velocidad, intervalos (HIIT) y pasadas largas a ritmos alegres.",
                "Ciclismo": "Entrenamientos de potencia, intervalos cortos de alta intensidad y rodajes en montaña."
            }
        },
        "Ovulatoria": {
            "hormonas": "Pico máximo de estrógenos y pico de la hormona luteinizante (LH).",
            "rendimiento": "Fuerza máxima y máxima energía, aunque hay un pequeño riesgo de lesión de rodilla o ligamentos por laxitud.",
            "sintomas": ["Mayor libido", "Pinchazo leve en un lado del abdomen", "Flujo cervical elástico"],
            "recomendaciones": {
                "Funcional": "Ejercicios de estabilidad de core, control neuromuscular y fuerza explosiva con buena técnica.",
                "Gym": "Excelente para potencia máxima y levantamientos pesados, cuidando muy bien el calentamiento articular.",
                "Running": "Rendimiento óptimo para competir o buscar tiempos en distancias medias o largas.",
                "Ciclismo": "Salidas fuertes en grupo o crono, aprovechando el pico de máxima capacidad respiratoria y fuerza."
            }
        },
        "Lútea": {
            "hormonas": "Aumento de progesterona y caída posterior si no hay embarazo (fase premenstrual al final).",
            "rendimiento": "La temperatura corporal sube; la resistencia cardiovascular disminuye ligeramente al inicio y decae la energía al final.",
            "sintomas": ["Ansiedad o cambios de humor", "Sensibilidad en los senos", "Hinchazón o gases", "Fatiga premenstrual"],
            "recomendaciones": {
                "Funcional": "Pilates, entrenamientos de fuerza moderada controlando la respiración y bajando la exigencia.",
                "Gym": "Mantén pesos moderados, prioriza la técnica y evita llegar al fallo muscular absoluto en la última semana.",
                "Running": "Carrera continua a ritmo constante y cómodo (zona aeróbica). Evita sesiones agónicas de velocidad.",
                "Ciclismo": "Rodajes base estables de larga duración pero a baja intensidad, a ritmo conversacional."
            }
        }
    }
    
    resultado = detalles[fase]
    resultado["dias"] = (inicio, fin)
    return resultado

def determinar_fase(dia_ciclo, duracion_ciclo):
    fases = ["Menstrual", "Folicular", "Ovulatoria", "Lútea"]
    for f in fases:
        info = obtener_datos_fase(f, duracion_ciclo)
        inicio, fin = info["dias"]
        if inicio <= dia_ciclo <= fin:
            return f
    return "Lútea"

# Interfaz de usuario con Streamlit
st.title("🩸 Calendario de Ciclo Menstrual y Deporte")
st.write("Optimiza tus entrenamientos según tu momento biológico.")

# Panel de configuración del ciclo
st.sidebar.header("⚙️ Configuración de tu Ciclo")

duracion_ciclo = st.sidebar.selectbox(
    "¿Cuánto dura habitualmente tu ciclo completo?",
    options=[28, 30, 32],
    format_func=lambda x: f"{x} días"
)

fecha_inicio = st.sidebar.date_input("Fecha de INICIO de tu última regla:", datetime.now().date())
fecha_fin = st.sidebar.date_input("Fecha de FIN de tu última regla:", datetime.now().date() + timedelta(days=5))

# Validación simple de fechas
if fecha_fin < fecha_inicio:
    st.sidebar.error("Error: La fecha de fin no puede ser anterior a la de inicio.")
else:
    duracion_sangrado = (fecha_fin - fecha_inicio).days + 1
    st.sidebar.success(f"Duración estimada del sangrado: {duracion_sangrado} días.")

    # Cálculos para el día de HOY
    hoy_dt = datetime.now().date()
    diferencia_hoy = (hoy_dt - fecha_inicio).days
    dia_ciclo_hoy = (diferencia_hoy % duracion_ciclo) + 1
    fase_actual = determinar_fase(dia_ciclo_hoy, duracion_ciclo)
    info_hoy = obtener_datos_fase(fase_actual, duracion_ciclo)
    
    st.divider()
    
    # Métricas principales de HOY
    st.subheader("📅 Tu Estado el Día de Hoy")
    col1, col2 = st.columns(2)
    col1.metric(label="Fase Actual", value=fase_actual.upper())
    col2.metric(label="Día del Ciclo", value=f"Día {dia_ciclo_hoy} de {duracion_ciclo}")
    
    # Detalles del estado físico
    st.info(f"**Hormonas:** {info_hoy['hormonas']}")
    st.warning(f"**Impacto físico:** {info_hoy['rendimiento']}")
    
    # Síntomas y recomendaciones
    col_sintomas, col_entreno = st.columns(2)
    
    with col_sintomas:
        st.subheader("🧠 Síntomas Frecuentes")
        for s in info_hoy["sintomas"]:
            st.write(f"• {s}")
            
    with col_entreno:
        st.subheader("🏋️‍♀️ Ejercicio para Hoy")
        for deporte, rec in info_hoy["recommendaciones"].items():
            st.write(f"**{deporte}:** {rec}")
            
    st.divider()
    
    # --- NUEVA SECCIÓN DE CALENDARIO VISUAL SIMULADO ---
    st.subheader("🗓️ Calendario Visual de Proyecciones")
    st.write("Selecciona una fecha en el simulador para ver qué fase te corresponderá y planificar tu rutina:")
    
    # Usamos un date_input interactivo que actúa como un selector de calendario mensual integrado
    fecha_futura_elegida = st.date_input(
        "Haz clic aquí para abrir el calendario y elegir cualquier día del mes:",
        value=hoy_dt
    )
    
    # Calcular datos de la fecha seleccionada en el calendario
    diferencia_futura = (fecha_futura_elegida - fecha_inicio).days
    dia_ciclo_futuro = (diferencia_futura % duracion_ciclo) + 1
    fase_futura = determinar_fase(dia_ciclo_futuro, duracion_ciclo)
    info_futura = obtener_datos_fase(fase_futura, duracion_ciclo)
    
    # Emojis orientativos de fase
    emojis = {"Menstrual": "🩸", "Folicular": "⚡", "Ovulatoria": "🔥", "Lútea": "🧘‍♀️"}
    
    # Cuadro de resultados dinámico según el día seleccionado en el calendario
    st.subheader(f"🔮 Proyección para el {fecha_futura_elegida.strftime('%d/%m/%Y')}")
    st.markdown(f"Ese día estarás en el **Día {dia_ciclo_futuro}** de tu ciclo (Fase {emojis[fase_futura]} **{fase_futura}**).")
    
    # Desglose en pestañas limpias de lo que pasará ese día elegido
    pestana1, pestana2 = st.tabs(["🎯 Síntomas y Energía", "🚴 Recomendaciones de Deporte"])
    with pestana1:
        st.write(f"**Energía estimada:** {info_futura['rendimiento']}")
        st.write("**Síntomas probables:** " + ", ".join(info_futura["sintomas"]))
    with pestana2:
        for dep, texto in info_futura["recomendaciones"].items():
            st.write(f"• **{dep}**: {texto}")
