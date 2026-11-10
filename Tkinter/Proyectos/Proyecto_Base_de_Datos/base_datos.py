import sqlite3

DATABASE = "GYM.db"

def conectar():
    return sqlite3.connect(DATABASE)

def crear_tabla():
    with conectar() as conect:
        conect.execute("""CREATE TABLE IF NOT EXISTS clientes(
            ID TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            tipo_membresia TEXT NOT NULL,
            fecha_nacimiento TEXT NOT NULL)""")

def generar_id(nombre, apellido, tipo_membresia, fecha_nacimiento):
    if not nombre or not apellido or not tipo_membresia or not fecha_nacimiento:
        raise ValueError("Todos los campos son obligatorios")

    inicial_apellido  = apellido.strip()[0].upper()
    inicial_nombre  = nombre.strip()[0].upper()
    inicial_membresia = tipo_membresia.strip()[0].upper()
    fecha_limpia = fecha_nacimiento.strip().replace("/", "").replace("-", "").replace("_","")

    if len(fecha_limpia) != 8 or not fecha_limpia.isdigit():
        raise ValueError("La fecha debe tener formato DDMMAAAA")

    return f"{inicial_apellido}{inicial_nombre}{inicial_membresia}{fecha_limpia}"

def agregar_cliente(nombre, apellido, telefono, tipo_membresia, fecha_nacimiento):
    fecha_limpia = fecha_nacimiento.strip().replace("/", "").replace("-", "").replace("_", "")
    nuevo_id = generar_id(nombre, apellido, tipo_membresia, fecha_limpia)
    try:
        with conectar() as conect:
            conect.execute(
                "INSERT INTO clientes (ID, nombre, apellido, telefono, tipo_membresia, fecha_nacimiento) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (nuevo_id, nombre, apellido, telefono, tipo_membresia, fecha_limpia))
    except sqlite3.IntegrityError:
        raise ValueError(f"El ID {nuevo_id} ya existe. Cambia algún dato del cliente.")
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

    actu = ", ".join(f"{columna} = ?" for columna in valores.keys())
    meter_valor = list(valores.values()) + [ID]
    actu_cliente = f"UPDATE clientes SET {actu} WHERE ID = ?"

    with conectar() as conect:
        cursor = conect.execute(actu_cliente, meter_valor)
        return cursor.rowcount > 0

def eliminar_cliente(ID):
    with conectar() as conect:
        cur = conect.execute("DELETE FROM clientes WHERE ID = ?", (ID,))
        return cur.rowcount > 0

def ver_clientes():
    with conectar() as conect:
        return conect.execute("SELECT * FROM clientes").fetchall()


if __name__ == "__main__":
    crear_tabla()
    nuevo = agregar_cliente("Carlos", "Colon", "44217249863", "Basica", "10112026")