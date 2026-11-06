#01/10/2026

#unidad 2 :P.O.O en python 
#conceptos escenciales
#(abstracion, encapsulamiento, herencia)

#principios SOLID
#
#
#interfaces (diseño x contrato)
#
#
#patrones de diseño 
#patron arquitectonico MVC




from  abc import ABC, abstractmethod
from pyclbr import Class

#-----------------------------------------ASTRACCIÓN--------------------------------------------

#INTRODUCCIÓN A LA ASTRACCIÓN
#clase absstracta que define la interfaz de un método de pago

class MetodoPago(ABC):
    @abstractmethod
    #los metodosque empiecen con una referencia a this, o self, son
    #metodos de instancia 
    def procesar_pago(self, monto:float):
        pass



#clases concetas: métodos de pago, especificos:
class TarjetaCredito(MetodoPago):
    def procesar_pago(this, monto):
        #return super().procesar_pago(monto)
        print(f"Procesando pago con tarjeta de crédito por el monto:", monto)

class pagoMercadoPago(MetodoPago):
    def procesar_pago(this, monto):
        print("procesando pago Mercado pago por: ", monto)


#-----------------------------------------ENCAPSULAMIENTO--------------------------------------------

#INSTRODUCCIÓN AL ENCAPSULAMIENTO

class cuentaBancaria:

    def __init__(this, titular:str, numero:int, saldo_inicial:float):

        #Todos los atributoss de "This", "self", son atributoss de instancia:
        this.titular = titular
        this.numero = numero
        this.saldo_inic = saldo_inicial


    def obtener_saldo(this):
        return this.saldo

    def depositar(this, valor:float):
        if valor > 0:
            this.saldo = this.saldo + valor

    def hacer_retiro(this, valor:float):
        if valor > 0 and this._saldo >= valor:
            this._saldo -= valor


#------------------------------------------HERENCIA--------------------------------------------

class Empleado(ABC):
    def __init__(this, nombre: str, id: int, salario_base: float):
        this.nombre = nombre
        this.id = id
        this.salario_base = salario_base

    @abstractmethod
    def liquidar_pago(this):
        pass


class Administrativo(Empleado):
    def __init__(this, nombre: str, id: int, salario_base: float, bono: float):
        super().__init__(nombre, id, salario_base)
        this.bono = bono

    def liquidar_pago(this):
        # Liquidar pago con el bono
        return this.salario_base + this.bono


class Docente(Empleado):
    def __init__(this, nombre: str, id: int, salario_base: float, bono: float):
        super().__init__(nombre, id, salario_base)
        this.bono = bono

    def liquidar_pago(this):
        # Liquidar pago con el bono
        return this.salario_base + this.bono


administrativo = Administrativo("Carlos", 101, 2000000, 300000)
docente = Docente("Maria", 102, 2500000, 500000)

print(administrativo.liquidar_pago())
print(docente.liquidar_pago())


#Crear empleados
administrativo = Administrativo("Carlos", 101, 2000000, 300000)
docente = Docente("María", 102, 2500000, 500000)

print("Pago administrativo:", administrativo.liquidar_pago())
print("Pago docente:", docente.liquidar_pago())



#----------------------------------Ejercicio para la proxima semana--------------------------------------------   

#sistema de gestión de una biblioteca:
#A) lIBROS FISICOS 
#B)E-books 
#C)Audiolibros

#1. Astracción: que clase asbstracta modela el recurso bibliografico (titulo,autor,año)
#2.herencia:cada tipo de publicación tiene sus atributos propios
#3. cada publicación tiene sus atributos privados: usuario en prestamo, fecha de entrega 
#4. polimorfismo: cada tipo de publicación tiene su propia forma de gestionar prestamo


from abc import ABC, abstractmethod
from datetime import date, timedelta


#-----------------------------------------1. ABSTRACCIÓN--------------------------------------------

class RecursoBibliografico(ABC):

    def __init__(self, titulo: str, autor: str, anio: int):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio

        #-------------------------------3. ENCAPSULAMIENTO----------------------------------
        # Atributos privados (doble guion bajo)
        self.__usuario_prestamo = None
        self.__fecha_entrega = None

    # Getters: permiten LEER los atributos privados
    @property
    def usuario_prestamo(self):
        return self.__usuario_prestamo

    @property
    def fecha_entrega(self):
        return self.__fecha_entrega

    def esta_prestado(self) -> bool:
        return self.__usuario_prestamo is not None

    # Métodos protegidos: las clases hijas los usan para modificar los privados
    def _registrar_prestamo(self, usuario: str, dias: int):
        if self.esta_prestado():
            raise ValueError(f"'{self.titulo}' ya está prestado a {self.__usuario_prestamo}")
        if not usuario:
            raise ValueError("Debe indicar un usuario")
        self.__usuario_prestamo = usuario
        self.__fecha_entrega = date.today() + timedelta(days=dias)

    def _limpiar_prestamo(self):
        self.__usuario_prestamo = None
        self.__fecha_entrega = None

    # Contrato que toda publicación debe cumplir
    @abstractmethod
    def prestar(self, usuario: str):
        pass

    @abstractmethod
    def devolver(self):
        pass

    def __str__(self):
        estado = (f"prestado a {self.usuario_prestamo} hasta {self.fecha_entrega}"
                  if self.esta_prestado() else "disponible")
        return f"[{type(self).__name__}] {self.titulo} - {self.autor} ({self.anio}) -> {estado}"


#-----------------------------------------2. HERENCIA--------------------------------------------

class LibroFisico(RecursoBibliografico):
    DIAS_PRESTAMO = 15

    def __init__(self, titulo, autor, anio, num_paginas: int, estante: str):
        super().__init__(titulo, autor, anio)
        self.num_paginas = num_paginas
        self.estante = estante

    #------------------------------4. POLIMORFISMO------------------------------------
    def prestar(self, usuario: str):
        self._registrar_prestamo(usuario, self.DIAS_PRESTAMO)
        print(f"Libro físico '{self.titulo}': retirar en el estante {self.estante}. "
              f"Entregar antes del {self.fecha_entrega}.")

    def devolver(self):
        if not self.esta_prestado():
            print(f"'{self.titulo}' no estaba prestado.")
            return
        dias_retraso = (date.today() - self.fecha_entrega).days
        multa = dias_retraso * 1000 if dias_retraso > 0 else 0
        self._limpiar_prestamo()
        print(f"Libro físico '{self.titulo}' devuelto. Multa: ${multa}")


class EBook(RecursoBibliografico):
    DIAS_PRESTAMO = 7

    def __init__(self, titulo, autor, anio, formato: str, tamano_mb: float):
        super().__init__(titulo, autor, anio)
        self.formato = formato
        self.tamano_mb = tamano_mb

    def prestar(self, usuario: str):
        self._registrar_prestamo(usuario, self.DIAS_PRESTAMO)
        print(f"E-book '{self.titulo}': enlace de descarga ({self.formato}, {self.tamano_mb} MB) "
              f"enviado a {usuario}. Licencia hasta el {self.fecha_entrega}.")

    def devolver(self):
        if not self.esta_prestado():
            print(f"'{self.titulo}' no estaba prestado.")
            return
        self._limpiar_prestamo()
        print(f"E-book '{self.titulo}': licencia revocada.")


class Audiolibro(RecursoBibliografico):
    DIAS_PRESTAMO = 10

    def __init__(self, titulo, autor, anio, duracion_min: int, narrador: str):
        super().__init__(titulo, autor, anio)
        self.duracion_min = duracion_min
        self.narrador = narrador

    def prestar(self, usuario: str):
        self._registrar_prestamo(usuario, self.DIAS_PRESTAMO)
        horas, minutos = divmod(self.duracion_min, 60)
        print(f"Audiolibro '{self.titulo}' ({horas}h {minutos}min, narrado por {self.narrador}): "
              f"streaming para {usuario} hasta el {self.fecha_entrega}.")

    def devolver(self):
        if not self.esta_prestado():
            print(f"'{self.titulo}' no estaba prestado.")
            return
        self._limpiar_prestamo()
        print(f"Audiolibro '{self.titulo}': acceso cerrado.")


#-----------------------------------------PRUEBAS--------------------------------------------

catalogo = [
    LibroFisico("Cien años de soledad", "Gabriel García Márquez", 1967, 471, "A-12"),
    EBook("Clean Code", "Robert C. Martin", 2008, "PDF", 4.5),
    Audiolibro("El principito", "Antoine de Saint-Exupéry", 1943, 95, "Juan Pérez"),
]

# Polimorfismo: el mismo método se comporta distinto según el tipo
for recurso in catalogo:
    recurso.prestar("Ana Gómez")

for recurso in catalogo:
    print(recurso)

# Encapsulamiento
libro = catalogo[0]
try:
    print(libro.__usuario_prestamo)
except AttributeError:
    print("No se puede acceder al atributo privado directamente")
print("Con el getter:", libro.usuario_prestamo)

# Abstracción: no se puede instanciar la clase abstracta
try:
    RecursoBibliografico("X", "Y", 2000)
except TypeError:
    print("RecursoBibliografico es abstracta, no se puede instanciar")

for recurso in catalogo:
    recurso.devolver()




#PRINCICIOS SOLID APLICADOS A LA PROGRAMACIÓN ORIENTADA A OBJETOS 


# S - Single Responsibility 
#Una clase dede tener una sola responsabilidad, y por lo tanto, una sola razón para cambiar.
#regla:Abierto para extensión, cerrado para modificación.

# O - Open/Closed for modificación

#Ejemplo:Aplicar estos dos ejemplos a la implementacipón de un módulo de Liquidación de matricula a estudiante,aplicando distintos tipos de descuento.

# L - Liskov Substitution Principle (LSP): Una subclase debe poder reeemplazar a su clase padre sin vulnerar el diseño ni la implementación
Ejemplo:una clase abstracta de descuento, y distintas clases concretas que implementen distintos tipos de descuento
#y una clase calculadora que calcule la liquidación de la matrícula del estudiante aplicando los descuentos que correspondan.

# I - Interface Segregation Principle (ISP): Una clase no debe depender de métodos que no utiliza.
Ejemplo:una clase abstracta de descuento, y distintas clases concretas que implementen distintos tipos de descuento

# D - Dependency Inversion Principle (DIP): Una clase debe depender de abstracciones, no de implementaciones concretas.
#Ejemplo:

#Sistme ade notificaciones:

class EmailSender:
    def send_email(self, message):
        print(f"Enviando notificación: {message}")

class SMSSender:
    pass

class WhatsappSender:
    pass


class Notificationservice:
    def __init__(self):
        #ya estoy "amarrando" la funcionalidad a una implementación concreta
        self.sender = EmailSender

    def sendNotification(self, message):
        self.sender.send_email(message)

#Como lo solucionamos:

class INotificationService(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailSender(INotificationService):
    def send(self, message):
        print(f"Enviando notificación:{message}, por email")

class SMSSender(INotificationService):
    def send(self, message):
        print(f"Enviando notificación:{message}, por SMS")

class WhatsappSender(INotificationService):
    def send(self, message):
        print(f"Enviando notificación:{message}, por WhatsApp")

sender_via_sms = SMSSender()

myNotificationService = Notificationservice(sender_via_sms)
myNotificationService.sen("Hola ya llego el pedido")



#Ejemplo de aplicación de los principios SOLID a la liquidación de matrícula de un estudiante, aplicando distintos tipos de descuento.--------------------------------------------------------------
 
from abc import ABC, abstractmethod
 
 

 
class IDescuento(ABC):
   
 
# principio L
      
    @abstractmethod
    def calcular(self, valor_matricula: float) -> float:
        pass
 
    @abstractmethod
    def descripcion(self) -> str:
        pass
 
 
class IRequiereSoporte(ABC):
    """Interfaz SOLO para descuentos que exigen un documento de soporte."""
    @abstractmethod
    def documento_soporte(self) -> str:
        pass
 

 
class MatriculaHonor(IDescuento):
    def __init__(self, promedio: float):
        self.promedio = promedio
 
    def calcular(self, valor_matricula):
        return valor_matricula * 0.50 if self.promedio >= 4.5 else 0
 
    def descripcion(self):
        return f"Matrícula de honor (promedio {self.promedio})"
 
 
class Familiar(IDescuento, IRequiereSoporte):        # I: implementa también IRequiereSoporte
    def __init__(self, num_hermanos: int):
        self.num_hermanos = num_hermanos
 
    def calcular(self, valor_matricula):
        return valor_matricula * 0.10 if self.num_hermanos >= 1 else 0
 
    def descripcion(self):
        return f"Descuento familiar ({self.num_hermanos} hermano(s))"
 
    def documento_soporte(self):
        return "Registro civil del hermano"
 
 
class Convenio(IDescuento, IRequiereSoporte):        # I: implementa también IRequiereSoporte
    def __init__(self, empresa: str, porcentaje: float):
        self.empresa = empresa
        self.porcentaje = porcentaje
 
    def calcular(self, valor_matricula):
        if not self.empresa:
            return 0                                                # L: sin error, solo no hay descuento
        return valor_matricula * min(max(self.porcentaje, 0), 1)   # L: siempre entre 0% y 100%
 
    def descripcion(self):
        return f"Convenio con {self.empresa or 'ninguna empresa'} ({self.porcentaje:.0%})"
 
    def documento_soporte(self):
        return f"Carta laboral de {self.empresa or '(empresa no registrada)'}"
 
 
 
class Deportista(IDescuento):        # EXTENSIÓN: se agregó sin tocar nada más
    def __init__(self, deporte: str):
        self.deporte = deporte
 
    def calcular(self, valor_matricula):
        return valor_matricula * 0.15
 
    def descripcion(self):
        return f"Descuento deportista ({self.deporte})"
 
 

 
class ReciboMatricula:
    """Responsabilidad: SOLO mostrar el recibo."""
    def imprimir(self, estudiante: str, descuento: IDescuento, valor: float, total: float):
        print("=" * 55)
        print(f"Estudiante: {estudiante}")
        print(f"  {descuento.descripcion()}")
        print(f"  Matrícula: ${valor:,.0f}   Descuento: -${valor - total:,.0f}")
        print(f"  TOTAL A PAGAR: ${total:,.0f}")
 
 
class RepositorioMatricula:
    """Responsabilidad: SOLO guardar la información."""
    def __init__(self):
        self.registros = []
 
    def guardar(self, estudiante: str, total: float):
        self.registros.append((estudiante, total))
        print(f"  [Guardado] {estudiante} -> ${total:,.0f}")
 
 

 
class AplicadorDescuento:
    """Clase de alto nivel. S: su única responsabilidad es aplicar el descuento."""
    def __init__(self, recibo: ReciboMatricula, repositorio: RepositorioMatricula):
        self.recibo = recibo                     # D: inyectado desde afuera
        self.repositorio = repositorio           # D: inyectado desde afuera
 
    def aplicar(self, estudiante: str, descuento: IDescuento, valor_matricula: float) -> float:
        # L: funciona con CUALQUIER clase que implemente IDescuento
        total = valor_matricula - descuento.calcular(valor_matricula)
 
        self.recibo.imprimir(estudiante, descuento, valor_matricula, total)
 
        # I: solo pide documento si el descuento implementa IRequiereSoporte
        if isinstance(descuento, IRequiereSoporte):
            print(f"  Documento requerido: {descuento.documento_soporte()}")
 
        self.repositorio.guardar(estudiante, total)
        return total
 
 
#=====================================================================================
# PRUEBAS
#=====================================================================================
if __name__ == "__main__":
    VALOR_MATRICULA = 5000000
 
    aplicador = AplicadorDescuento(ReciboMatricula(), RepositorioMatricula())
 
    aplicador.aplicar("Laura Ríos",   MatriculaHonor(4.8),           VALOR_MATRICULA)
    aplicador.aplicar("Andrés Mora",  Familiar(2),                   VALOR_MATRICULA)
    aplicador.aplicar("Sofía Díaz",   Convenio("Ecopetrol", 0.25),   VALOR_MATRICULA)
    aplicador.aplicar("Juan Pérez",   Deportista("Fútbol"),          VALOR_MATRICULA)   # O: clase nueva
    aplicador.aplicar("María López",  Convenio("", 0.25),            VALOR_MATRICULA)   # L: no se rompe
 




 #22/10/2026 

 #Patrones de diseño 
 #1. Creacionales 
 # SINGLETON: permite solo una instancia de una clase 

 class configuracion:
    _INSTANCIA = None 
    def __new__(cls):
        if cls._INSTANCIA is None:
            #usamos un metodo de instanciación genérico de onjetos en python:
            cls._INSTANCIA.moneda = "COP"
            cls._INSTANCIA.IVA = 0.19
        return cls._INSTANCIA
    def cambiarIVA(this, nuevoIVA):
        this._INSTANCIA.IVA = nuevoIVA

    #Implementar un metodo que cambie el valor de un atributo (IVA):

    #Implementar un metodo que consulte el valor de un atributo (IVA):

#Realizamos una prueba:
config_cliente1 = configuracion()
config_cliente2 = configuracion()

config_cliente2.cambiarIVA(18)
config_cliente1.cambiarIVA(17)

#como sabemos si son el mismo objeto?
print(config_cliente1 is config_cliente2)

#Que valor imprime?
print(f"El iva quedo en: {config_cliente2.consultarIVA()}")


#2. FACTORY METHOD
class Notificador(ABC):
    @abstractmethod
    def Enviar(this, destino: str, mensaje: str) -> None:
        pass

Class NotificacionEmail(Notificador):
def Enviar(self, destino, mnensaje):
    print(f"se le envio el email {mensaje} a {destino}")

class NotificacionSMS:
    pass 

#PUEDO AGREGAR NUEVOS CANALES DE NOTIFICACION EN EL REGISTRO
_CANALES_NOTIF = {"email":NotificacionEmail, "SMS":NotificacionSMS}

#CLASE FACTORY 
class crearNotificador():

    def crear_notificador(canal:str) -> Notificador:
        try:
            #retornamos instancia de la clase correspondiente:
            return _CANALES_NOTIF[canal1]()
        except KeyError:
            raise ValueError("El valor no existe")

#Como usar el factory metod?
crearNotificador().crear_notificador("emnail").Enviar("nrivasc@gamil.com", "Pedido en camino")




# 3. Builder: permite construir un objeto con partes de los atributos de la clase: parte por parte
class PedidoBuilder:
    def __init__(self, cliente: str):
        self._pedido = Pedido(cliente)

    def agregar_item(self, nombre, precio, cantidad=1):
        self._pedido.items.append((nombre, precio, cantidad))
        return self

    def con_direccion(self, direccion):
        self._pedido.direccion = direccion
        return self

    def con_cupon(self, cupon):
        self._pedido.cupon = cupon
        return self

    def construir(self) -> Pedido:
        if not self._pedido.items:
            raise ValueError("Un pedido necesita al menos un ítem")
        return self._pedido

pedido = (PedidoBuilder("Ana")
          .agregar_item("Teclado", 40.0, 1)
          .agregar_item("Mouse", 15.0, 2)
          .con_direccion("Calle 5 #10-20")
          .construir())
print(pedido.total)  # 70.0


# strategy:

class EstrategiaEnvio(ABC):
    @abstractmethod
    def calcularTiempoEnvio(this, pedido:pedido)->int:
        pass
    @abstractmethod
    }def calcularCostoEnvio(this, pedido:pedido)->float:





     pass

#Esstrategias concretas:
class EnvioEstandar(EstrategiaEnvio):
    def  calcularCostoEnvio(this,pedido):
        #cada estrategia implementa su propia lógica
    def calcularTiempoEnvio_(this, pedido):
            return super().calcularTiempoEnvio(pedido)

class EnvioExpress(EstrategiaEnvio):
    #cada estrategia implementa su propia logica 
         def calcularTiempoEnvio_(this, pedido):
                    return super().calcularTiempoEnvio(pedido)
         
    def  calcularCostoEnvio(this,pedido):
    return super().calcularCostoEnvio(pedido)


#Clase cliente de las estrategias disponibles:
class ClculoEnvio():
    #Aplica el principio SOLID, D:
    #Dependency Injection
    def ___init___(this, tipoEnvio: EstrategiaEnvio):
        this.