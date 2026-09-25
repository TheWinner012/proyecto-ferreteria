# ==========================================
# Sistema de Inventario y Ventas - Ferretería
# ==========================================

# Estructura principal para almacenar los productos en memoria
# Se utiliza un diccionario donde la clave es el nombre del producto
inventario_productos = {}

# Lista para registrar el historial de ventas durante la sesión
# Cada venta se guarda como tupla: (nombre_producto, cantidad, precio_unitario, total)
registro_ventas_dia = []


def mostrar_menu_principal():
    # RF1: Muestra el menu 
    print("\n--- SISTEMA DE INVENTARIO Y VENTAS ---")
    print("1. Agregar producto")
    print("2. Consultar inventario")
    print("3. Buscar producto")
    print("4. Vender producto")
    print("5. Reporte de stock bajo")
    print("6. Ver ventas del día")
    print("7. Ver total vendido en el día")
    print("8. Salir")


def agregar_producto_nuevo():
    # RF2: Registra productos nuevos
    print("\n--- AGREGAR NUEVO PRODUCTO ---")
    
    # Solicita el nombre del producto
    nombre_producto = input("Ingrese el nombre del producto: ")
    
    # Valida si el producto ya existe para evitar duplicados en el inventario
    if nombre_producto in inventario_productos:
        print(f"Error: El producto '{nombre_producto}' ya existe en el inventario.")
        return

    try:
        # Solicita el precio convirtiéndolo a tipo de dato decimal (float)
        precio_producto = float(input("Ingrese el precio del producto: "))
        
        # Regla de negocio: El precio siempre debe ser mayor a 0
        if precio_producto <= 0:
            print("Error: El precio del producto debe ser mayor a 0.")
            return

        # Solicita la cantidad inicial en stock (entero mayor o igual a 0)
        cantidad_stock = int(input("Ingrese la cantidad inicial en stock: "))
        if cantidad_stock < 0:
            print("Error: La cantidad en stock no puede ser negativa.")
            return

        # Almacena el producto dentro del diccionario principal
        inventario_productos[nombre_producto] = {
            "precio": precio_producto,
            "stock": cantidad_stock
        }
        
        # Muestra el mensaje de confirmación con los datos del producto
        print(f"¡Éxito! Producto agregado: {nombre_producto} | Precio: ${precio_producto:.2f} | Stock: {cantidad_stock}")

    except ValueError:
        # Controla errores si el usuario ingresa letras en lugar de números
        print("Error: Ingrese valores numéricos válidos para el precio y el stock.")


def consultar_inventario_completo():
    # RF3: Muestra todo el inventario
    print("\n--- INVENTARIO COMPLETO ---")
    
    # Verifica si el inventario está vacío
    if not inventario_productos:
        print("El inventario actual está vacío.")
        return

    # Imprime los encabezados para organizar los datos visualmente
    print(f"{'Producto':<25} | {'Precio':<10} | {'Stock':<10}")
    print("-" * 50)
    
    # Recorre cada elemento del diccionario para mostrar sus detalles
    for nombre_item, datos_item in inventario_productos.items():
        precio_item = datos_item["precio"]
        stock_item = datos_item["stock"]
        print(f"{nombre_item:<25} | ${precio_item:<9.2f} | {stock_item:<10}")


def ver_ventas_dia():
    # RF7: Ver ventas del día
    # Entrada: ninguna (usa la lista global registro_ventas_dia)
    # Proceso: recorre el registro de ventas de la sesión y las muestra en orden
    # Salida: listado de ventas, o mensaje si aún no hay ninguna
    print("\n--- VENTAS DEL DÍA ---")

    # Si la lista de ventas está vacía, se avisa al usuario y se sale de la función
    if not registro_ventas_dia:
        print("Aún no se ha registrado ninguna venta en esta sesión.")
        return

    # Encabezados para mostrar la información de forma ordenada
    print(f"{'Producto':<25} | {'Cantidad':<10} | {'Precio unit.':<12} | {'Total':<10}")
    print("-" * 65)

    # Ciclo for que recorre cada venta registrada durante la sesión
    for venta_registrada in registro_ventas_dia:
        # Cada venta es una tupla: (nombre, cantidad, precio_unitario, total)
        nombre_producto = venta_registrada[0]
        cantidad_vendida = venta_registrada[1]
        precio_unitario = venta_registrada[2]
        total_venta = venta_registrada[3]

        print(f"{nombre_producto:<25} | {cantidad_vendida:<10} | ${precio_unitario:<11.2f} | ${total_venta:<9.2f}")


def calcular_total_vendido_dia():
    # RF8: Total vendido en el día (función CON retorno)
    # Entrada: ninguna (usa la lista global registro_ventas_dia)
    # Proceso: suma el total de todas las ventas registradas en la sesión
    # Salida: regresa un número decimal con el total acumulado
    total_acumulado = 0.0  # Variable donde se va acumulando la suma de ventas

    # Se recorre la lista de ventas sumando el total de cada una
    for venta_registrada in registro_ventas_dia:
        total_venta = venta_registrada[3]  # Posición 3 de la tupla = total de esa venta
        total_acumulado = total_acumulado + total_venta  # Se acumula al total general

    return total_acumulado  # La función regresa el valor calculado, no solo lo imprime


def mostrar_total_vendido_dia():
    # Función auxiliar que llama a calcular_total_vendido_dia() y muestra el resultado
    # Separa el cálculo (con retorno) de la presentación en pantalla
    total_del_dia = calcular_total_vendido_dia()  # Se guarda el valor que regresa la función
    print(f"\nTotal vendido en el día: ${total_del_dia:,.2f}")


def ejecutar_programa():
    # RF1: Controla la repetición continua del menú hasta que el usuario elija Salir
    opcion_seleccionada = ""
    
    # Ciclo que mantiene vivo el programa mientras la opción no sea "8"
    while opcion_seleccionada != "8":
        mostrar_menu_principal()
        opcion_seleccionada = input("Seleccione una opción (1-8): ").strip()

        # Evaluación de la opción ingresada por el usuario
        if opcion_seleccionada == "1":
            agregar_producto_nuevo()
        elif opcion_seleccionada == "2":
            consultar_inventario_completo()
        elif opcion_seleccionada == "3":
            print("Función 'Buscar producto' pendiente de implementar (RF5).")
        elif opcion_seleccionada == "4":
            print("Función 'Vender producto' pendiente de implementar (RF4).")
        elif opcion_seleccionada == "5":
            print("Función 'Reporte de stock bajo' pendiente de implementar (RF6).")
        elif opcion_seleccionada == "6":
            ver_ventas_dia()
        elif opcion_seleccionada == "7":
            mostrar_total_vendido_dia()
        elif opcion_seleccionada == "8":
            # Mensaje de cierre del programa
            print("Saliendo del programa...")
        else:
            # Mensaje en caso de que la opción ingresada no sea válida
            print("Opción no válida. Por favor, ingrese un número del 1 al 8.")


# Punto de inicio para la ejecución del código
if __name__ == "__main__":
    ejecutar_programa()
