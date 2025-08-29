import os
from datetime import datetime

catalogo = []
carrito = []

def cargar_catalogo():
    if not os.path.exists('catalogo.txt'):
        with open('catalogo.txt', 'w') as f:
            f.write("P001,Azucar,2.50,100\n")
            f.write("P002,Sal,1.00,100\n")
            f.write("P003,Atun,1.65,100\n")
            f.write("P004,Fideos,0.75,100\n")
            f.write("P005,Cola,1.00,100\n")
            f.write("P006,Jugo,0.50,100\n")
    catalogo.clear()
    
    with open('catalogo.txt', 'r') as archivo_catalogo:
        for linea in archivo_catalogo:
            partes = linea.strip().split(',')
            if len(partes) != 4:
                continue
            codigo, nombre, precio, stock = partes 
            catalogo.append({
                'codigo': codigo.strip().upper(),
                'nombre': nombre.strip().strip(),
                'precio': float(precio),
                'stock': int(stock)
            })
            
def guardar_catalogo():
    with open('catalogo.txt', 'w') as archivo_catalogo:
        for product in catalogo:
            archivo_catalogo.write(f"{product['codigo']}, {product['nombre']}, {product['precio']}, {product['stock']}\n")
    
def registrar_venta(ticket_texto):
    with open ('ventas.txt', 'a') as archivo_venta:
        archivo_venta.write(ticket_texto + '\n' + ' = ' * 40 + '\n')


def ver_catalogo():
    print("\n--- CATÁLOGO ---")
    for product in catalogo:
        print(f"{product['codigo']} | {product['nombre']} | {product['precio']} | {product['stock']} ")

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
    print(f"{cantidad} unidades de {producto['nombre']} ha sido agregado al carrito")
    
def ver_carrito():
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
    confirm = input("Desea finalizar la compra (si/no): ").strip.lower()
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
    0. Salir
    \n""")
        opcion = input("\nIngrese la opción: ")
        match opcion:
            case '1':
                ver_catalogo()
            case '2':
                agregar_carrito()
            case '3':
                ver_carrito()
            case '4':
                finalizar_compra()
            case '5':
                ver_ventas()
            case '0':
                print("\n ¡Gracias por su compra! Hasta luego. \n")
                carrito.clear()
                os.system('cls' if os.name == 'nt' else 'clear')
     
                continue
            case _:
                print("Opción inválida")
            