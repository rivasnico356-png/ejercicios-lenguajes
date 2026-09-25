"""
Ejercicio: Programación funcional sobre datos de humedales de Cali.
Completar cada función marcada con # TODO.
No usar bucles for/while explícitos dentro de las funciones
(sí se permiten dentro de comprensiones).
"""

from functools import reduce


# ---------------------------------------------------------------------------
# Carga de datos
def LoadData(fileName):
    dataset = []
    with open(fileName, encoding='utf-8') as f:
        for line in f:
            values = line.split(sep=';')

            registro = {
                "nombre": values[0],
                "direccion": values[1],
                "hectareas": float(values[2]),
                "aves": int(values[3]),
                "flora": int(values[4]),
                "estado": values[5].strip()
            }

            dataset.append(registro)

    return dataset


# ---------------------------------------------------------------------------
def LoadData_lazy(fileName):
    with open(fileName, encoding='utf-8') as f:
        for line in f:
            values = line.split(sep=';')

            registro = {
                "nombre": values[0],
                "direccion": values[1],
                "hectareas": float(values[2]),
                "aves": int(values[3]),
                "flora": int(values[4]),
                "estado": values[5].strip()
            }

            yield registro


# ---------------------------------------------------------------------------
# Punto 1
def filtrar_por_estado(dataset, estado):
    """
    Retorna los registros cuyo 'estado' coincide con el parámetro dado
    (comparación insensible a mayúsculas/minúsculas y espacios).
    """

    return list(
        filter(
            lambda registro: registro["estado"].strip().lower() == estado.strip().lower(),
            dataset
        )
    )


# ---------------------------------------------------------------------------
# Punto 2
def extraer_nombres(dataset):
    """
    Retorna una lista solo con los nombres de los humedales.
    """

    return list(
        map(
            lambda registro: registro["nombre"],
            dataset
        )
    )


# ---------------------------------------------------------------------------
# Punto 3
def total_hectareas(dataset):
    """
    Retorna la suma total de hectáreas de todos los humedales.
    """

    return reduce(
        lambda acumulado, registro: acumulado + registro["hectareas"],
        dataset,
        0
    )


# ---------------------------------------------------------------------------
# Punto 4
def promedio_biodiversidad(dataset):
    """
    Retorna el promedio de (aves + flora) por humedal,
    usando reduce.
    """

    total_biodiversidad = reduce(
        lambda acumulado, registro:
            acumulado + registro["aves"] + registro["flora"],
        dataset,
        0
    )

    return total_biodiversidad / len(dataset) if dataset else 0


# ---------------------------------------------------------------------------
# Punto 5
def extraer_estados(dataset):
    """
    Retorna el conjunto (set) de estados distintos
    presentes en el dataset.
    """

    return set(
        map(
            lambda registro: registro["estado"].strip(),
            dataset
        )
    )


def resumen_por_estado(dataset):
    """
    Retorna un diccionario:
    {estado: cantidad_de_humedales_en_ese_estado}
    """

    estados = extraer_estados(dataset)

    return {
        estado: len(
            filtrar_por_estado(dataset, estado)
        )
        for estado in estados
    }


# ---------------------------------------------------------------------------
# Punto 6
def humedales_criticos_lazy(fileName, hectareas_min):
    """
    Retorna un GENERADOR (no una lista) con los humedales cuyo estado es
    'Deteriorado' o cuyas hectáreas son menores a hectareas_min.

    Usa LoadData_lazy() + filter(), conservando la evaluación perezosa.
    """

    return filter(
        lambda registro:
            registro["estado"].strip().lower() == "deteriorado"
            or registro["hectareas"] < hectareas_min,
        LoadData_lazy(fileName)
    )


# ---------------------------------------------------------------------------
# Punto 7 - BONUS
def componer(*funciones):
    """
    Retorna una nueva función que aplica las funciones recibidas
    en cadena, de derecha a izquierda.

    Ejemplo:
    componer(f, g)(x) == f(g(x))
    """

    def identidad(x):
        return x

    def aplicar(f, g):
        return lambda x: f(g(x))

 


# ---------------------------------------------------------------------------

if __name__ == "__main__":

    dataset = LoadData("dataset1.csv")

   
    print("Humedales en estado Deteriorado:")
    print(filtrar_por_estado(dataset, "deteriorado"))


    print("\nNombres de todos los humedales:")
    print(extraer_nombres(dataset))

 
    print("\nTotal de hectáreas:")
    print(total_hectareas(dataset))

  
    print("\nPromedio de biodiversidad (aves + flora):")
    print(promedio_biodiversidad(dataset))


    print("\nEstados diferentes:")
    print(extraer_estados(dataset))

    print("\nResumen por estado:")
    print(resumen_por_estado(dataset))

   
    print("\nGenerador perezoso (humedales críticos, hectareas_min=3.0):")

    gen = humedales_criticos_lazy("dataset1.csv", 3.0)

    print(next(gen))
    print(next(gen))


  