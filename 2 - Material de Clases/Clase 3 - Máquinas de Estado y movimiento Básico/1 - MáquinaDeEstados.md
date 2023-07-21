# Máquinas de Estado

Dentro de la simulación, contamos con el la sentencia TimeStep, la cual indica la velocidad en milisegundos sobre la cual se actualizarán los valores de nuestros sensores y motores.

En caso de que se necesitara que un sensor actúe de manera independiente a la velocidad de actualización, y que nuestro robot ejecute cierta acción solamente si el valor de un sensor es específico, es necesario utilizar una máquina de estados.

## ¿Cómo definir una máquina de estados?

La respuesta es utilizando una o más variables para definir los estados que tendremos, y utilizando estructuras de control (if - elif - else).

Considerando el siguiente Pseudocódigo:

    miEstado = Rojo
    contador = 1

    Mientras contador <= 3:
        Si miEstado == Rojo:
            Ejecutar (nuestras_instrucciones)
            miEstado = Azul
        
        Si miEstado == Azul:
            Ejecutar (otras_Instrucciones)
            miEstado = Rojo
            contador = contador + 1

El Pseudocódigo anterior declara una variable la cual nos servirá como punto de partida y se evaluará hasta que el contador sea 3.

Posteriormente, en caso de que la variable adquiera un valor u otro, ejecutará cierta pieza de instrucciones que nosotros querramos, para luego tomar otro valor y producir un "cambio de estado".

En este sentido, se logra apreciar que nosotros controlamos en que momento cambiará de un estado a otro, y que instrucciones ejecutará en cada uno que definimos.
