import pytest

from implementacion_transporte_mercancias_alvaro_serrano import Empresa, Camion, Manejador_camion, Manejador_estadisticos, Manejador_umbral, Manejador_temperatura, Objetivo, CoordenadasGD

# -------------------------------
# Pruebas con pytest
# -------------------------------

def test_raises_exception_on_Empresa():
    s1 = Empresa.obtener_empresa()
    with pytest.raises(TypeError):
        s2 = Empresa()
        s1 is s2

def test_raises_exception_on_matricula():
    with pytest.raises(TypeError):
        Camion("C1")

def test_singleton():
    s1 = Empresa.obtener_empresa()
    s2 = Empresa.obtener_empresa()
    # s2 = Camion('2345VDF')
    assert s1 is s2

def test_observer(capfd):
    singleton = Empresa.obtener_empresa()
    camion = Camion("1234BBB")
    singleton.añadir_camion(camion)
    singleton.camiones[0].notificarSuscriptores()  # Verifica que no lanza errores 
    assert "Datos recibidos del camión" in out


def test_chain_of_responsibility():
    datos = Camion('0000AAA')
    handler = Manejador_estadisticos(Manejador_temperatura(Manejador_umbral()))
    handler.manejador(datos)
    assert True

def test_adapter():
    coordenadas = CoordenadasGD(lat=37.5, lon=-1.2)
    adaptador = Objetivo(coordenadas)
    codigo = adaptador.conversor()
    assert codigo.startswith("OCL(")
