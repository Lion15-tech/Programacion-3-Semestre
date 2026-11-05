import sqlite3

conexion = sqlite3.connect("Gimnasio.db")
cursor= conexion.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("CREATE TABLE IF NOT EXISTS clientes(ID INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT, tipo_membresia TEXT, telefono TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS estado_membresia(ID, tipo_membresia TEXT, vigencia TEXT, proximo_pago TEXT, FOREIGN KEY(ID) REFERENCES clientes(ID) ON DELETE CASCADE)")

cursor.execute("CREATE TABLE IF NOT EXISTS inversion(unico REAL, mensual REAL, anual REAL)")

cursor.execute("CREATE TABLE IF NOT EXISTS instalaciones(zona_cardio TEXT, zona_maquinas TEXT, zona_peso_libre TEXT)")

def agregar_usuario(nombre, apellido, tipo_membresia, telefono):
    conexion= sqlite3.connect("Gimnasio.db")
    cursor= conexion.cursor()

    insertar= "INSERT INTO clientes (nombre, apellido, tipo_membresia, telefono) VALUES (?,?,?,?)"
    cursor.execute(insertar, (nombre, apellido, tipo_membresia, telefono))

    id_usuario= cursor.lastrowid
    conexion.commit()
    conexion.close()
    return id_usuario

def agregar_estado_membresia(ID, tipo_membresia, vigencia, proximo_pago):
    conexion= sqlite3.connect("Gimnasio.db")
    cursor = conexion.cursor()

    insertar= "INSERT INTO estado_membresia (ID, tipo_membresia, vigencia, proximo_pago) VALUES(?,?,?,?)"
    cursor.execute(insertar, (ID,tipo_membresia,vigencia,proximo_pago))

    conexion.commit()
    conexion.close()


conexion.commit()
conexion.close()

id_usuario = agregar_usuario("Adrián", "Hernández", "Básico", "442 123 4567")
id_usuario = agregar_usuario("Nestor", "Morales", "Estandar", "442 987 6543")
id_usuario = agregar_usuario("Camila", "Gonzáles", "Básico", "442 856 7810")
id_usuario = agregar_usuario("Monika", "Asano", "Ultra", "442 456 7890")
id_usuario = agregar_usuario("Jorge", "González", "Estandar", "442 123 4561")
id_usuario = agregar_usuario("María", "López", "Básico", "442 987 6542")
id_usuario = agregar_usuario("Luis", "Ramírez", "Estandar", "442 856 7813")
id_usuario = agregar_usuario("Sofía", "Martínez", "Ultra", "442 456 7894")
id_usuario = agregar_usuario("Diego", "Hernández", "Básico", "442 123 4565")
id_usuario = agregar_usuario("Valeria", "García", "Estandar", "442 987 6546")
id_usuario = agregar_usuario("Andrés", "Pérez", "Básico", "442 856 7817")
id_usuario = agregar_usuario("Isabella", "Rodríguez", "Ultra", "442 456 7230")
id_usuario = agregar_usuario("Fernando", "Sánchez", "Estandar", "442 123 4569")
id_usuario = agregar_usuario("Camila", "Torres", "Básico", "442 987 6533")
id_usuario = agregar_usuario("Valentina", "Ramírez", "Estandar", "442 856 7831")
id_usuario = agregar_usuario("Sebastián", "González", "Ultra", "442 456 7839")
id_usuario = agregar_usuario("Martín", "Hernández", "Básico", "442 123 4527")

agregar_estado_membresia(id_usuario, "Básico", "ACTIVA", "2024-07-01")
agregar_estado_membresia(id_usuario, "Estandar", "ACTIVA", "2024-07-01")
agregar_estado_membresia(id_usuario, "Básico", "ACTIVA", "2024-07-01")
agregar_estado_membresia(id_usuario, "Ultra", "ACTIVA", "2024-07-01")
agregar_estado_membresia(id_usuario, "Ultra", "ACTIVA", "2024-07-01")

