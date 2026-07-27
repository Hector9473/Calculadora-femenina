"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🌸 CycleFit Tracker v1.0                        ║
║                                                              ║
║     Seguimiento del ciclo menstrual y entrenamiento          ║
║                                                              ║
║  Autor : Hector Salazar                                     ║
║  Licencia : MIT                                              ║
║  Lenguaje : Python 3.12+                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

# ============================================================
# IMPORTACIONES
# ============================================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime, timedelta

import calendar

import json

import os

from pathlib import Path

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

APP_NAME = "CycleFit Tracker"

VERSION = "1.0"

WINDOW_WIDTH = 1450

WINDOW_HEIGHT = 900

JSON_FILE = "datos.json"



# ============================================================
# PALETA DE COLORES
# (Pastel accesible)
# ============================================================

COLORS = {

    "background": "#FAFAFA",

    "card": "#FFFFFF",

    "border": "#D8D8D8",

    "text": "#222222",

    "button": "#9EC5FE",

    "button_hover": "#7FB3FF",

    "menstruacion": "#FFD6E8",

    "folicular": "#D8F3DC",

    "ovulacion": "#FFF3BF",

    "lutea": "#E9D8FD"

}



# ============================================================
# FUENTES
# ============================================================

FONT_SMALL = ("Segoe UI", 10)

FONT_NORMAL = ("Segoe UI", 11)

FONT_TITLE = ("Segoe UI", 18, "bold")

FONT_BIG = ("Segoe UI", 26, "bold")



# ============================================================
# SÍNTOMAS DISPONIBLES
# ============================================================

SYMPTOMS = [

    "Cólicos",

    "Dolor de cabeza",

    "Migraña",

    "Fatiga",

    "Inflamación",

    "Antojos",

    "Ansiedad",

    "Estrés",

    "Irritabilidad",

    "Acné",

    "Sensibilidad senos",

    "Náuseas"

]



# ============================================================
# BASE DE DATOS JSON
# ============================================================

class JsonDatabase:

    """
    Guarda toda la información del programa.
    """

    def __init__(self):

        self.file = JSON_FILE

        self.data = {

            "config":{

                "cycle_length":28,

                "period_length":5

            },

            "periods":[],

            "symptoms":{},

            "energy":{},

            "training":{},

            "notes":{}

        }

        self.load()



    def load(self):

        if Path(self.file).exists():

            try:

                with open(

                    self.file,

                    "r",

                    encoding="utf8"

                ) as f:

                    self.data = json.load(f)

            except:

                self.save()

        else:

            self.save()



    def save(self):

        with open(

            self.file,

            "w",

            encoding="utf8"

        ) as f:

            json.dump(

                self.data,

                f,

                indent=4,

                ensure_ascii=False

            )



    def get_cycle(self):

        return self.data["config"]["cycle_length"]



    def set_cycle(self,value):

        self.data["config"]["cycle_length"]=value

        self.save()



    def get_period(self):

        return self.data["config"]["period_length"]



    def set_period(self,value):

        self.data["config"]["period_length"]=value

        self.save()



# ============================================================
# MOTOR DEL CICLO
# ============================================================

class CycleEngine:

    """
    Toda la lógica del ciclo menstrual.
    """

    def __init__(self,db):

        self.db = db



    def get_phase(self,day):

        cycle = self.db.get_cycle()

        period = self.db.get_period()

        ovulation = cycle - 14

        if day <= period:

            return "Menstruación"

        elif day < ovulation - 2:

            return "Folicular"

        elif ovulation - 2 <= day <= ovulation + 2:

            return "Ovulación"

        else:

            return "Lútea"



    def get_phase_color(self,phase):

        colors = {

            "Menstruación":COLORS["menstruacion"],

            "Folicular":COLORS["folicular"],

            "Ovulación":COLORS["ovulacion"],

            "Lútea":COLORS["lutea"]

        }

        return colors[phase]



    def get_energy(self,phase):

        values = {

            "Menstruación":2,

            "Folicular":4,

            "Ovulación":5,

            "Lútea":3

        }

        return values[phase]



    def fertility(self,day):

        cycle = self.db.get_cycle()

        ovulation = cycle - 14

        if ovulation - 2 <= day <= ovulation + 2:

            return "🔴 Alta"

        elif ovulation - 4 <= day <= ovulation + 4:

            return "🟡 Media"

        return "🟢 Baja"



    def next_period(self,last_date):

        return last_date + timedelta(

            days=self.db.get_cycle()

        )
        # ============================================================
# CLASE PRINCIPAL
# ============================================================

class CycleFitApp(tk.Tk):

    def __init__(self):

        super().__init__()

        self.db = JsonDatabase()

        self.engine = CycleEngine(self.db)

        self.title(f"{APP_NAME}  v{VERSION}")

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.minsize(1200, 750)

        self.configure(bg=COLORS["background"])

        # Fecha actual

        self.today = datetime.today()

        self.current_year = self.today.year

        self.current_month = self.today.month

        self.selected_day = self.today.day

        self.build_layout()

        self.draw_calendar()

        self.update_information_panel()


# ============================================================
# INTERFAZ
# ============================================================

    def build_layout(self):

        # ---------------------------
        # CABECERA
        # ---------------------------

        header = tk.Frame(

            self,

            bg=COLORS["background"]

        )

        header.pack(fill="x", padx=15, pady=10)

        tk.Label(

            header,

            text="🌸 CycleFit Tracker",

            font=FONT_BIG,

            bg=COLORS["background"],

            fg=COLORS["text"]

        ).pack(side="left")

        self.month_label = tk.Label(

            header,

            font=FONT_TITLE,

            bg=COLORS["background"],

            fg=COLORS["text"]

        )

        self.month_label.pack(side="right")



        # ---------------------------
        # CONTENIDO
        # ---------------------------

        content = tk.Frame(

            self,

            bg=COLORS["background"]

        )

        content.pack(

            fill="both",

            expand=True,

            padx=15,

            pady=10

        )



        # ---------------------------
        # CALENDARIO
        # ---------------------------

        self.calendar_frame = tk.LabelFrame(

            content,

            text="Calendario",

            font=FONT_NORMAL,

            bg=COLORS["card"],

            padx=10,

            pady=10

        )

        self.calendar_frame.pack(

            side="left",

            fill="both",

            expand=True

        )



        # ---------------------------
        # PANEL DERECHO
        # ---------------------------

        self.right_panel = tk.LabelFrame(

            content,

            text="Información del día",

            bg=COLORS["card"],

            font=FONT_NORMAL,

            width=360,

            padx=15,

            pady=15

        )

        self.right_panel.pack(

            side="right",

            fill="y",

            padx=(15,0)

        )

        self.right_panel.pack_propagate(False)



        # ---------------------------
        # PIE
        # ---------------------------

        footer = tk.Frame(

            self,

            bg=COLORS["background"]

        )

        footer.pack(fill="x")

        tk.Label(

            footer,

            text="CycleFit Tracker © 2026",

            bg=COLORS["background"],

            fg="gray"

        ).pack(pady=5)



# ============================================================
# DIBUJAR CALENDARIO
# ============================================================

    def draw_calendar(self):

        for widget in self.calendar_frame.winfo_children():

            widget.destroy()

        meses = [

            "Enero","Febrero","Marzo","Abril",

            "Mayo","Junio","Julio","Agosto",

            "Septiembre","Octubre","Noviembre","Diciembre"

        ]

        self.month_label.config(

            text=f"{meses[self.current_month-1]} {self.current_year}"

        )

        nav = tk.Frame(

            self.calendar_frame,

            bg=COLORS["card"]

        )

        nav.pack(fill="x", pady=(0,10))

        tk.Button(

            nav,

            text="◀",

            width=4,

            command=self.previous_month

        ).pack(side="left")

        tk.Button(

            nav,

            text="▶",

            width=4,

            command=self.next_month

        ).pack(side="right")

        days = [

            "Lun","Mar","Mié",

            "Jue","Vie","Sáb","Dom"

        ]

        header = tk.Frame(

            self.calendar_frame,

            bg=COLORS["card"]

        )

        header.pack()

        for name in days:

            tk.Label(

                header,

                text=name,

                width=12,

                font=("Segoe UI",10,"bold"),

                bg=COLORS["card"]

            ).pack(side="left")

        grid = tk.Frame(

            self.calendar_frame,

            bg=COLORS["card"]

        )

        grid.pack()

        cal = calendar.monthcalendar(

            self.current_year,

            self.current_month

        )

        for row in cal:

            row_frame = tk.Frame(

                grid,

                bg=COLORS["card"]

            )

            row_frame.pack()

            for number in row:

                if number == 0:

                    tk.Label(

                        row_frame,

                        text="",

                        width=12,

                        height=5,

                        bg=COLORS["card"]

                    ).pack(side="left", padx=2, pady=2)

                    continue

                cycle_day = ((number-1) %

                             self.db.get_cycle()) + 1

                phase = self.engine.get_phase(cycle_day)

                color = self.engine.get_phase_color(phase)

                icon = {

                    "Menstruación":"🩷",

                    "Folicular":"🟩",

                    "Ovulación":"🟨",

                    "Lútea":"🟪"

                }[phase]

                text = f"{number}\n{icon}"

                button = tk.Button(

                    row_frame,

                    text=text,

                    bg=color,

                    relief="flat",

                    width=12,

                    height=5,

                    command=lambda d=number:

                        self.select_day(d)

                )

                button.pack(

                    side="left",

                    padx=2,

                    pady=2

                )



# ============================================================
# CAMBIAR MES
# ============================================================

    def previous_month(self):

        self.current_month -= 1

        if self.current_month == 0:

            self.current_month = 12

            self.current_year -= 1

        self.draw_calendar()



    def next_month(self):

        self.current_month += 1

        if self.current_month == 13:

            self.current_month = 1

            self.current_year += 1

        self.draw_calendar()



# ============================================================
# SELECCIONAR DÍA
# ============================================================

    def select_day(self, day):

        self.selected_day = day

        self.update_information_panel()
        
