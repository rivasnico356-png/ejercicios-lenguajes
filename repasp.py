# def duplicar(x):
# return x * 2



# # funciones puras 

# public class personas 
# _(
# flat salario;
# string nombre;
# int identificador;


# //metodos 
# public perosna()
# public float getsalario(){}
# public void setsalrio(){}
# public void aplicarAumento(float porc){}
# public void aplicarBonifc(float valor)()

# )


# #ejemplo 

# valor_usuario = int(input("Ingrese un entero cualquiera:"))
# print(f"El valor duplicado es: {duplicar(valor_usuario)}")


# from functools import reduce

# lista_palabras = ["SI", "LO", "puedes", "SOÑAR", "lo", "PUEDES", "PROGRAMAR"]


# palabras_correctas = list(map(lambda palabra: palabra.lower(), lista_palabras))


# palabras_correctas[0] = palabras_correctas[0].capitalize()

# print("Lista corregida:", palabras_correctas)

# oracion = reduce(
#     lambda palabra1, palabra2: palabra1 + " " + palabra2,
#     palabras_correctas
# )

# print("Oración final:", oracion)


# Función para consumidor hambriento
def eager():
    numbers = []
    for i in range(500000):
        numbers.append(i)
    return numbers


# Función perezosa: genera valores bajo demanda
def lazy_generator():
    for i in range(10000):
        yield i


# Consumo con "evaluación hambrienta"

# nuevos_numeros = eager()
# print(nuevos_numeros)


# Consumo con evaluación perezosa

gen = lazy_generator()

try:
    while True:
        print(next(gen))   #El consumidor perezoso consume solo un elemento a la vez
except StopIteration:
    print("El generador ya no tiene mas números")






 