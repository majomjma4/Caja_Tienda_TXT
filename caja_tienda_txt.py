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
    