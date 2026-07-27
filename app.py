# ==========================================================
# RECOMENDACIONES DEL DÍA
# ==========================================================

frame_recomendaciones = tk.LabelFrame(
    root,
    text="🏋️ Recomendaciones deportivas",
    bg=COLOR_FONDO,
    font=("Segoe UI", 11, "bold"),
    padx=10,
    pady=10
)

frame_recomendaciones.pack(fill="x", padx=20, pady=10)

rec = recomendaciones(fase_actual)

texto_recomendaciones = ""

for deporte, descripcion in rec.items():

    texto_recomendaciones += f"{deporte}\n"

    texto_recomendaciones += f"• {descripcion}\n\n"

lbl_recomendaciones = tk.Label(
    frame_recomendaciones,
    text=texto_recomendaciones,
    justify="left",
    bg=COLOR_FONDO,
    font=("Segoe UI", 10)
)

lbl_recomendaciones.pack(anchor="w")


# ==========================================================
# CALENDARIO
# ==========================================================

frame_calendario = tk.LabelFrame(
    root,
    text="📅 Calendario mensual",
    bg=COLOR_FONDO,
    padx=10,
    pady=10,
    font=("Segoe UI", 11, "bold")
)

frame_calendario.pack(fill="both", expand=True, padx=20, pady=10)

dias_semana = [
    "Lun",
    "Mar",
    "Mié",
    "Jue",
    "Vie",
    "Sáb",
    "Dom"
]

for coluna, nombre in enumerate(dias_semana):

    tk.Label(
        frame_calendario,
        text=nombre,
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO,
        font=("Segoe UI", 10, "bold"),
        width=12
    ).grid(row=0, column=coluna, padx=3, pady=3)


cal = calendar.monthcalendar(anio, mes)


# ==========================================================
# DETALLE DEL DÍA
# ==========================================================

def mostrar_detalle(numero_dia):

    dia_ciclo = ((numero_dia - 1) % 28) + 1

    fase = obtener_fase(dia_ciclo)

    energia = energia_fase(fase)

    fert = fertilidad(dia_ciclo)

    recomendaciones_dia = recomendaciones(fase)

    ventana = tk.Toplevel(root)

    ventana.title(f"Día {numero_dia}")

    ventana.geometry("600x650")

    ventana.configure(bg=color_fase(fase))

    titulo = tk.Label(

        ventana,

        text=f"{numero_dia}/{mes}/{anio}",

        bg=color_fase(fase),

        font=("Segoe UI",18,"bold")

    )

    titulo.pack(pady=10)

    tk.Label(

        ventana,

        text=f"Fase: {fase}",

        bg=color_fase(fase),

        font=("Segoe UI",13)

    ).pack()

    tk.Label(

        ventana,

        text=f"Energía: {'⭐'*energia}",

        bg=color_fase(fase),

        font=("Segoe UI",13)

    ).pack()

    tk.Label(

        ventana,

        text=f"Fertilidad estimada: {fert}",

        bg=color_fase(fase),

        font=("Segoe UI",13,"bold")

    ).pack(pady=10)

    frame = tk.LabelFrame(

        ventana,

        text="Síntomas",

        bg=color_fase(fase)

    )

    frame.pack(fill="x", padx=15, pady=10)

    checks = []

    for sintoma in SINTOMAS:

        var = tk.BooleanVar()

        c = tk.Checkbutton(

            frame,

            text=sintoma,

            variable=var,

            bg=color_fase(fase)

        )

        c.pack(anchor="w")

        checks.append(var)

    frame2 = tk.LabelFrame(

        ventana,

        text="Recomendaciones",

        bg=color_fase(fase)

    )

    frame2.pack(fill="both", expand=True, padx=15, pady=10)

    texto = ""

    for deporte, descripcion in recomendaciones_dia.items():

        texto += f"{deporte}\n"

        texto += f"{descripcion}\n\n"

    tk.Label(

        frame2,

        text=texto,

        justify="left",

        bg=color_fase(fase),

        font=("Segoe UI",10)

    ).pack(anchor="w", padx=10, pady=10)

    tk.Button(

        ventana,

        text="Cerrar",

        bg=COLOR_BOTON,

        command=ventana.destroy

    ).pack(pady=15)


# ==========================================================
# CREAR TARJETAS DEL CALENDARIO
# ==========================================================

for fila, semana in enumerate(cal, start=1):

    for columna, numero_dia in enumerate(semana):

        if numero_dia == 0:

            tk.Label(

                frame_calendario,

                text="",

                width=12,

                height=5,

                bg=COLOR_FONDO

            ).grid(row=fila,column=columna,padx=3,pady=3)

            continue

        dia_ciclo = ((numero_dia - 1) % 28) + 1

        fase = obtener_fase(dia_ciclo)

        color = color_fase(fase)

        boton = tk.Button(

            frame_calendario,

            text=f"{numero_dia}\n{fase}",

            bg=color,

            relief="flat",

            width=12,

            height=5,

            wraplength=80,

            command=lambda d=numero_dia: mostrar_detalle(d)

        )

        boton.grid(

            row=fila,

            column=columna,

            padx=3,

            pady=3,

            sticky="nsew"

        )


for i in range(7):

    frame_calendario.grid_columnconfigure(i, weight=1)
    
