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
    modelo = input("Ingrese el modelo a consultar (ej: GLC): ").strip()
    precio_min = float(input("Ingrese el precio mínimo (USD): ").strip())
    precio_max = float(input("Ingrese el precio máximo (USD): ").strip())

    resultado = logic.req_1(control, modelo, precio_min, precio_max)

    print(f"\nTiempo de ejecución: {resultado['tiempo']:.2f} ms")
    print(f"Total de ventas que cumplen el filtro: {resultado['total']}")
    print(f"Promedio de precio: ${resultado['promedio']:,.2f} USD")

    lista = resultado["resultados"]
    total = resultado["total"]

    if total == 0:
        print("No se encontraron ventas con los filtros ingresados")
        return
 
    indices = resultado["indices"]
    separador_en = resultado["separador_en"]

    filas = []
    for i in range(len(indices)):
        idx = indices[i]

        if separador_en != -1 and i == separador_en:
            filas.append({
                "Modelo": None,
                "Año": None,
                "Fuel Type": None,
                "Color": None,
                "Base Price (USD)": None,
                "Horsepower": None,
                "Turbo": None
            })

        carro = al.get_element(lista, idx)
        precio_val = carro.get("Base Price (USD)", "").strip() or None
        filas.append({
            "Modelo":          carro.get("Model", None).strip() if carro.get("Model") else None,
            "Año":             carro.get("Year", None).strip() if carro.get("Year") else None,
            "Fuel Type":       carro.get("Fuel Type", None).strip() if carro.get("Fuel Type") else None,
            "Color":           carro.get("Color", None).strip() if carro.get("Color") else None,
            "Base Price (USD)": precio_val,
            "Horsepower":      carro.get("Horsepower", None).strip() if carro.get("Horsepower") else None,
            "Turbo":           carro.get("Turbo", None).strip() if carro.get("Turbo") else None,
        })
    print(tabulate(filas, headers="keys", tablefmt="fancy_grid"))

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


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
    anio = int(input("Ingrese el año a consultar (ej: 2021): ").strip())
    N = int(input("Ingrese la cantidad N de modelos a mostrar: ").strip())

    resultado = logic.req_4(control, anio, N)

    print(f"\nTiempo de ejecución: {resultado['tiempo']:.2f} ms")
    print(f"Total de modelos encontrados en {anio}: {resultado['total_modelos']}")
    print(f"\nTop {N} modelos con mayor número de ventas en {anio}:\n")

    top_n = resultado["top_n"]
    total_top = al.size(top_n)

    for i in range(total_top):
        info = al.get_element(top_n, i)

        print(f"{'='*60}")
        modelo_str = info["modelo"].upper() if info["modelo"] is not None else "None"
        print(f"  #{i+1} — Modelo: {modelo_str}")
        print(f"{'='*60}")

        resumen = [{
            "Ventas":          info["ventas"],
            "Precio Promedio": f"${info['precio_prom']:,.2f}",
            "HP Promedio":     f"{info['hp_prom']:.1f}",
            "% Turbo":         f"{info['pct_turbo']:.1f}%",
        }]
        print(tabulate(resumen, headers="keys", tablefmt="fancy_grid"))

        max_carro = info.get("max_hp_carro")
        if max_carro:
            print(f"\n  Venta con mayor Horsepower del modelo {modelo_str}:")
            detalle = [{
                "Modelo":           max_carro["Model"].strip() if max_carro["Model"].strip() else None,
                "Año":              max_carro["Year"].strip() if max_carro["Year"].strip() else None,
                "Fuel Type":        max_carro["Fuel Type"].strip() if max_carro["Fuel Type"].strip() else None,
                "Color":            max_carro["Color"].strip() if max_carro["Color"].strip() else None,
                "Base Price (USD)": max_carro["Base Price (USD)"].strip() if max_carro["Base Price (USD)"].strip() else None,
                "Horsepower":       max_carro["Horsepower"].strip() if max_carro["Horsepower"].strip() else None,
                "Turbo":            max_carro["Turbo"].strip() if max_carro["Turbo"].strip() else None,
            }]
            print(tabulate(detalle, headers="keys", tablefmt="fancy_grid"))
        else:
            print("  No se encontró venta representativa.")

        print()



def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


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
