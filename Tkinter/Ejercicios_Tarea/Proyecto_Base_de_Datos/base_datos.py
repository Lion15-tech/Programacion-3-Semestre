import sqlite3 #TTK

conexion = sqlite3.connect("GYM.db")

cursor = conexion.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS clientes(ID INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, apellido TEXT, telefono TEXT)')
conexion.commit()

conexion.close()