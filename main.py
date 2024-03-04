import modelo
import vista
import controlador


def main():
    # Crear objetos
    modelo_productos = modelo.ModeloProductos()
    controlador_productos = controlador.ControladorProductos()
    vista_productos = vista.VistaProductos(controlador_productos)

    # Loop principal
    vista_productos.ventana.mainloop()


if __name__ == '__main__':
    main()
