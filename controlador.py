import modelo

#se crea el controlador
class ControladorProductos:
    def __init__(self):
        self.modelo = modelo.ModeloProductos()

    def agregar_producto(self, art, producto, talle, unidades, precio):
        self.modelo.agregar_producto(art, producto, talle, unidades, precio)
    def obtener_productos(self):
        return self.modelo.obtener_productos()

    def actualizar_producto(self, id_producto, art, producto, talle, unidades, precio):
        self.modelo.actualizar_producto(id_producto, art, producto, talle, unidades, precio)

    def eliminar_producto(self, id_producto):
        self.modelo.eliminar_producto(id_producto)

    def obtener_producto(self,id_producto):
        self.modelo.obtener_producto_por_id(id_producto)

    def buscar_productos(self, busqueda):
        return self.modelo.buscar_productos(busqueda)
    
