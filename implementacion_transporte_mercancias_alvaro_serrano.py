class Singleton:
   
    _unicaInstancia = None
   
    def __init__(self):
        self.atributo1 = "Valor1"
        self.atributo2 = "Valor2"
    
    @classmethod
    def obtener_instancia(cls):
        if not cls._unicaInstancia :
            cls._unicaInstancia = cls()
        return cls._unicaInstancia
    
    def metodo1(self):
        return "Método 1 ejecutado"
    
    def metodo2(self):
        return "Método 2 ejecutado"
    
if __name__ == "__main__":
# Uso del patrón Singleton con atributos y métodos
 singleton = Singleton.obtener_instancia()
 # Acceso a los atributos
 print("Atributo 1:", singleton.atributo1)
 print("Atributo 2:", singleton.atributo2)
 # Llamada a los métodos
 print(singleton.metodo1())
 print(singleton.metodo2())
 # Ambas instancias son la misma
 singleton2 = Singleton.obtener_instancia()
 print(singleton is singleton2) # Devuelve True