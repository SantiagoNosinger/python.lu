import sqlite3
import re


class ModeloProductos:
    def __init__(self):
        self.conexion = sqlite3.connect('productos.db')
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        sql = "CREATE TABLE IF NOT EXISTS indumentaria (id integer PRIMARY KEY AUTOINCREMENT, art VARCHAR(12)," \
              " producto VARCHAR(12), talle VARCHAR(12), unidades VARCHAR(12), precio VARCHAR(12))"
        self.cursor.execute(sql)
        self.conexion.commit()

    def agregar_producto(self, art, producto, talle, unidades, precio):
        patron = "^[A-Za-z0-9]+$"
        if not re.match(patron, art):
            raise ValueError("El código de artículo debe contener solo caracteres alfanuméricos")
        sql = "INSERT INTO indumentaria (art, producto, talle, unidades, precio) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (art, producto, talle, unidades, precio))
        self.conexion.commit()

    def actualizar_producto(self, id, art, producto, talle, unidades, precio):
        patron = "^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$"
        if not re.match(patron, art):
            raise ValueError(
                "El código de artículo no es válido. Debe contener solo caracteres alfanuméricos y opcionalmente "
                "espacios, guiones o guiones bajos.")
        sql = "UPDATE indumentaria SET art=?, producto=?, talle=?, unidades=?, precio=? WHERE id=?"
        self.cursor.execute(sql, (art, producto, talle, unidades, precio, id))
        self.conexion.commit()

    def eliminar_producto(self, id):
        sql = "DELETE FROM indumentaria WHERE id=?"
        self.cursor.execute(sql, (id,))
        self.conexion.commit()

    def obtener_productos(self):
        sql = "SELECT * FROM indumentaria"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def obtener_producto_por_id(self, id):
        sql = "SELECT * FROM indumentaria WHERE id=?"
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()

    def buscar_productos(self, busqueda):
        sql = "SELECT * FROM indumentaria WHERE art LIKE ? OR producto LIKE ?"
        busqueda = f"%{busqueda}%"
        self.cursor.execute(sql, (busqueda, busqueda))
        return self.cursor.fetchall()
