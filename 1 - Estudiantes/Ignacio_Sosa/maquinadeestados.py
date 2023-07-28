import time as tm

semaforo = "Rojo"
contador = 1

while contador <= 3:
    if semaforo == "Rojo":
        print(f"el semaforo esta en color {semaforo}")
        tm.sleep(3)
        semaforo = "Amarillo"
    
    elif semaforo == "Amarillo":
        print(f"el semaforo esta en color {semaforo}")
        tm.sleep(3)
        semaforo = "Verde"
    
    elif semaforo == "Verde":
        print(f"el semaforo esta en color {semaforo}")
        tm.sleep(3)
        semaforo = "Rojo"
        contador += 1

print("finalizo programa")