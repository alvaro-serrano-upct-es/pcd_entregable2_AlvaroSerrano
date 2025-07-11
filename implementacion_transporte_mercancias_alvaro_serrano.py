from datetime import datetime
import asyncio
import random
import numpy as np
import functools

# ------- Manejador de la cadena de responsabilidades -------
class Manejador_camion:
    
    def __init__(self, successor=None):
        self.successor = successor
    
    def manejador(self, camion):
        if self.successor:
            self.successor.manejador(camion)
    
# Se definen las clases herederas de Manejador_camion. Cada uno cumple una función diferente
class Manejador_estadisticos(Manejador_camion):     # Calcula la media de la temperatura y la humedad en el último minuto
    def manejador(self, camion):
        print(" ↳ Estadísticos:")
        if len(camion.t) >= 12 and len(camion.h) >= 12:

            tem_ult_min = camion.t[-12:]
            hum_ult_min = camion.h[-12:]

            # Media de la temperatura del último minuto
            media_t = functools.reduce(lambda x, y: x+y, tem_ult_min)/12
            # Media de la humedad del último minuto
            media_h = functools.reduce(lambda x, y: x+y, hum_ult_min)/12
            # Desviación típica de la temperatura del último minuto
            desv_tem_ult_min = np.sqrt(sum(map(lambda x: (x - media_t)**2, tem_ult_min))/12)
            # Desviación típica de la humedad del último minuto
            desv_hum_ult_min = np.sqrt(sum(map(lambda x: (x - media_h)**2, hum_ult_min))/12)

        else:

            media_t = functools.reduce(lambda x, y: x+y, camion.t)/len(camion.t)
            media_h = functools.reduce(lambda x, y: x+y, camion.h)/len(camion.h)
            desv_tem_ult_min = np.sqrt(sum(map(lambda x: (x - media_t)**2, camion.t))/len(camion.t))
            desv_hum_ult_min = np.sqrt(sum(map(lambda x: (x - media_h)**2, camion.h))/len(camion.h))
        
        print("     ·Temperatura media último minuto: ", round(media_t, 2))
        print("     ·Humedad media último minuto: ", round(media_h, 2))
        print("     ·Desviación típica temperatura último minuto: ", round(desv_tem_ult_min, 2))
        print("     ·Desviación típica humedad último minuto: ", round(desv_hum_ult_min, 2))

        super().manejador(camion)

class Manejador_temperatura(Manejador_camion):       # Comprueba que la temperatura no supere un límite que hemos establecido en 7,5
    def manejador(self, camion):
        print("  ↳ Alerta:")
        if camion.t[-1] > 7.5:
            print("      ¡¡¡temperatura supera el umbral de 7,5 grados!!!")
        else:
            print("      ·Ninguna alerta")
        valores = list(filter(lambda x: x > 7.5, camion.t))
        print(f"      ·Valores que han superado el umbral: {valores}")
        super().manejador(camion)

class Manejador_umbral(Manejador_camion):  # Revisa que en los últimos 30 segundos la temperatura y la humedad no haya variado más de 2º
    def manejador(self, camion):
        print("   ↳ Variación: ")
        if (len(camion.t) < 6 or len(camion.h) < 6):
            print("       ·Ninguna variación significativa registrada")
        else:
            if abs(camion.t[-6] - camion.t[-1]) > 2:
                print(f"       ·La variación de temperatura supera los 2 grados -> alcanza los {int(abs(camion.t[-6] - camion.t[-1]))} grados de variación")
            if abs(camion.h[-6] - camion.h[-1]) > 2:
                print(f"       ·La variación de humedad supera los 2 grados -> alcanza los {int(abs(camion.h[-6] - camion.h[-1]))} grados de variación")
            if not (abs(camion.t[-6] - camion.t[-1]) > 2 or abs(camion.h[-6] - camion.h[-1]) > 2):
                print("       ·Ninguna variación significativa registrada")
        print()
        super().manejador(camion)

# ------- Clase Objetivo del Adaptador -------
class CoordenadasGD: # Clase abstraida para auxiliar a la clase objetivo
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class Objetivo:     # La clase convierte de coordenadas GD a OCL con la formula matemática que se usa para ello

    def __init__(self, coordenadas_gd):
        self.coordenadas_gd = coordenadas_gd

    def conversor(self):
        a = 6378137.0       # Constante de World Geodetic System 1984 (WGS 84) 
        b = 6356752.314245  # Constante de World Geodetic System 1984 (WGS 84) 
        h = 1000
        phi = self.coordenadas_gd.lat * np.pi/180
        lam = self.coordenadas_gd.lon * np.pi/180
        N = (a**2) / (((a**2) * np.cos(phi)**2) + ((b**2) * np.sin(phi)**2))**(1/2)
        x = (N + h) * np.cos(phi) * np.cos(lam)
        y = (N + h) * np.cos(phi) * np.sin(lam)
        z = ((N * (b**2/a**2)) + h) * np.sin(phi)
        coord = list(map(lambda x: round(x, 2), [x, y, z])) # Utilizamos map para redondear todos los terminos de las coordenadas
        # Coordenas transformadas
        return f"OCL({coord[0]},{coord[1]},{coord[2]})"

# ------- Clases Suscriptor y Publicador del Observador -------
class Suscriptor:
    
    def actualizar(self, camion, datos):

        # Añadimos los valores nuevos si no salen de un umbral definido
        camion.timestamp.append(datetime.now())
        if datos[0] < 15 and datos[0] > -10:
            camion.t.append(datos[0])
        if datos[1] < 60.0 and datos[1] > 20.0:
            camion.lat.append(datos[1])
        if datos[2] < 6.0 and datos[2] > -6.0:
            camion.lon.append(datos[2])
        if datos[3] < 90 and datos[3] > 60:
            camion.h.append(datos[3])
        coordenadas = CoordenadasGD(camion.lat[-1], camion.lon[-1]) #print(f'{camion.lat[-1]}, {camion.lon[-1]}')
        adaptador = Objetivo(coordenadas)
        camion.coordenadas.append(adaptador.conversor())
        print(f"[{camion.timestamp[-1]}] \nDatos recibidos del camión {camion.matricula}: (Coordenadas: {camion.coordenadas[-1]}, Temperatura: {camion.t[-1]}, Humedad: {camion.h[-1]})")

class Publicador:
    
    def __init__(self):
        self.suscriptores= []

    def alta(self, suscriptor):
        if suscriptor not in self.suscriptores:
            self.suscriptores.append(suscriptor)

    def baja(self, subscriptor):
        self.suscriptores.remove(subscriptor)

    def notificarSuscriptores(self):
        for suscriptor in self.suscriptores:
            suscriptor.actualizar(self, self.obtener_datos())
            suscriptor.procesador.manejador(self)

# ------- Clases principales: Camion, Empresa, Cliente -------
class Camion(Publicador):   # Abstraemos una clase que representa un camion y que guardará los valores de estos cuando se vayan actualizando.

    def __init__(self, matricula: str):

        if len(matricula) != 7:
            raise Exception("La matrícula debe tener 7 caracteres.")

        super().__init__()
        self.matricula = matricula
        self.timestamp = [datetime.now()]
        self.t = [0.0]
        self.lat = [40.41698]
        self.lon = [-3.70361]
        self.h = [75.0]
        self.coordenadas = ["OCL(,)"]

    def obtener_datos(self):

        temperatura = random.uniform(-1.5, 2.0)
        lat = random.uniform(-2.0, 2.0)
        lon = random.uniform(-0.5, 0.5)
        humedad = random.uniform(-2.0, 2.0) 
        return [round(self.t[-1] + temperatura, 2), round(self.lat[-1] + lat, 2), round(self.lon[-1] + lon, 2), round(self.h[-1] + humedad, 2)]

class Empresa(Suscriptor): # La clase Empresa es un singleton para que solo haya una sola instancia 
   
    _unicaEmpresa = None
   
    def __init__(self):

        if Empresa._unicaEmpresa is not None:
            raise Exception("¡Esta clase es un Singleton! Utilice 'obtener_empresa()' para obtener la instancia.")
        
        # Creamos los atributos
        super().__init__()
        self.camiones = []
        self.procesador = Manejador_estadisticos(Manejador_temperatura(Manejador_umbral()))
    
    # Metodo para crear una Empresa única
    @classmethod
    def obtener_empresa(cls):
        if not cls._unicaEmpresa :
            cls._unicaEmpresa = cls()
        return cls._unicaEmpresa
    
    def añadir_camion(self, camion: Camion):
        self.camiones.append(camion)
        camion.alta(self)
    
    # Función que inicia el seguimiento de los camiones. Usa asyncio para que el seguimiento sea cada 5 segundo
    async def seguimiento(self):
        cont = 1
        while True:
            await asyncio.sleep(5)
            print(f"----------------- {cont}º Datos recibidos -----------------")
            for camion in self.camiones:
                camion.notificarSuscriptores()
            cont += 1

class Cliente(Empresa): # La clase empresa será la que sirva de intermediaria entre la empresa y el cliente a la hora de hacer el seguimiento
    
    def __init__(self):

        self.empresa = Empresa.obtener_empresa()

    async def seguir(self): # Ejecuta la función asyncio

        await asyncio.gather(self.empresa.seguimiento())

if __name__ == "__main__":
    # Ejemplos de camiones
    camion1 = Camion('1234BCD')
    camion2 = Camion('0000BBB')
    camion3 = Camion('2005SRD')
    camion4 = Camion('2025PCD')
    # Obtener empresa
    empresa = Empresa.obtener_empresa()
    # Añadimos los camiones a la empresa
    empresa.añadir_camion(camion1)
    empresa.añadir_camion(camion2)
    # empresa.añadir_camion(camion3)
    # empresa.añadir_camion(camion4)
    # print("Camiones:", empresa.camiones)

    # Añadimos un cliente y empezamos el seguimiento
    cliente1 = Cliente()
    asyncio.run(cliente1.seguir())