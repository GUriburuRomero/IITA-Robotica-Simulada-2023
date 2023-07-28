import time as tiempo 

estado = 'rojo'

contador = 1

while contador <= 3:
   if estado == 'rojo':
       print(f"el semaforo esta en {estado}")
       tiempo.sleep(3)
       estado = 'amarillo'

   if estado == 'amarillo':
       print(f"el semaforo esta en {estado}")
       tiempo.sleep(3)
       estado = 'verde'

   if estado == 'verde':
       print(f"el semaforo esta en {estado}")
       tiempo.sleep(3)
       estado = 'rojo'
       contador = contador + 1

  