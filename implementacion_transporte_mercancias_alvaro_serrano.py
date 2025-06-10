from datetime import datetime

class Manejador_furgoneta:
    pass

class Objetivo:
    pass

class Publicador:
    pass

class Subscriptor:
    pass

class Empresa(Objetivo, Manejador_furgoneta):
   
    _unicaEmpresa = None
   
    def __init__(self, furgonetas: list):

        # Comprobar que todos los elementos sean Furgonetas
        if any(type(furgoneta) != Furgoneta for furgoneta in furgonetas):
            raise TypeError("La lista de furgonetas debe ser de objetos Furgonetas")
        
        # Creamos los atributos
        self.furgonetas = furgonetas
    
    # Metodo para crear una Empresa única
    @classmethod
    def obtener_empresa(cls, furgonetas):
        if not cls._unicaEmpresa :
            cls._unicaEmpresa = cls(furgonetas)
        return cls._unicaEmpresa
    
    # Función que inicia el seguimiento de las furgonetas
    def seguimiento(self):

        return "Método 1 ejecutado"
    
class Furgoneta(Publicador):

    def __init__(self, matricula: str):

        if len(matricula) != 7:
            raise TypeError("La matrícula debe tener 7 caracteres")

        self.matricula = matricula
        self.timestamp = datetime.now()
        self.t = 0.
        self.lat = 0.
        self.lon = 0.
        self.h = 0.

class Cliente(Empresa):
    
    def __init__(self):

        #Empresa.__init__(furgonetas)
        pass
    
if __name__ == "__main__":
    furgoneta1 = Furgoneta('1234BCD')
    furgoneta2 = Furgoneta('0000BBB')
    furgoneta3 = Furgoneta('2005SRD')
    furgoneta4 = Furgoneta('2025PCD')
    furgonetas = [furgoneta1, furgoneta2, furgoneta3, furgoneta4]
    empresa = Empresa.obtener_empresa(furgonetas)
    print("Furgonetas:", empresa.furgonetas)
    print(empresa.seguimiento())
    empresa2 = Empresa.obtener_empresa([furgoneta2, furgoneta4])
    print(empresa is empresa2)