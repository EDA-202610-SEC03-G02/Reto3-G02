import time
import csv
import os
import sys
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
from DataStructures.Priority_queue import priority_queue as pq

csv.field_size_limit(2147483647)
sys.setrecursionlimit(10000)

data_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/Data/data/'

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    analyzer = {
        "reporte_carga": None,
        "req1": None,
        "req_2": None,
        "req_3": None,
        "lista_general": None,
    }
    
    factor_carga = 0.5
    capacidad = 20000
    analyzer["reporte_carga"] = rbt.new_map()
    analyzer["req1"] = lp.new_map(capacidad, factor_carga)
    analyzer["req_2"] = lp.new_map(capacidad, factor_carga)
    analyzer["req_3"] = lp.new_map(capacidad, factor_carga)
    analyzer["lista_general"] = al.new_list()
    return analyzer

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    star_time = get_time()
    
    reporte = catalog["reporte_carga"]
    map_req1 = catalog["req1"]
    map_req2 = catalog["req_2"]
    map_req3 = catalog["req_3"]
    lista_carros = catalog["lista_general"]
    
    total = 0
    computer_file = data_dir + filename
    file = open(computer_file, encoding="utf-8")
    input_file = csv.DictReader(file)
    
    for carro in input_file:
        modelo = carro["Model"].lower().strip()
        if modelo == "" or modelo is None:
            modelo = "Unknown"
        anio = carro["Year"].strip()
        if anio == "" or anio is None:
            anio = 0
        fuel_type = carro["Fuel Type"].lower().strip()
        if fuel_type == "" or fuel_type is None:
            fuel_type = "Unknown"
        precio = carro["Base Price (USD)"].strip()
        if precio == "" or precio is None:
            precio = 0
        horsepower = carro["Horsepower"].strip()
        if horsepower == "" or horsepower is None:
            horsepower = 0
        
        al.add_last(lista_carros, carro)
        total += 1
        
        llave_reporte = f"{int(anio):04d}-{float(precio):010.2f}-{modelo}-{total}"
        rbt.put(reporte, llave_reporte, carro)
        
        arbol_req1 = lp.get(map_req1, modelo)
        if arbol_req1 is None:
            arbol_req1 = rbt.new_map()
            lp.put(map_req1, modelo, arbol_req1)
        rbt.put(arbol_req1, f"{float(precio):010.2f}-{total}", carro)
        
        arbol_req2 = lp.get(map_req2, fuel_type)
        if arbol_req2 is None:
            arbol_req2 = rbt.new_map()
            lp.put(map_req2, fuel_type, arbol_req2)
        llave_req2 = f"{int(horsepower):06d}-{float(precio):010.2f}-{modelo}-{total}"
        rbt.put(arbol_req2, llave_req2, carro)
        
        llave_req3 = f"{int(anio)}-{fuel_type}"
        arbol_req3 = lp.get(map_req3, llave_req3)
        if arbol_req3 is None:
            arbol_req3 = rbt.new_map()
            lp.put(map_req3, llave_req3, arbol_req3)
        rbt.put(arbol_req3, f"{float(precio):010.2f}-{total}", carro)
        
    file.close()
        
    llaves = rbt.key_set(reporte)
    size = sl.size(llaves)
        
    primeros_5 = al.new_list()
    for i in range(0,5):
        key = sl.get_element(llaves, i)
        al.add_last(primeros_5, rbt.get(reporte, key))
    
    ultimos_5 = al.new_list()
    for i in range(size-5, size):
        key = sl.get_element(llaves, i)
        al.add_last(ultimos_5, rbt.get(reporte, key))
    
    end_time = get_time()
    tiempo = delta_time(star_time, end_time)
    
    return {
        "tiempo": tiempo,
        "total": total,
        "primeros_5": primeros_5,
        "ultimos_5": ultimos_5
    }
           
# Funciones de consulta sobre el catálogo

def req_1(catalog, modelo, precio_min, precio_max):
    """
    Retorna el resultado del requerimiento 1
    """    
    # TODO: Modificar el requerimiento 1
      
    start = get_time()
    modelo = modelo.lower().strip()
    map_req1 = catalog["req1"]
    arbol_modelo = lp.get(map_req1, modelo)
    
    if arbol_modelo is None:
        return {"total": 0, "promedio": 0, "resultados": al.new_list(), "tiempo": delta_time(start, get_time())}
    
    precio_min_val = float(precio_min)
    precio_min_str = format(precio_min_val, "010.2f")

    llave_min = precio_min_str + "-0"


    precio_max_val = float(precio_max)
    precio_max_str = format(precio_max_val, "010.2f")
    
    llave_max = precio_max_str + "-9999999"

    carros_en_rango = rbt.values(arbol_modelo, llave_min, llave_max)
   
    total = sl.size(carros_en_rango)
    
    suma_precios = 0
    nodo = carros_en_rango["first"]
    while nodo is not None:
        carro = nodo["info"]
        precio_str = carro["Base Price (USD)"].strip()
        if precio_str != "":
            precio_val = float(precio_str)
        else:
         precio_val = 0
        suma_precios += precio_val
        nodo = nodo["next"]
    if total > 0:
        promedio = suma_precios / total
    else:
        promedio = 0
        
    resultado_al = al.new_list()
    nodo = carros_en_rango["first"]
    while nodo is not None:
        al.add_last(resultado_al, nodo["info"])
        nodo = nodo["next"]

    al.merge_sort(resultado_al, sort_req1)
    
    total = al.size(resultado_al)
    if total > 12:
        indices = list(range(0, 6)) + list(range(total - 6, total))
        separador_en = 6
    else:
        indices = list(range(total))
        separador_en = -1

    end = get_time()
    return {
        "tiempo": delta_time(start, end),
        "total": total,
        "promedio": promedio,
        "resultados": resultado_al,
        "indices": indices,
        "separador_en": separador_en
    }
    
def sort_req1(c1, c2):
    p1 = float(c1["Base Price (USD)"].strip() or 0)
    p2 = float(c2["Base Price (USD)"].strip() or 0)
    if p1 != p2:
        return p1 < p2 
    h1 = int(c1["Horsepower"].strip() or 0)
    h2 = int(c2["Horsepower"].strip() or 0)
    if h1 != h2:
        return h1 > h2 
    return c1["Color"].strip() < c2["Color"].strip()

def req_2(catalog, combustible, minimo, maximo):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    star_time = get_time()
    
    map_req2 = catalog["req_2"]
    arbol_req2 = lp.get(map_req2, combustible.lower().strip())
    
    unidad_vendida = 0
    suma_precios = 0
    suma_horsepower = 0
    resultado = al.new_list()
    
    if arbol_req2 is not None:
        llaves = rbt.key_set(arbol_req2)
        size = sl.size(llaves)
        
        for i in range(size):
            key = sl.get_element(llaves,i)
            horsepower = int(key.split("-")[0])
            
            if minimo <= horsepower <= maximo:
                carro = rbt.get(arbol_req2, key)
                al.add_last(resultado, carro)
                
                unidad_vendida += 1
                suma_precios += float(carro["Base Price (USD)"])
                suma_horsepower += horsepower
    
    if unidad_vendida > 0:
        promedio_precio = suma_precios / unidad_vendida
        promedio_horsepower = suma_horsepower / unidad_vendida
    else:
        promedio_precio = 0
        promedio_horsepower = 0
    
    end_time = get_time()
    tiempo = delta_time(star_time, end_time)
    
    return {
        "tiempo": tiempo,
        "total_unidades": unidad_vendida,
        "promedio_precio": round(promedio_precio, 2),
        "promedio_horsepower": round(promedio_horsepower, 2),
        "resultado": resultado
    }


def req_3(catalog, anio, fuel_type, precio_min, precio_max):
   """
   Retorna el resultado del requerimiento 3
   """
   # TODO: Modificar el requerimiento 3
   start_time = get_time()


   map_req3 = catalog["req_3"]
   llave = f"{int(anio)}-{fuel_type.lower().strip()}"


   arbol = lp.get(map_req3, llave)


   resultado = al.new_list()
   total = 0
   suma_precios = 0


   if arbol is not None:
       llaves = rbt.key_set(arbol)
       size = sl.size(llaves)


       arbol_ordenado = rbt.new_map()


       for i in range(size):
           key = sl.get_element(llaves, i)
           carro = rbt.get(arbol, key)


           precio = float(carro["Base Price (USD)"])
           horsepower = int(carro["Horsepower"])
           turbo = carro["Turbo"].lower().strip()


           if precio_min <= precio <= precio_max:
               total += 1
               suma_precios += precio


               turbo_orden = 0
               if turbo != "yes":
                   turbo_orden = 1


               llave_orden = f"{999999999 - precio:015.2f}-{999999 - horsepower:06d}-{turbo_orden}-{total}"


               rbt.put(arbol_ordenado, llave_orden, carro)


       llaves_ordenadas = rbt.key_set(arbol_ordenado)
       size_ordenado = sl.size(llaves_ordenadas)


       for i in range(size_ordenado):
           key = sl.get_element(llaves_ordenadas, i)
           al.add_last(resultado, rbt.get(arbol_ordenado, key))


   promedio = 0
   if total > 0:
       promedio = suma_precios / total


   end_time = get_time()
   tiempo = delta_time(start_time, end_time)


   return {
       "tiempo": tiempo,
       "total": total,
       "promedio_precio": promedio,
       "ventas": resultado
   }



def req_4(catalog, anio, N):
    """
    Retorna el resultado del requerimiento 4:
    Para un año dado, identificar los N modelos con mayor número de vehículos vendidos.
    """

    start = get_time()

    reporte = catalog["reporte_carga"]
    llave_min = f"{int(anio):04d}-0000000000.00-"
    llave_max = f"{int(anio):04d}-9999999999.99-~"
    carros_anio = rbt.values(reporte, llave_min, llave_max)
    
    mapa_modelos = lp.new_map(5000, 0.5)

    nodo = carros_anio["first"]
    while nodo is not None:
        carro = nodo["info"]

        modelo_raw = carro["Model"].strip()
        if modelo_raw:
            modelo = modelo_raw.lower()
        else:
            modelo = None

        precio = float(carro["Base Price (USD)"].strip() or 0)
        hp = int(carro["Horsepower"].strip() or 0)
        turbo = carro["Turbo"].strip().lower()
        anio_carro = int(carro["Year"].strip() or 0)

        info = lp.get(mapa_modelos, modelo)
        if info is None:
            info = {
                "ventas": 0,
                "suma_precio": 0.0,
                "suma_hp": 0,
                "turbo_yes": 0,
                "max_hp": -1,
                "max_hp_carro": None
            }

        info["ventas"] += 1
        info["suma_precio"] += precio
        info["suma_hp"] += hp
        if turbo == "yes":
            info["turbo_yes"] += 1

        if hp > info["max_hp"]:
            info["max_hp"] = hp
            info["max_hp_carro"] = carro
        elif hp == info["max_hp"] and info["max_hp_carro"] is not None:
            precio_actual = float(info["max_hp_carro"]["Base Price (USD)"].strip() or 0)
            anio_actual = int(info["max_hp_carro"]["Year"].strip() or 0)
            if precio < precio_actual or (precio == precio_actual and anio_carro < anio_actual):
                info["max_hp_carro"] = carro

        lp.put(mapa_modelos, modelo, info)
        nodo = nodo["next"]

    lista_modelos = al.new_list()
    tabla = mapa_modelos["table"]

    for i in range(mapa_modelos["capacity"]):
        entry = al.get_element(tabla, i)
        key = me.get_key(entry)
        value = me.get_value(entry)

        if key is not None and key != "__EMPTY__":
            ventas = value["ventas"]
            precio_prom = value["suma_precio"] / ventas
            hp_prom = value["suma_hp"] / ventas
            pct_turbo = (value["turbo_yes"] / ventas) * 100

            al.add_last(lista_modelos, {
                "modelo": key,
                "ventas": ventas,
                "precio_prom": precio_prom,
                "hp_prom": hp_prom,
                "pct_turbo": pct_turbo,
                "max_hp_carro": value["max_hp_carro"]
            })

    total_modelos = al.size(lista_modelos)

    al.merge_sort(lista_modelos, sort_req4)

    n_real = min(N, total_modelos)
    top_n = al.sub_list(lista_modelos, 0, n_real)

    end = get_time()
    return {
        "tiempo": delta_time(start, end),
        "total_modelos": total_modelos,
        "top_n": top_n
    }


def sort_req4(m1, m2):
    if m1["ventas"] != m2["ventas"]:
        return m1["ventas"] > m2["ventas"]
    return m1["precio_prom"] > m2["precio_prom"]

def req_5(catalog, horsepower, delta, n):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    star_time = get_time()
    horsepower_min = horsepower - delta
    horsepower_max = horsepower + delta
    
    lista_carros = catalog["lista_general"]
    size = al.size(lista_carros)
    
    mapa_agrupado = lp.new_map(10000, 0.5)
    lista_colores = al.new_list()
    total_rango = 0
    
    for i in range(size):
        carro = al.get_element(lista_carros, i)
        horsep = int(carro["Horsepower"].strip())
        
        if horsepower_min <= horsep <= horsepower_max:
            total_rango += 1
            color = carro["Color"].lower().strip()
            registros_color = lp.get(mapa_agrupado, color)
            if registros_color is None:
                al.add_last(lista_colores, color)
                nuevo = {"ventas":1, "suma_hp": horsep}
                lp.put(mapa_agrupado, color, nuevo)
            else:
                registros_color["ventas"] += 1
                registros_color["suma_hp"] += horsep
    
    cola_prioridad = pq.new_heap()
    size_colores = al.size(lista_colores)
    
    for i in range(size_colores):
        color = al.get_element(lista_colores, i)
        datos_color = lp.get(mapa_agrupado, color)
        ventas = datos_color["ventas"]
        suma_hp = datos_color["suma_hp"]
        promedio_hp = suma_hp / ventas
        
        llave = f"{1000000 - ventas:06d}-{100000 - promedio_hp:06.2f}-{color}"
        
        info_color = {
            "color": color,
            "ventas": ventas,
            "promedio_hp": promedio_hp
        }
        
        pq.insert(cola_prioridad, llave, info_color)
        
    resultado = al.new_list()
    for i in range(n):
        if not pq.is_empty(cola_prioridad):
            mejor = pq.remove(cola_prioridad)
            al.add_last(resultado, mejor)
            
    end_time = get_time()
    tiempo = delta_time(star_time, end_time)
    
    return {
        "tiempo": tiempo,
        "total_rango": total_rango,
        "resultado": resultado
    }
    

def req_6(catalog, anio_min, anio_max, precio_min, precio_max, m):
   """
   Retorna el resultado del requerimiento 6
   """
   # TODO: Modificar el requerimiento 6
   start_time = get_time()


   lista_carros = catalog["lista_general"]
   mapa_modelos = lp.new_map(20000, 4)
   lista_modelos = al.new_list()


   size = al.size(lista_carros)


   for i in range(size):
       carro = al.get_element(lista_carros, i)


       anio = int(carro["Year"])
       precio = float(carro["Base Price (USD)"])


       if anio_min <= anio <= anio_max and precio_min <= precio <= precio_max:
           modelo = carro["Model"].lower().strip()


           info = lp.get(mapa_modelos, modelo)


           if info is None:
               info = {
                   "modelo": modelo,
                   "ventas": al.new_list(),
                   "suma_precios": 0,
                   "suma_cuadrados": 0,
                   "suma_hp": 0,
                   "total": 0
               }


               lp.put(mapa_modelos, modelo, info)
               al.add_last(lista_modelos, modelo)


           al.add_last(info["ventas"], carro)
           info["suma_precios"] += precio
           info["suma_cuadrados"] += precio ** 2
           info["suma_hp"] += int(carro["Horsepower"])
           info["total"] += 1


   arbol_estabilidad = rbt.new_map()
   modelos_considerados = 0


   for i in range(al.size(lista_modelos)):
       modelo = al.get_element(lista_modelos, i)
       info = lp.get(mapa_modelos, modelo)


       total = info["total"]
       promedio = info["suma_precios"] / total


       if promedio != 0:
           modelos_considerados += 1


           varianza = (info["suma_cuadrados"] / total) - (promedio ** 2)


           if varianza < 0:
               varianza = 0


           desviacion = varianza ** 0.5
           estabilidad = desviacion / promedio
           hp_promedio = info["suma_hp"] / total


           venta_repr = encontrar_representativa(info["ventas"], promedio)


           registro = {
               "modelo": modelo,
               "total_ventas": total,
               "promedio_precio": promedio,
               "desviacion": desviacion,
               "estabilidad": estabilidad,
               "horsepower_promedio": hp_promedio,
               "venta_representativa": venta_repr
           }


           llave_orden = f"{estabilidad:020.10f}-{desviacion:020.10f}-{modelo}"
           rbt.put(arbol_estabilidad, llave_orden, registro)


   resultado = al.new_list()
   llaves_estabilidad = rbt.key_set(arbol_estabilidad)


   limite = m
   if sl.size(llaves_estabilidad) < m:
       limite = sl.size(llaves_estabilidad)


   nodo = llaves_estabilidad["first"]
   contador = 0


   while nodo is not None and contador < limite:
       key = nodo["info"]
       al.add_last(resultado, rbt.get(arbol_estabilidad, key))


       nodo = nodo["next"]
       contador += 1


   end_time = get_time()
   tiempo = delta_time(start_time, end_time)


   return {
       "tiempo": tiempo,
       "modelos_considerados": modelos_considerados,
       "modelos": resultado
   }
  
def encontrar_representativa(lista_ventas, promedio):
   mejor = None
   mejor_diferencia = None


   for i in range(al.size(lista_ventas)):
       carro = al.get_element(lista_ventas, i)


       precio = float(carro["Base Price (USD)"])
       anio = int(carro["Year"])
       diferencia = abs(precio - promedio)


       if mejor is None:
           mejor = carro
           mejor_diferencia = diferencia


       else:
           mejor_precio = float(mejor["Base Price (USD)"])
           mejor_anio = int(mejor["Year"])


           if diferencia < mejor_diferencia:
               mejor = carro
               mejor_diferencia = diferencia


           elif diferencia == mejor_diferencia:
               if precio < mejor_precio:
                   mejor = carro
                   mejor_diferencia = diferencia


               elif precio == mejor_precio and anio < mejor_anio:
                   mejor = carro
                   mejor_diferencia = diferencia


   return mejor


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
