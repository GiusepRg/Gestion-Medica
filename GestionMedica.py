import datetime
from datetime import timedelta

# --- Simulación de Base de Datos (Datos en Memoria) ---
# Usamos listas de diccionarios para simular las tablas de una base de datos.

doctores = [
    {"id": 1, "nombre": "Dr. García", "especialidad": "Cardiología", "horarios": [
        {"dia": "Lunes", "inicio": "09:00", "fin": "13:00"},
        {"dia": "Martes", "inicio": "09:00", "fin": "13:00"}
    ]},
    {"id": 2, "nombre": "Dra. Martínez", "especialidad": "Dermatología", "horarios": [
        {"dia": "Lunes", "inicio": "10:00", "fin": "15:00"},
        {"dia": "Miércoles", "inicio": "08:00", "fin": "12:00"}
    ]},
    {"id": 3, "nombre": "Dr. López", "especialidad": "Cardiología", "horarios": [
        {"dia": "Jueves", "inicio": "14:00", "fin": "18:00"}
    ]}
]

pacientes = [
    {"id": 101, "nombre": "Ana Torres", "contacto": "ana.torres@email.com"},
    {"id": 102, "nombre": "Carlos Ruiz", "contacto": "555-1234"}
]

citas = [
    {"id": 1, "id_paciente": 101, "id_medico": 1,
     "fecha": (datetime.date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
     "hora": "10:00", "motivo": "Chequeo general", "estado": "Programada"},
    {"id": 2, "id_paciente": 102, "id_medico": 2,
     "fecha": datetime.date.today().strftime("%Y-%m-%d"),
     "hora": "11:30", "motivo": "Consulta de piel", "estado": "Programada"}
]

id_proxima_cita = 3  # Para autoincrementar el ID de nuevas citas
