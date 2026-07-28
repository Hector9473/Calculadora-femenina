import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página de Streamlit
st.set_page_config(page_title="Rendimiento y Ciclo Menstrual", page_icon="🩸", layout="centered")

# Diccionario con la información detallada de cada fase del ciclo
FASES_CICLO = {
    "Menstrual": {
        "dias": (1, 5),
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
        "dias": (6, 13),
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
        "dias": (14, 15),
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
        "dias": (16, 28),
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

def determinar_fase(dia_ciclo):
    # Retorna el nombre de la fase según el día del ciclo actual
    for fase, datos in FASES_CICLO.items():
        inicio, fin = datos["dias"]
        if inicio <= dia_ciclo <= fin:
            return fase
    return "Lútea"

def calcular_dia_actual(fecha_inicio):
    # Calcula los días que pasaron desde la fecha de inicio del periodo
    hoy = datetime.now().date()
    diferencia = (hoy - fecha_inicio).days
    dia_ciclo = (diferencia % 28) + 1
    return dia_ciclo, diferencia

# Interfaz de usuario con Streamlit
st.title("🩸 Calendario de Ciclo Menstrual y Deporte")
st.write("Optimiza tus entrenamientos según tu momento biológico.")

# Selector de fecha integrado
fecha_seleccionada = st.date_input("Selecciona la fecha de tu última regla (FUR):", datetime.now().date())

if fecha_seleccionada:
    dia_ciclo, dias_totales = calcular_dia_actual(fecha_seleccionada)
    fase_actual = determinar_fase(dia_ciclo)
    info = FASES_CICLO[fase_actual]
    
    st.divider()
    
    # Métricas principales de HOY
    st.subheader("📅 Tu Estado el Día de Hoy")
    col1, col2 = st.columns(2)
    col1.metric(label="Fase Actual", value=fase_actual.upper())
    col2.metric(label="Día del Ciclo", value=f"Día {dia_ciclo} de 28")
    
    # Detalles del estado físico
    st.info(f"**Hormonas:** {info['hormonas']}")
    st.warning(f"**Impacto físico:** {info['rendimiento']}")
    
    # Síntomas
    st.subheader("🧠 Posibles Síntomas Frecuentes")
    for s in info["sintomas"]:
        st.write(f"• {s}")
        
    # Recomendaciones deportivas
    st.subheader("🏋️‍♀️ Recomendaciones de Entrenamiento")
    for deporte, rec in info["recomendaciones"].items():
        with st.expander(f"Recomendación para **{deporte}**"):
            st.write(rec)
            
    st.success("¡Escucha a tu cuerpo y adapta las cargas, no las suspendas!")
    
    st.divider()
    
    # --- NUEVA VENTANA DE PROYECCIÓN MENSUAL ---
    st.subheader("🔮 Proyección Mensual (Próximos 30 días)")
    st.write("Planifica tus entrenamientos de las siguientes semanas sabiendo qué fase te espera:")
    
    # Creamos un contenedor expandible para no saturar la pantalla inicial
    with st.expander("Ver calendario de proyección día por día"):
        hoy_dt = datetime.now().date()
        
        # Generamos la tabla de proyección
        for i in range(30):
            fecha_futura = hoy_dt + timedelta(days=i)
            # Calculamos qué día del ciclo será en esa fecha futura
            diferencia_futura = (fecha_futura - fecha_seleccionada).days
            dia_ciclo_futuro = (diferencia_futura % 28) + 1
            fase_futura = determinar_fase(dia_ciclo_futuro)
            
            # Formateamos la fecha en castellano amigable
            fecha_formateada = fecha_futura.strftime("%d / %m / %Y")
            
            # Asignamos un emoji según la fase para que sea visualmente escaneable
            emoji_fase = "🩸" if fase_futura == "Menstrual" else "⚡" if fase_futura == "Folicular" else "🔥" if fase_futura == "Ovulatoria" else "🧘‍♀️"
            
            # Mostramos la línea con estilo limpio
            st.write(f"**{fecha_formateada}** — Día {dia_ciclo_futuro:02d} | {emoji_fase} Fase **{fase_futura}**")
