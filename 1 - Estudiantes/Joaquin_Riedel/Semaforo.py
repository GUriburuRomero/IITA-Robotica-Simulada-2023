mensaje= "Semaforo"
print(mensaje)
import time as tm
Estado= "Rojo"
contador= 0
while contador<=3:
    if Estado== "Rojo":
     print(str("Detengase, el semaforo se encuentra en Rojo"))
    tm.sleep(2)
    Estado= "Amarillo"
    if Estado== "Amarillo":
       print(str("Amarillo: Preparese para el proximo cambio"))
       tm.sleep(1)
    Estado="Verde"
    if Estado=="Verde":
        print("Avance, estamos en verde :D")
        tm.sleep(2)
    Estado== "Rojo"
    print("Detengase, el semaforo se encuentra en Rojo")
    contador=contador+1
#SE DETENDRA A LA TERCERA O CUARTA VEZ