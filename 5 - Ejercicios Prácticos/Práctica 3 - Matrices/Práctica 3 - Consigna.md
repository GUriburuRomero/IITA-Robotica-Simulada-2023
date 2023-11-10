# Parte 1 - Columnas y filas

- a) Utilizando la siguiente matriz, realice un programa el cual cuente la cantidad de filas y columnas que contenga la misma.

- b) Realice un programa tal que pueda identificar una fila nula (compuesta solamente por ceros) y la muestre en consola. Adicionalmente, intente contar todas las filas que sean nulas.

- c) Realice un programa el cual transforme los elementos de las columnas en una fila, y añada esa fila a otra matriz. Mostrar al final de la ejecución la matriz obtenida.

    matriz = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 3, 1, 1, 2, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
              [1, 1, 1, 1, 1, 1, 1, 7, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],]

# Parte 2 - Filtrado de Matrices

- A) Utilizando la siguiente matriz, elimine todas las filas y columnas que sean nulas. Puede utilizar cualquier método. Consejo: Puede utilizar una matriz auxiliar que será la que presentará finalmente.

```
# Matriz para utilizar

matriz = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

```