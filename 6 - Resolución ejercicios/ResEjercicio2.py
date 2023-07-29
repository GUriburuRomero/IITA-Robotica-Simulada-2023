""" Máquina de Estados - Simulación de Semáforo """

import time as tm

state = 'rojo'
count = 0

while count < 3:
    if state == "rojo":
        print(f'Estoy en {state}')
        state = "amarillo"
        tm.sleep(3)

    elif state == "amarillo":
        print(f'Ahora estoy en {state}')
        state = "verde"
        tm.sleep(2)

    elif state == "verde":
        print(f'¡Corre! Ahora estoy en {state}')
        state = 'rojo'
        tm.sleep(2)
        count += 1
