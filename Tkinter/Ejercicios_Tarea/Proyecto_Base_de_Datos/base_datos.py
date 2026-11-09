import sqlite3 #TTK

DB = "GYM.db"

def conectar():
    return sqlite3.connect(DB)

def crear_tabla():
    with conectar() as con:
        con.execute('''CREATE TABLE IF NOT EXISTS clientes(
        ID TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        telefono TEXT NOT NULL) ''')    

def agregar_cliente(ID,nombre,apellido,telefono):
    with conectar() as con:
        con.execute(
            'INSERT INTO clientes (ID,nombre,apellido,telefono) VALUES (?,?,?,?)',
        (ID,nombre,apellido,telefono))
        return ID

if __name__ == "__main__":
    crear_tabla()
    nuevo = agregar_cliente("CC001", "Carlos", "Colon", "44217249863")