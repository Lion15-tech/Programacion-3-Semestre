import sqlite3 #TTK

DB = "GYM.db"

def conectar():
    return sqlite3.connect(DB)

def crear_tabla():
    with conectar() as conect:
        conect.execute('''CREATE TABLE IF NOT EXISTS clientes(
        ID TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        telefono TEXT NOT NULL,
        tipo_membresia TEXT NOT NULL) ''')    

def agregar_cliente(nombre,apellido,telefono,tipo_membresia, fecha_nacimiento):
    nuevo_id = generar_id(nombre, apellido, tipo_membresia, fecha_nacimiento)
    with conectar() as conect:
        conect.execute(
            'INSERT INTO clientes (ID,nombre,apellido,telefono,tipo_membresia, fecha_nacimiento) VALUES (?,?,?,?,?,?)',
        (nuevo_id,nombre,apellido,telefono, tipo_membresia, fecha_nacimiento))
        return nuevo_id
    
def modificar_cliente(ID, **valores):
    valor_protegido = {"ID"}
    valores_modificar = {"nombre", "apellido", "telefono", "tipo_membresia", "fecha_nacimiento"}

    if not valores:
        raise ValueError("No se proporcionó ningún campo a modificar")

    if valor_protegido & valores.keys():
        raise ValueError("El ID no se puede modificar")

    if not valores.keys() <= valores_modificar:
        invalidos = valores.keys() - valores_modificar
        raise ValueError(f"Campos no válidos: {invalidos}")

    actu_cliente = ", ".join(f"{columna} = ?" for columna in valores.keys())
    meter_valor = list(valores.values()) + [ID]

    actu_terminada = f"UPDATE clientes SET {actu_cliente} WHERE ID = ?"

    with conectar() as conect:
        cursor = conect.execute(actu_terminada, meter_valor)
        if cursor.rowcount == 0:
            return False
        return True

def eliminar_cliente(ID):
    with conectar() as conect:
        cursor= conect.execute("DELETE FROM clientes WHERE ID = ?",(ID,))  
        if cursor.rowcount == 0:
            return False
        return True  

def ver_clientes():
    with conectar() as conect:
        return conect.execute(
            "SELECT * FROM clientes"
        ).fetchall()

def generar_id(nombre, apellido, tipo_membresia):
    if not (nombre and apellido and tipo_membresia):
        raise ValueError("Nombre, apellido y membresía son obligatorios")

    inicial_apellido  = apellido.strip()[0].upper()
    inicial_nombre    = nombre.strip()[0].upper()
    inicial_membresia = tipo_membresia.strip()[0].upper()
    return f"{inicial_apellido}{inicial_nombre}{inicial_membresia}"



if __name__ == "__main__":
    crear_tabla()
    nuevo = agregar_cliente("CC001", "Carlos", "Colon", "44217249863", "Basica")