# ==========================================
# Sistema de Inventario y Ventas - Ferretería
# ==========================================

# Estructura principal para almacenar los productos en memoria
# Se utiliza un diccionario donde la clave es el nombre del producto
inventario_productos = {}

# Lista para registrar el historial de ventas durante la sesión
# Cada venta se guarda como tupla: (nombre_producto, cantidad, precio_unitario, total)
registro_ventas_dia = []

# Umbral de stock bajo (RF6): por debajo o igual a este valor se considera bajo
UMBRAL_STOCK_BAJO = 5

# Nombre del archivo donde se guarda y se recupera el inventario (RF9 y RF10)
ARCHIVO_INVENTARIO = "inventario_datos.txt"


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


def buscar_nombre_real_producto(nombre_ingresado):
    # Función auxiliar: encuentra el nombre EXACTO como está guardado en el inventario,
    # comparando sin importar si el usuario escribió mayúsculas o minúsculas.
    # Se usa tanto al agregar (para detectar duplicados) como al vender un producto.
    # Entrada: nombre_ingresado -> texto que escribió el usuario
    # Salida: regresa el nombre tal como está guardado (para usarlo como llave del
    # diccionario), o None si no se encontró ningún producto que coincida.
    nombre_ingresado_normalizado = nombre_ingresado.strip().lower()

    # Se recorre cada nombre guardado en el inventario para comparar sin distinguir mayúsculas
    for nombre_guardado in inventario_productos:
        if nombre_guardado.lower() == nombre_ingresado_normalizado:
            return nombre_guardado  # Se regresa el nombre real, tal como está guardado

    return None  # No se encontró ningún producto con ese nombre


def agregar_producto_nuevo():
    # RF2: Registra productos nuevos
    print("\n--- AGREGAR NUEVO PRODUCTO ---")

    # Solicita el nombre del producto y quita espacios sobrantes al inicio/final
    # (evita que "Martillo" y "Martillo " con espacio se traten como productos distintos)
    nombre_producto = input("Ingrese el nombre del producto: ").strip()

    # Valida que el usuario no haya dejado el nombre vacío
    if nombre_producto == "":
        print("Error: El nombre del producto no puede estar vacío.")
        return

    # Valida si el producto ya existe, sin importar mayúsculas/minúsculas,
    # usando la misma función que usa vender_producto()
    nombre_ya_existente = buscar_nombre_real_producto(nombre_producto)
    if nombre_ya_existente is not None:
        print(f"Error: El producto '{nombre_ya_existente}' ya existe en el inventario.")
        return
    # Valida que el nombre solo contenga letras (se permiten espacios entre palabras)
    elif not nombre_producto.replace(" ", "").isalpha():
        print("Error: El nombre del producto solo debe contener letras, sin números ni símbolos.")
        return

    try:
        # Solicita el precio como texto primero, para poder limpiarlo antes de convertirlo
        precio_texto = input("Ingrese el precio del producto: ")

        # Se quitan el símbolo $ y las comas de miles (por si el usuario escribe $1,500)
        # para que la conversión a número no truene por caracteres no numéricos
        precio_texto_limpio = precio_texto.replace("$", "").replace(",", "").strip()

        # Convierte el texto ya limpio a tipo de dato decimal (float)
        precio_producto = float(precio_texto_limpio)
        
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


def vender_producto():
    # RF4: Registra la venta de un producto y descuenta del stock
    print("\n--- VENDER PRODUCTO ---")

    # Verifica si el inventario está vacío antes de intentar vender
    if not inventario_productos:
        print("No se puede vender: el inventario actual está vacío.")
        return

    # Solicita el nombre del producto a vender
    nombre_ingresado = input("Ingrese el nombre del producto a vender: ")

    # Busca el nombre real del producto sin importar mayúsculas/minúsculas
    nombre_producto = buscar_nombre_real_producto(nombre_ingresado)

    # Valida que el producto exista en el inventario
    if nombre_producto is None:
        print(f"Error: El producto '{nombre_ingresado}' no existe en el inventario.")
        return

    try:
        # Solicita la cantidad a vender
        cantidad_vendida = int(input("Ingrese la cantidad a vender: "))

        # Regla de negocio: la cantidad vendida debe ser mayor a 0
        if cantidad_vendida <= 0:
            print("Error: La cantidad a vender debe ser mayor a 0.")
            return

        stock_disponible = inventario_productos[nombre_producto]["stock"]

        # Valida que haya stock suficiente para cubrir la venta
        if cantidad_vendida > stock_disponible:
            print(f"Error: Stock insuficiente. Stock disponible: {stock_disponible}.")
            return

        # Calcula el subtotal de la venta usando el precio unitario del producto
        precio_unitario = inventario_productos[nombre_producto]["precio"]
        subtotal_venta = precio_unitario * cantidad_vendida

        # Descuenta la cantidad vendida del stock actual
        inventario_productos[nombre_producto]["stock"] -= cantidad_vendida

        # Registra la venta en el historial del día como tupla:
        # (nombre_producto, cantidad, precio_unitario, total) — mismo formato que usan
        # ver_ventas_dia() y calcular_total_vendido_dia()
        registro_ventas_dia.append((nombre_producto, cantidad_vendida, precio_unitario, subtotal_venta))

        # Muestra el mensaje de confirmación con los datos de la venta
        print(f"¡Venta registrada! {cantidad_vendida} x {nombre_producto} = ${subtotal_venta:.2f}")
        print(f"Stock restante de '{nombre_producto}': {inventario_productos[nombre_producto]['stock']}")

    except ValueError:
        # Controla errores si el usuario ingresa un valor no numérico
        print("Error: Ingrese un valor numérico válido para la cantidad.")


def buscar_producto():
    # RF5: Busca un producto específico por nombre (coincidencia exacta o parcial)
    print("\n--- BUSCAR PRODUCTO ---")

    if not inventario_productos:
        print("El inventario actual está vacío.")
        return

    texto_busqueda = input("Ingrese el nombre (o parte del nombre) del producto: ").strip().lower()

    if texto_busqueda == "":
        print("Error: Debe ingresar un texto de búsqueda.")
        return

    # Filtra los productos cuyo nombre contenga el texto ingresado, usando un for
    # normal en lugar de comprensión de diccionario (ya es insensible a mayúsculas
    # porque ambos lados usan .lower())
    resultados_encontrados = {}
    for nombre_item, datos_item in inventario_productos.items():
        if texto_busqueda in nombre_item.lower():
            resultados_encontrados[nombre_item] = datos_item

    if not resultados_encontrados:
        print(f"No se encontraron productos que coincidan con '{texto_busqueda}'.")
        return

    # Muestra los resultados encontrados con el mismo formato que el inventario completo
    print(f"\n{'Producto':<25} | {'Precio':<10} | {'Stock':<10}")
    print("-" * 50)
    for nombre_item, datos_item in resultados_encontrados.items():
        precio_item = datos_item["precio"]
        stock_item = datos_item["stock"]
        print(f"{nombre_item:<25} | ${precio_item:<9.2f} | {stock_item:<10}")


def reporte_stock_bajo():
    # RF6: Muestra los productos cuyo stock está en o por debajo del umbral definido
    print(f"\n--- REPORTE DE STOCK BAJO (umbral: {UMBRAL_STOCK_BAJO} unidades) ---")

    if not inventario_productos:
        print("El inventario actual está vacío.")
        return

    # Arma una lista con los productos de stock bajo, usando un for normal
    # en lugar de comprensión de diccionario
    productos_stock_bajo = []
    for nombre_item, datos_item in inventario_productos.items():
        if datos_item["stock"] <= UMBRAL_STOCK_BAJO:
            productos_stock_bajo.append((nombre_item, datos_item))

    if not productos_stock_bajo:
        print("No hay productos con stock bajo en este momento.")
        return

    # Ordena la lista de menor a mayor stock con un ordenamiento burbuja simple,
    # hecho con ciclos for (en vez de sorted() con lambda)
    cantidad_productos = len(productos_stock_bajo)
    for vuelta_actual in range(cantidad_productos):
        for posicion in range(cantidad_productos - 1 - vuelta_actual):
            stock_actual = productos_stock_bajo[posicion][1]["stock"]
            stock_siguiente = productos_stock_bajo[posicion + 1][1]["stock"]

            # Si el producto actual tiene más stock que el siguiente, se intercambian
            if stock_actual > stock_siguiente:
                producto_temporal = productos_stock_bajo[posicion]
                productos_stock_bajo[posicion] = productos_stock_bajo[posicion + 1]
                productos_stock_bajo[posicion + 1] = producto_temporal

    # Muestra los productos con stock bajo, ya ordenados de menor a mayor stock
    print(f"{'Producto':<25} | {'Precio':<10} | {'Stock':<10}")
    print("-" * 50)
    for nombre_item, datos_item in productos_stock_bajo:
        precio_item = datos_item["precio"]
        stock_item = datos_item["stock"]
        print(f"{nombre_item:<25} | ${precio_item:<9.2f} | {stock_item:<10} ⚠")


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

    # Encabezados 
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
    # RF8: Total vendido en el día función CON retorno
    # Entrada: ninguna (usa la lista global registro_ventas_dia)
    # Proceso: suma el total de todas las ventas registradas en la sesión
    # Salida: regresa un número decimal con el total acumulado
    total_acumulado = 0.0  # Variable donde se va acumulando la suma de ventas

    # Se recorre la lista de ventas sumando el total de cada una
    for venta_registrada in registro_ventas_dia:
        total_venta = venta_registrada[3]  # Posición 3 de la tupla = total de esa venta
        total_acumulado = total_acumulado + total_venta  # Se acumula al total general

    return total_acumulado


def mostrar_total_vendido_dia():
    # Función auxiliar que llama a calcular_total_vendido_dia() y muestra el resultado
    # Separa el cálculo (con retorno) de la presentación en pantalla
    total_del_dia = calcular_total_vendido_dia()  # Se guarda el valor que regresa la función
    print(f"\nTotal vendido en el día: ${total_del_dia:,.2f}")


def guardar_inventario_archivo():
    # RF9: Guarda el inventario actual en un archivo de texto antes de salir del programa
    try:
        # Se usa "with" para que el archivo se cierre automáticamente, incluso si
        # ocurre un error a la mitad de la escritura
        with open(ARCHIVO_INVENTARIO, "w") as archivo_salida:
            # Recorre cada producto del inventario y lo escribe como una línea de texto
            for nombre_item, datos_item in inventario_productos.items():
                # Separa cada dato con una coma para poder leerlo después fácilmente
                linea_producto = f"{nombre_item},{datos_item['precio']},{datos_item['stock']}\n"
                archivo_salida.write(linea_producto)

        print(f"Inventario guardado correctamente en '{ARCHIVO_INVENTARIO}'.")

    except Exception as error_al_guardar:
        # Controla cualquier problema al escribir el archivo (permisos, disco lleno, etc.)
        print(f"Error: No se pudo guardar el inventario. Detalle: {error_al_guardar}")


def cargar_inventario_archivo():
    # RF10: Carga el inventario guardado la última vez que se usó el programa, si existe
    try:
        # Se usa "with" para que el archivo se cierre automáticamente al terminar de leerlo
        with open(ARCHIVO_INVENTARIO, "r") as archivo_entrada:
            # Recorre cada línea del archivo, donde cada línea es un producto guardado
            for linea_actual in archivo_entrada:
                linea_limpia = linea_actual.strip()

                # Ignora líneas vacías (por ejemplo, la última línea del archivo)
                if linea_limpia == "":
                    continue

                # Se valida cada línea por separado: si una línea viene dañada,
                # se omite solo esa línea y se sigue leyendo el resto del archivo
                try:
                    # Separa la línea en sus tres partes: nombre, precio y stock
                    partes_linea = linea_limpia.split(",")
                    nombre_producto = partes_linea[0]
                    precio_producto = float(partes_linea[1])
                    cantidad_stock = int(partes_linea[2])

                    # Reconstruye el producto dentro del diccionario principal
                    inventario_productos[nombre_producto] = {
                        "precio": precio_producto,
                        "stock": cantidad_stock
                    }

                except (ValueError, IndexError):
                    # La línea no tiene el formato esperado (faltan datos o no son números)
                    print(f"Aviso: se omitió una línea con formato inválido: '{linea_limpia}'")
                    continue

        print(f"Inventario cargado: {len(inventario_productos)} producto(s) recuperado(s) de '{ARCHIVO_INVENTARIO}'.")

    except FileNotFoundError:
        # Es normal la primera vez que se ejecuta el programa: aún no existe un archivo guardado
        print("No se encontró un inventario guardado previamente. Se inicia con el inventario vacío.")

    except Exception as error_al_cargar:
        # Controla otros errores al abrir el archivo (permisos, archivo dañado, etc.)
        print(f"Error: No se pudo cargar el inventario. Detalle: {error_al_cargar}")


def ejecutar_programa():
    # RF1: Controla la repetición continua del menú hasta que el usuario elija Salir
    opcion_seleccionada = ""

    # RF10: Antes de mostrar el menú, se intenta recuperar el inventario guardado
    cargar_inventario_archivo()

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
            buscar_producto()
        elif opcion_seleccionada == "4":
            vender_producto()
        elif opcion_seleccionada == "5":
            reporte_stock_bajo()
        elif opcion_seleccionada == "6":
            ver_ventas_dia()
        elif opcion_seleccionada == "7":
            mostrar_total_vendido_dia()
        elif opcion_seleccionada == "8":
            # RF9: Se guarda el inventario 
            guardar_inventario_archivo()
            print("Saliendo del programa...")
        else:
            # Mensaje en caso de que la opción ingresada no sea válida
            print("Opción no válida. Por favor, ingrese un número del 1 al 8.")


# Punto de inicio para la ejecución del código
if __name__ == "__main__":
    ejecutar_programa()
