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


#------------------------------------------------------
# --- Funcionalidades del Paciente ---

def HU_1_2_buscar_medicos_disponibles():
    print("\n--- Búsqueda de Médicos Disponibles ---")
    especialidad = input("Ingrese la especialidad que busca: ").strip()
    fecha_str = input("Ingrese la fecha (YYYY-MM-DD): ").strip()
    
    dia_semana = formato_fecha_a_dia_semana(fecha_str)
    if not dia_semana:
        print("Error: Formato de fecha incorrecto.")
        return

    print(f"\nResultados para '{especialidad}' el {fecha_str} ({dia_semana}):")
    
    medicos_encontrados = False
    for medico in doctores:
        if medico["especialidad"].lower() == especialidad.lower():
            horarios_del_dia = [h for h in medico["horarios"] if h["dia"] == dia_semana]
            if horarios_del_dia:
                medicos_encontrados = True
                print(f"\nDr(a). {medico['nombre']} (ID: {medico['id']})")
                
                citas_agendadas = [c["hora"] for c in citas if c["id_medico"] == medico["id"] and c["fecha"] == fecha_str]
                franjas_disponibles = []
                for horario in horarios_del_dia:
                    hora_inicio = datetime.datetime.strptime(horario["inicio"], "%H:%M")
                    hora_fin = datetime.datetime.strptime(horario["fin"], "%H:%M")
                    hora_actual = hora_inicio
                    while hora_actual < hora_fin:
                        hora_slot = hora_actual.strftime("%H:%M")
                        if hora_slot not in citas_agendadas:
                            franjas_disponibles.append(hora_slot)
                        hora_actual += timedelta(hours=1)
                
                if franjas_disponibles:
                    print("  Franjas horarias disponibles:", ", ".join(franjas_disponibles))
                else:
                    print("  No hay franjas horarias disponibles para este día.")

    if not medicos_encontrados:
        print("No se encontraron médicos con esa especialidad o que trabajen ese día.")


def HU_1_1_reservar_cita():
    global id_proxima_cita
    print("\n--- Reservar Nueva Cita ---")
    try:
        id_paciente = int(input("Ingrese su ID de paciente: ").strip())
        id_medico = int(input("Ingrese el ID del médico: ").strip())
        fecha = input("Ingrese la fecha (YYYY-MM-DD): ").strip()
        hora = input("Ingrese la hora (HH:MM): ").strip()
        motivo = input("Motivo de la consulta: ").strip()
    except ValueError:
        print("Error: ID debe ser un número.")
        return

    franja_ocupada = any(c["id_medico"] == id_medico and c["fecha"] == fecha and c["hora"] == hora for c in citas)
    if franja_ocupada:
        print("Error: La franja ya está ocupada.")
        return

    nueva_cita = {
        "id": id_proxima_cita,
        "id_paciente": id_paciente,
        "id_medico": id_medico,
        "fecha": fecha,
        "hora": hora,
        "motivo": motivo,
        "estado": "Programada"
    }
    citas.append(nueva_cita)
    id_proxima_cita += 1

    print("¡Cita reservada con éxito!")
    contacto = obtener_contacto_paciente(id_paciente)
    if contacto:
        print(f"Enviando confirmación a {contacto}...")
# --- Funcionalidades del Médico ---

def menu_medico():
    try:
        id_medico = int(input("\nIngrese su ID de Médico: ").strip())
        if not any(m['id'] == id_medico for m in doctores):
            print("Error: Médico no encontrado.")
            return
    except ValueError:
        print("Error: ID inválido.")
        return

    while True:
        print(f"\n--- Portal del Médico: {obtener_nombre_medico(id_medico)} ---")
        print("1. Ver mi agenda")
        print("2. Actualizar estado de cita")
        print("3. Volver")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            HU_2_1_y_2_2_ver_agenda(id_medico)
        elif opcion == '2':
            HU_2_2_actualizar_estado_cita(id_medico)
        elif opcion == '3':
            break
        else:
            print("Opción no válida.")


def HU_2_1_y_2_2_ver_agenda(id_medico):
    fecha_str = input("Ingrese la fecha (YYYY-MM-DD), o Enter para hoy: ").strip()
    if not fecha_str:
        fecha_str = datetime.date.today().strftime("%Y-%m-%d")

    print(f"\n--- Agenda para {fecha_str} ---")
    citas_del_dia = [c for c in citas if c["id_medico"] == id_medico and c["fecha"] == fecha_str]
    citas_del_dia.sort(key=lambda x: datetime.datetime.strptime(x['hora'], '%H:%M'))

    if not citas_del_dia:
        print("No tiene citas hoy.")
    else:
        print("{:<8} {:<20} {:<25} {:<15}".format("Hora", "Paciente", "Motivo", "Estado"))
        print("-" * 70)
        for c in citas_del_dia:
            print("{:<8} {:<20} {:<25} {:<15}".format(
                c["hora"], obtener_nombre_paciente(c["id_paciente"]), c["motivo"], c["estado"]))


def HU_2_2_actualizar_estado_cita(id_medico):
    print("\n--- Actualizar Estado de Cita ---")
    try:
        id_cita = int(input("Ingrese el ID de la cita: ").strip())
    except ValueError:
        print("Error: ID inválido.")
        return

    cita = next((c for c in citas if c["id"] == id_cita and c["id_medico"] == id_medico), None)
    if not cita:
        print("Cita no encontrada o no le pertenece.")
        return

    print("1. Atendida")
    print("2. No asistió")
    opcion = input("Opción: ")

    if opcion == '1':
        cita["estado"] = "Atendida"
        print("Cita marcada como atendida.")
    elif opcion == '2':
        cita["estado"] = "No asistió"
        print("Cita marcada como no asistió.")
    else:
        print("Opción no válida.")
#------------------------------------------------------
# --- Funcionalidades del Recepcionista / Administrador ---

def HU_3_2_gestionar_horarios():
    print("\n--- Gestión de Horarios ---")
    for m in doctores:
        print(f"ID: {m['id']}, Nombre: {m['nombre']}")

    try:
        id_medico = int(input("Ingrese ID del médico: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    medico = next((m for m in doctores if m["id"] == id_medico), None)
    if not medico:
        print("Médico no encontrado.")
        return

    print("Horarios actuales:")
    for h in medico["horarios"]:
        print(f"- {h['dia']}: {h['inicio']} - {h['fin']}")

    dia = input("Nuevo día: ").capitalize()
    inicio = input("Hora inicio (HH:MM): ").strip()
    fin = input("Hora fin (HH:MM): ").strip()

    try:
        i = datetime.datetime.strptime(inicio, "%H:%M")
        f = datetime.datetime.strptime(fin, "%H:%M")
        if i >= f:
            print("Error: hora inválida.")
            return
    except ValueError:
        print("Formato incorrecto.")
        return

    medico["horarios"].append({"dia": dia, "inicio": inicio, "fin": fin})
    print("Horario agregado con éxito.")


def HU_3_1_enviar_recordatorios_automaticos():
    print("\n--- Envío de Recordatorios ---")
    fecha_manana = (datetime.date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    for c in citas:
        if c["fecha"] == fecha_manana and c["estado"] == "Programada":
            contacto = obtener_contacto_paciente(c["id_paciente"])
            if contacto:
                print(f"Recordatorio enviado a {contacto} para cita con {obtener_nombre_medico(c['id_medico'])} a las {c['hora']}.")
            else:
                print(f"No se pudo enviar recordatorio para cita {c['id']}, sin contacto.")
