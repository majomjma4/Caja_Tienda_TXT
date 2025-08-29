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


