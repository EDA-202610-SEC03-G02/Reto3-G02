import sys
from unittest.mock import Base
from tabulate import tabulate
import App.logic as logic
from DataStructures.List import array_list as al



def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    opciones = ["test", "small", "medium", "large"]
    tamaño = input("Ingrese el tamaño de datos a cargar (test, small, medium, large): ").strip().lower()
    
    while tamaño not in opciones:
        print("Opción inválida. Por favor, ingrese una opción válida.")
        tamaño = input("Ingrese el tamaño de datos a cargar (test, small, medium, large): ").strip().lower()
        
    input_file = f"mercedes_sales_{tamaño}.csv"
    datos = logic.load_data(control, input_file)
    
    print(f"\nTiempo de carga: {datos['tiempo']} ms")
    print(f"Total de ventas cargadas: {datos['total']}")
    
    print(f"Primeros 5 carros en orden cronologico de venta:")
    primeros_5 = []
    for i in range(al.size(datos['primeros_5'])):
        carro = al.get_element(datos['primeros_5'], i)
        carro_info = {
            "Modelo": carro["Model"],
            "Año": carro["Year"],
            "Fuel Type": carro["Fuel Type"],
            "Color": carro["Color"],
            "Precio": carro["Base Price (USD)"],
            "Horsepower": carro["Horsepower"],
            "Turbo": carro["Turbo"]
        }
        primeros_5.append(carro_info)
    print(tabulate(primeros_5, headers="keys", tablefmt="fancy_grid"))
    
    print(f"Últimos 5 carros en orden cronologico de venta:")
    ultimos_5 = []
    for i in range(al.size(datos['ultimos_5'])):
        carro = al.get_element(datos['ultimos_5'], i)
        carro_info = {
            "Modelo": carro["Model"],
            "Año": carro["Year"],
            "Fuel Type": carro["Fuel Type"],
            "Color": carro["Color"],
            "Precio": carro["Base Price (USD)"],
            "Horsepower": carro["Horsepower"],
            "Turbo": carro["Turbo"]
        }
        ultimos_5.append(carro_info)
    print(tabulate(ultimos_5, headers="keys", tablefmt="fancy_grid"))

    print("\nDatos cargados exitosamente.\n")

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    combustible = input("Ingrese el tipo de combustible: ").strip().lower()
    minimo = float(input("Ingrese el valor mínimo de caballos de fuerza: "))
    maximo = float(input("Ingrese el valor máximo de caballos de fuerza: "))
    
    datos = logic.req_2(control, combustible, minimo, maximo)
    print(f"\nTiempo de consulta: {datos['tiempo']} ms")
    print(f"Total de carros encontrados: {datos['total_unidades']} unidades")
    print(f"Promedio de precio: {datos['promedio_precio']} USD")
    print(f"Promedio de caballos de fuerza: {datos['promedio_horsepower']} HP")
    
    lista_carros = datos["resultado"]
    total = datos["total_unidades"]
    
    if total == 0:
        print("\nNo se encontraron carros que cumplan con los criterios de búsqueda.\n")
    else:
        if total>12:
            datos_primeros = []
            print(f"\nMostrando los primeros 6 carros encontrados:\n")
            for i in range(6):
                carro = al.get_element(lista_carros, i)
                carro_info = {
                    "Modelo": carro["Model"],
                    "Año": carro["Year"],
                    "Fuel Type": carro["Fuel Type"],
                    "Color": carro["Color"],
                    "Precio": carro["Base Price (USD)"],
                    "Horsepower": carro["Horsepower"],
                    "Turbo": carro["Turbo"]
                }
                datos_primeros.append(carro_info)
            print(tabulate(datos_primeros, headers="keys", tablefmt="fancy_grid"))
            print(f"\nMostrando los últimos 6 carros encontrados:\n")
            datos_ultimos = []
            for i in range(total-6, total):
                carro = al.get_element(lista_carros, i)
                carro_info = {
                    "Modelo": carro["Model"],
                    "Año": carro["Year"],
                    "Fuel Type": carro["Fuel Type"],
                    "Color": carro["Color"],
                    "Precio": carro["Base Price (USD)"],
                    "Horsepower": carro["Horsepower"],
                    "Turbo": carro["Turbo"]
                }
                datos_ultimos.append(carro_info)
            print(tabulate(datos_ultimos, headers="keys", tablefmt="fancy_grid"))
        else:
            datos_carros = []
            print(f"\nMostrando los {total} carros encontrados:\n")
            for i in range(total):
                carro = al.get_element(lista_carros, i)
                carro_info = {
                    "Modelo": carro["Model"],
                    "Año": carro["Year"],
                    "Fuel Type": carro["Fuel Type"],
                    "Color": carro["Color"],
                    "Precio": carro["Base Price (USD)"],
                    "Horsepower": carro["Horsepower"],
                    "Turbo": carro["Turbo"]
                }
                datos_carros.append(carro_info)
            print(tabulate(datos_carros, headers="keys", tablefmt="fancy_grid"))

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    horsepower = int(input("Ingrese el valor de caballos de fuerza: "))
    delta = int(input("Ingrese el rango de caballos de fuerza: "))
    n = int(input("Ingrese el número de carros a mostrar: "))
    
    datos = logic.req_5(control, horsepower, delta, n)
    print(f"\nTiempo de consulta: {datos['tiempo']} ms")
    print(f"Total de carros encontrados: {datos['total_rango']} unidades")
    lista_colores = datos["resultado"]
    total_colores = al.size(lista_colores)
    
    if total_colores == 0:
        print("\nNo se encontraron carros que cumplan con los criterios de búsqueda.\n")
    else:
        print(f"\nMostrando los top {n} colores con carros más vendidos:\n")
        top = []
        for i in range(total_colores):
            info = al.get_element(lista_colores, i)
            color_info = {
                "Ranking": i+1,
                "Color": info["color"].capitalize(),
                "Ventas": info["ventas"],
                "Promedio HP": round(info["promedio_hp"], 2)
            }
            top.append(color_info)
        print(tabulate(top, headers="keys", tablefmt="fancy_grid"))
        

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
