]
"""

from datetime import datetime, timedelta

# Diccionario con la información detallada de cada fase del ciclo
FASES_CICLO = {
    "Menstrual": {
        "dias": (1, 5),
        "hormonas": "Estrógenos y progesterona en niveles muy bajos.",
        "rendimiento": "Energía reducida, mayor percepción de fatiga, pero buena tolerancia al dolor inicial.",
        "sintomas": ["Cólicos abdominales", "Fatiga o letargo", "Dolor lumbar", "Retención de líquidos leve"],
        "recomendaciones": {
            "Funcional": "Movilidad articular, yoga suave, estiramientos y ejercicios de baja intensidad sin impacto.",
            "Gym": "Ejercicios con cargas livianas a moderadas, priorizando repeticiones altas si hay energía, o descanso activo.",
            "Running": "Trote suave o caminata ligera. Evitar entrenamientos de alta intensidad (HIIT) o fondo largo.",
            "Ciclismo": "Rodajes suaves y planos en zona 1-2. Evitar puertos exigentes o series de potencia."
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
            "Running": "Series de velocidad, intervalos (HIIT) y tiradas largas a ritmos alegres.",
            "Ciclismo": "Entrenamientos de potencia, intervalos cortos de alta intensidad y escalada."
        }
    },
    "Ovulatoria": {
        "dias": (14, 15),
        "hormonas": "Pico máximo de estrógenos y pico de la hormona luteinizante (LH).",
        "rendimiento": "Fuerza máxima y máxima energía, aunque hay un pequeño riesgo de lesión de rodilla/ligamentos por laxitud.",
        "sintomas": ["Mayor libido", "Dolor leve en un lado del abdomen (Mittelschmerz)", "Flujo cervical elástico"],
        "recomendaciones": {
            "Funcional": "Ejercicios de estabilidad de core, control neuromuscular y fuerza explosiva con buena técnica.",
            "Gym": "Excelente para potencia máxima y levantamientos pesados, cuidando muy bien el calentamiento articular.",
            "Running": "Rendimiento óptimo para competir o hacer marcas en distancias medias/largas.",
            "Ciclismo": "Salidas fuertes en grupeta o crono, aprovechando el pico de máxima capacidad respiratoria y fuerza."
        }
    },
    "Lútea": {
        "dias": (16, 28),
        "hormonas": "Aumento de progesterona y caída posterior si no hay fecundación (fase premenstrual al final).",
        "rendimiento": "La temperatura corporal sube; la resistencia cardiovascular disminuye ligeramente al inicio y decae la energía al final.",
        "sintomas": ["Ansiedad o cambios de humor", "Sensibilidad en los senos", "Hinchazón o gases", "Fatiga premenstrual"],
        "recomendaciones": {
            "Funcional": "Pilates, entrenamientos de fuerza moderada controlando la respiración y bajando la exigencia.",
            "Gym": "Mantener pesos moderados, priorizar técnica y evitar llegar al fallo muscular absoluto en la última semana.",
            "Running": "Carrera continua a ritmo constante y cómodo (zona aeróbica). Evitar sesiones agónicas de velocidad.",
            "Ciclismo": "Rodajes base estables de larga duración pero a baja intensidad conversacional."
        }
    }
}

def determinar_fase(dia_ciclo):
    """Retorna el nombre de la fase según el día del ciclo actual."""
    for fase, datos in FASES_CICLO.items():
        inicio, fin = datos["dias"]
        if inicio <= dia_ciclo <= fin:
            return fase
    return "Lútea" # Por si el ciclo se alarga más de 28 días

def calcular_dia_actual(fecha_inicio_str):
    """Calcula cuántos días han pasado desde la fecha de la última regla."""
    formato = "%Y-%m-%d"
    fecha_inicio = datetime.strptime(fecha_inicio_str, formato)
    hoy = datetime.now()
    diferencia = (hoy - fecha_inicio).days
    # Asumimos un ciclo estándar de 28 días para reiniciar el conteo modular si pasa de 28
    dia_ciclo = (diferencia % 28) + 1
    return dia_ciclo, diferencia

def main():
    print("==================================================")
    print("   CALENDARIO DE CICLO MENSTRUAL Y RENDIMIENTO    ")
    print("==================================================")
    
    # Ejemplo interactivo o predeterminado
    entrada_usuario = input("Ingresa la fecha de tu último periodo (YYYY-MM-DD) o presiona Enter para usar una de prueba: ").strip()
    
    if not entrada_usuario:
        # Fecha de prueba simulada (hace 10 días)
        fecha_prueba = datetime.now() - timedelta(days=10)
        entrada_usuario = fecha_prueba.strftime("%Y-%m-%d")
        print(f">> Usando fecha simulada de hace 10 días: {entrada_usuario}")
        
    try:
        dia_ciclo, dias_totales = calcular_dia_actual(entrada_usuario)
        fase_actual = determinar_fase(dia_ciclo)
        info = FASES_CICLO[fase_actual]
        
        print("\n----------------- RESULTADOS -----------------")
        print(f"Días desde el inicio registrado: {dias_totales} días")
        print(f"Días estimándose en tu ciclo actual: Día {dia_ciclo} de 28")
        print(f"Fase actual en la que te encuentras: {fase_actual.upper()}")
        print(f"Panorama hormonal: {info['hormonas']}")
        print(f"Impacto en rendimiento: {info['rendimiento']}")
        
        print("\n--- POSIBLES SÍNTOMAS FRECUENTES ---")
        for s in info["sintomas"]:
            print(f" • {s}")
            
        print("\n--- RECOMENDACIONES DE ENTRENAMIENTO ---")
        for deporte, rec in info["recomendaciones"].items():
            print(f" [{deporte}]: {rec}")
            
        print("\n==================================================")
        print("¡Escucha a tu cuerpo y adapta las cargas, no las suspendas!")
        
    except ValueError:
        print("Formato de fecha incorrecto. Por favor usa YYYY-MM-DD.")

if __name__ == "__main__":
    main()
