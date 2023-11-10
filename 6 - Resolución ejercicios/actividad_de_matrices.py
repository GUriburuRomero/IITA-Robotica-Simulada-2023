matriz = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 3, 1, 1, 2, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
            [1, 1, 1, 1, 1, 1, 1, 7, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],]

#punto 1
filas = len(matriz)
columnas = len(matriz[0])
print("Hay:" , filas)
print("Hay: ", columnas)

#punto 2
print(matriz)
referencia = [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0]
contador = matriz.count(referencia)
print(contador)

#punto 3
nueva_matriz = [list(columnas) for columnas in zip(*matriz)]
print(nueva_matriz)
