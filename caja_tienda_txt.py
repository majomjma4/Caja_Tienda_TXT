
import os
from datetime import datetime

CATALOGO_FILE = 'catalogo.txt'
VENTAS_FILE = 'ventas.txt'

catalogo, carrito = [], []

def leer_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        open(nombre_archivo, ' w').close()
    with open(nombre_archivo, 'r', encoding = 'utf-8') as f:
        return f.readlines()
def escribir_archivo(nombre_archivo, lineas, modo ='w'):
    with open(nombre_archivo, modo, encoding='utf-8') as f:
        f.writelines(lineas)

def cargar_catalogo():
    catalogo.clear()
    lineas = leer_archivo(CATALOGO_FILE)
    for linea in lineas:
        partes = linea.strip().split(",")
        if len(partes) == 4:
            codigo, nombre, precio, stock = linea.strip().split(",") 
            catalogo.append({
                'codigo': codigo.strip().upper(),
                'nombre': nombre.strip(),
                'precio': float(precio.strip()),
                'stock': int(stock.strip())
            })

def guardar_catalogo():
    lineas = [f"{product['codigo']}, {product['nombre']}, {product['precio']}, {product['stock']}\n" for product in catalogo]
    escribir_archivo(CATALOGO_FILE, lineas)
            
def ver_catalogo():
        if not catalogo: print("Catálogo vació. "); return
        
        print("\n------ CATÁLOGO ------")
        for product in catalogo:
            print(f"{product['codigo']} | {product['nombre']} | ${product['precio']:.2f} | {product['stock']} ")
      
def agregar_producto():
    codigo = input("Ingrese el código del producto: ").strip().upper()
    if any(product['codigo'] == codigo for product in catalogo):
        print("Ese código ya existe. "); return
    nombre = input("Ingrese el nombre del producto: ")
    
    try:
        precio = float(input("Ingrese el precio del producto: "))
        stock = int(input("Ingrese la cantidad de producto en stock: "))
        
    except ValueError:
        print("Datos inválidos. "); return
    catalogo.append({'codigo': codigo,'nombre': nombre, 'precio': precio, 'stock': stock })
    guardar_catalogo()
    print(f"Producto {nombre} agregado al catálogo. ")
        
    
def registrar_venta(ticket_texto):
    with open ('ventas.txt', 'a') as archivo_venta:
        archivo_venta.write(ticket_texto + '\n' + ' = ' * 40 + '\n')        

def agregar_carrito():
    codigo = input("Ingrese el código del producto que desea agregar al carrito: ").strip().upper()
    producto = next((product for product in catalogo if product['codigo'] == codigo), None)
    if not producto:
        print("Producto no encontrado")
        return
    try:
        cantidad = int(input("Ingrese la cantidad a comprar: "))
    except ValueError:
        print("Cantidad inválida")
        return
    if cantidad <= 0:
        print("La cantidad deber ser mayor a o")
        return
    if cantidad > producto['stock']:
        print(f"Stock insuficiente, disponible: {producto['stock']}")
        return
    
    carrito.append({'codigo': producto['codigo'], 'nombre': producto['nombre'], 'precio': producto['precio'], 'cantidad': cantidad})
    producto['stock'] -= cantidad
     
    with open('carrito.txt', 'a') as archivo_carrito:
        archivo_carrito.write(f"{producto['codigo']}, {producto['nombre']},{producto['precio']}, {cantidad}\n")
        
        print(f"{cantidad} unidades de {producto['nombre']} ha sido agregado al carrito")
        
def ver_carrito():
    if os.path.exists("carrito.txt"):
        with open("carrito.txt", "r") as archivo_carrito:
            lineas = archivo_carrito.readlines()
        carrito.clear()
        
        for linea in lineas:
            if "x" in linea or "Total" in linea or "---" in linea:
                continue
            partes = linea.strip().split(",")
            if len(partes) == 4:
                    codigo, nombre, precio, cantidad = partes
                    carrito.append({
                        'codigo': codigo.strip(),
                        'nombre': nombre.strip(),
                        'precio': float(precio.strip()),
                        'cantidad': int(cantidad.strip())
                    })
                
    if not carrito:
        print("Carrito vacío")
        return
    total = 0
    print("\n--- CARRITO DE COMPRAS --- ")
    for car in carrito:
        subtotal = car['precio'] * car['cantidad']
        total += subtotal
        print(f"{car['nombre']} x {car['cantidad']} = ${subtotal:.2f}")
    print(f"Total: ${total:.2f}")

def finalizar_compra():
    if not carrito:
        print("Carrito vacío")
        return
    confirm = input("Desea finalizar la compra (si/no): ").strip().lower()
    if confirm != 'si':
        print("Compra cancelada")
        return
   
    total = sum(car['precio'] * car['cantidad'] for car in carrito)
    descuento = 0.10 if total > 50 else 0.05 if total > 20 else 0
    total_desc = total * (1-descuento)
    iva = total_desc*0.15
    total_final = total_desc + iva
    ticket = f"FACTURA \nFecha {datetime.now()}\n " + "-" * 40 + "\n"
    
    for car in carrito:
        ticket += f"{car['nombre']} x {car['cantidad']} = ${car['precio']} * {car['cantidad']:.2f}\n"
    ticket += f"Total sin descuento: ${total:.2f}\n"
    
    if descuento > 0:
        ticket += f"Descuento: {int(descuento*100)}% | Total con descuento: ${total_desc:.2f}\n"
    ticket += f"IVA 15%: ${iva:.2f}\n Total a Pagar: ${total_final:.2f}"
    print("\n--- FACTURA ---")
    print(ticket)
    
    registrar_venta(ticket)
    guardar_catalogo()
    carrito.clear()
    with open("carrito.txt", "w") as archivo_carrito:
        archivo_carrito.write("")
    
def ver_ventas():
    if not os.path.exists('ventas.txt'):
        print("No hay ventas registradas")
        return
    
    with open('ventas.txt', 'r') as factu:
        ventas_todas = factu.read()
        
    opcion = input("Desea ver todas las ventas o buscar una venta especifica? (todas/buscar): ").strip().lower()
    if opcion == "todas":
        print(ventas_todas)
    elif opcion == "buscar":
        search = input("Ingrese la palabra clave para buscar (producto o fecha): ").strip().lower()
        ventas_filtradas = []
        for bloque in ventas_todas.split("="*40):
            if search in bloque.lower():
                ventas_filtradas.append(bloque)
        if ventas_filtradas:
            print("\n--- Ventas encontradas ---")
            print("\n".join(ventas_filtradas))
        else:
            print("No se encontraron ventas con esa palabra clave. ")
    else:
        print("Opción inválida")
    
if __name__=="__main__":
    cargar_catalogo()
    while True:
        print("""
    \nEscoja una opción:
    1. Ver catálogo
    2. Agregar al carrito
    3. Ver carrito
    4. Finalizar compra
    5. Ver ventas
    6. Agregar Producto 
    0. Salir
    \n""")
        opcion = input("\nIngrese la opción: ")
        if opcion == "1": ver_catalogo()
        elif opcion == "2": agregar_carrito()
        elif opcion == "3": ver_carrito()
        elif opcion == "4": finalizar_compra()
        elif opcion == "5": ver_ventas()
        elif opcion == "6": agregar_producto()
        elif opcion == "0": print("¡Gracias por preferirnos, Hasta luego!")
        else: print("Opción inválida")