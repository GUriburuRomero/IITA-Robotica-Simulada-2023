import time as tm
estado = 'rojo'
contador= 1

while contador <= 3:
    if estado == 'rojo':
        print(f'No avanzo porque esta en {estado}')
        tm.sleep(2)
        estado='amarillo'

    if estado == 'amarillo':
        print(f'Espero porque esta en  {estado}')
        tm.sleep(2)
        estado='verde'

    if estado == 'verde':
        print(f'Avanzo porque esta en {estado}')
        tm.sleep(3)
        estado='rojo'
        contador=contador+1






