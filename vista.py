import tkinter as tk
import random
import string
from tkinter import ttk, messagebox


class VistaProductos:
    def __init__(self, controlador):
        self.fila_seleccionada = None
        self.ultima_columna_ordenada = None
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title('ABM de Productos')
        self.crear_widgets()

    def crear_widgets(self):
        # Crear un marco para los campos de entrada
        input_frame = tk.Frame(self.ventana)
        input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Etiquetas
        tk.Label(input_frame, text='Artículo:').grid(row=0, column=0, padx=5, pady=5)
        tk.Label(input_frame, text='Producto:').grid(row=1, column=0, padx=5, pady=5)
        tk.Label(input_frame, text='Talle:').grid(row=2, column=0, padx=5, pady=5)
        tk.Label(input_frame, text='Unidades:').grid(row=3, column=0, padx=5, pady=5)
        tk.Label(input_frame, text='Precio:').grid(row=4, column=0, padx=5, pady=5)

        # Entradas
        self.entrada_art = tk.Entry(input_frame, width=20)
        self.entrada_art.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_producto = tk.Entry(input_frame, width=20)
        self.entrada_producto.grid(row=1, column=1, padx=5, pady=5)
        self.entrada_talle = tk.Entry(input_frame, width=20)
        self.entrada_talle.grid(row=2, column=1, padx=5, pady=5)
        self.entrada_unidades = tk.Entry(input_frame, width=20)
        self.entrada_unidades.grid(row=3, column=1, padx=5, pady=5)
        self.entrada_precio = tk.Entry(input_frame, width=20)
        self.entrada_precio.grid(row=4, column=1, padx=5, pady=5)

        # Botones
        tk.Button(input_frame, text='Agregar', background="Wheat1",
                  command=self.agregar_producto).grid(row=5, column=0, padx=5, pady=5)
        tk.Button(input_frame, text='Actualizar', background="Wheat1",
                  command=self.actualizar_producto).grid(row=5, column=1, padx=5, pady=5)
        tk.Button(input_frame, text='Eliminar', background="IndianRed1",
                  command=self.eliminar_producto).grid(row=5, column=2, padx=5, pady=5)
        tk.Button(input_frame, text='Generar datos aleatorios', background="Green",
                  command=lambda: self.generar_datos_aleatorios(10)).grid(row=6, column=0, padx=5, pady=5)

        # Lista de productos
        self.tree = ttk.Treeview(self.ventana, columns=('id', 'articulo', 'producto', 'talle', 'unidades', 'precio'),
                                 show="headings")
        self.tree.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Ajustar las columnas
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('articulo', width=100, anchor='center')
        self.tree.column('producto', width=150, anchor='center')
        self.tree.column('talle', width=80, anchor='center')
        self.tree.column('unidades', width=100, anchor='center')
        self.tree.column('precio', width=100, anchor='center')

        # Encabezados de columna
        self.tree.heading('id', text='ID')
        self.tree.heading('id', command=lambda: self.ordenar_columna('id'))
        self.tree.heading('articulo', text='Artículo')
        self.tree.heading('articulo', command=lambda: self.ordenar_columna('articulo'))
        self.tree.heading('producto', text='Producto')
        self.tree.heading('producto', command=lambda: self.ordenar_columna('producto'))
        self.tree.heading('talle', text='Talle')
        self.tree.heading('unidades', text='Unidades')
        self.tree.heading('precio', text='Precio')

        # Agregar una barra de desplazamiento para la tabla
        scrollbar = tk.Scrollbar(self.ventana, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=1, column=1, padx=5, pady=5, sticky="ns")

        # Alinear la tabla y la barra de desplazamiento
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Entradas para buscar productos
        buscar_frame = tk.Frame(self.ventana)
        buscar_frame.grid(row=2, column=0, padx=2, pady=2)

        self.entrada_busqueda = tk.Entry(buscar_frame, width=100)
        self.entrada_busqueda.grid(row=0, column=0, padx=5, pady=5)

        boton_buscar = tk.Button(buscar_frame, text='Buscar', background="Wheat1", command=self.buscar_productos)
        boton_buscar.grid(row=0, column=1, padx=5, pady=5)

        # Obtener todos los productos de la base de datos y agregarlos a la tabla
        productos = self.controlador.obtener_productos()
        for producto in productos:
            self.tree.insert('', 'end', text=producto[0],
                             values=(producto[0],producto[1], producto[2], producto[3], producto[4], producto[5]))

        # Seleccionar una fila al hacer clic en ella
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_producto)

        # Inicializar la fila seleccionada en None
        self.fila_seleccionada = None

    def generar_datos_aleatorios(self, num_filas=10):
        # Generar datos aleatorios
        datos = []
        for i in range(num_filas):
            id = i + 1
            art = f'art{id}'
            producto = random.choice(['Remera', 'Pantalon', 'Zapatillas'])
            talle = random.choice(['S', 'M', 'L', 'XL'])
            unidades = random.randint(20, 100)
            precio = round(random.uniform(20, 100), 2)
            datos.append((id, art, producto, talle, unidades, precio))
            self.controlador.agregar_producto( art, producto, talle, unidades, precio)  # insertar en la base
        # Insertar los datos en la tabla
        for dato in datos:
            self.tree.insert('', 'end', values=dato)

    def seleccionar_producto(self, event):
        try:
            # Obtener la fila seleccionada
            filas_seleccionadas = self.tree.selection()
            if filas_seleccionadas:
                fila_seleccionada = filas_seleccionadas[0]
                # Obtener los valores de la fila seleccionada
                valores_fila = self.tree.item(fila_seleccionada, 'values')
                # Actualizar los campos de entrada con los valores de la fila seleccionada
                self.entrada_art.delete(0, tk.END)
                self.entrada_art.insert(0, valores_fila[1])
                self.entrada_producto.delete(0, tk.END)
                self.entrada_producto.insert(0, valores_fila[2])
                self.entrada_talle.delete(0, tk.END)
                self.entrada_talle.insert(0, valores_fila[3])
                self.entrada_unidades.delete(0, tk.END)
                self.entrada_unidades.insert(0, valores_fila[4])
                self.entrada_precio.delete(0, tk.END)
                self.entrada_precio.insert(0, valores_fila[5])
                # Actualizar la fila seleccionada
                self.fila_seleccionada = fila_seleccionada
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar_productos(self):
        # Obtener la cadena de búsqueda ingresada por el usuario
        busqueda = self.entrada_busqueda.get()

        # Buscar los productos que coincidan con la cadena de búsqueda
        productos_encontrados = self.controlador.buscar_productos(busqueda)

        # Actualizar la tabla de productos con los productos encontrados
        self.tree.delete(*self.tree.get_children())
        for producto in productos_encontrados:
            self.tree.insert('', 'end', values=producto)

    def ordenar_columna(self, encabezado_columna):
        try:
            # Obtiene todas las filas de la tabla
            filas = [(self.tree.set(id_producto, encabezado_columna), id_producto) for id_producto in
                     self.tree.get_children('')]
            # Ordena las filas según el encabezado de la columna seleccionado
            filas.sort(reverse=False)
            for indice, (valor, id_producto) in enumerate(filas):
                self.tree.move(id_producto, '', indice)
            # Cambia la dirección de ordenamiento en caso de hacer clic en el mismo encabezado de columna
            if self.ultima_columna_ordenada == encabezado_columna:
                self.ordenamiento_ascendente = not self.ordenamiento_ascendente
            else:
                self.ordenamiento_ascendente = True
                self.ultima_columna_ordenada = encabezado_columna
            # Ordena las filas en orden descendente si se selecciona el encabezado de columna por segunda vez
            if not self.ordenamiento_ascendente:
                filas = reversed(filas)
            for indice, (valor, id_producto) in enumerate(filas):
                self.tree.move(id_producto, '', indice)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def obtener_valores_entrada(self):
        try:
            id_producto = self.fila_seleccionada
            art = self.entrada_art.get()
            producto = self.entrada_producto.get()
            talle = self.entrada_talle.get()
            unidades = self.entrada_unidades.get()
            precio = self.entrada_precio.get()
            return id_producto, art, producto, talle, unidades, precio
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_entradas(self):
        try:
            self.entrada_art.delete(0, tk.END)
            self.entrada_producto.delete(0, tk.END)
            self.entrada_talle.delete(0, tk.END)
            self.entrada_unidades.delete(0, tk.END)
            self.entrada_precio.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def agregar_producto(self):
        try:
            # Obtener los valores ingresados por el usuario
            valores = self.obtener_valores_entrada()
            # Agregar el nuevo producto a la base de datos
            self.controlador.agregar_producto(*valores)
            # Actualizar la tabla de productos
            self.actualizar_lista_productos()
            # Limpiar las entradas del formulario
            self.limpiar_entradas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_producto(self):
        try:
            # Obtener los valores ingresados por el usuario
            valores = self.obtener_valores_entrada()

            if self.fila_seleccionada:
                # Actualizar el producto seleccionado en la base de datos
                id_producto = self.tree.item(self.fila_seleccionada, 'values')[0]
                self.controlador.actualizar_producto(id_producto, *valores[1:])
                # Actualizar la tabla de productos
                self.tree.item(self.fila_seleccionada, values=(id_producto, *valores[1:]))
                # Limpiar las entradas del formulario
                self.limpiar_entradas()
                # Limpiar la fila seleccionada
                self.fila_seleccionada = None
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_producto(self):
        try:
            if self.fila_seleccionada:
                # Obtener el ID del producto seleccionado
                id_producto = self.tree.item(self.fila_seleccionada, 'text')
                # Confirmar con el usuario si desea eliminar el producto
                confirmacion = messagebox.askyesno("Eliminar producto",
                                                   f"¿Está seguro que desea eliminar el producto con ID {id_producto}?")
                if confirmacion:
                    # Eliminar el producto de la base de datos
                    self.controlador.eliminar_producto(id_producto)
                    # Actualizar la tabla de productos
                    self.actualizar_lista_productos()
                    # Limpiar las entradas del formulario
                    self.limpiar_entradas()
                    # Limpiar la fila seleccionada
                    self.fila_seleccionada = None
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista_productos(self):
        try:
            # Limpiar la tabla de productos
            self.tree.delete(*self.tree.get_children())
            # Obtener todos los productos de la base de datos
            productos = self.controlador.obtener_productos()
            # Insertar los productos en la tabla
            for producto in productos:
                self.tree.insert('', 'end', text=producto[0],
                                 values=(producto[0], producto[1], producto[2], producto[3], producto[4], producto[5]))
        except Exception as e:
            messagebox.showerror("Error", str(e))