import numpy as np
import cv2 as cv

img = cv.imread("C:/Users/GERARDO URIBURU/Desktop/Imagen.png") #Obtenemos la imagen desde el directorio


def classifyVictim(img):
    '''Permite clasificar la imagen'''
    img = cv.resize(img, (100, 100)) # Redimensionamis la imagen
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Convertimos la imagen a escala de grises para mejor detección
    thresh1 = cv.threshold(gray, 100, 255, cv.THRESH_BINARY_INV)[1]
    conts, h = cv.findContours(thresh1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv.boundingRect(conts[0])

    letter = thresh1[y:y + h, x:x + w]
    letter = cv.resize(letter, (100, 100), interpolation=cv.INTER_AREA)

    areaWidth = 20
    areaHeight = 30

    areas = {
        "top": ((0, areaHeight),(50 - areaWidth // 2, 50 + areaWidth // 2)),
        "middle": ((50 - areaHeight // 2, 50 + areaHeight // 2), (50 - areaWidth // 2, 50 + areaWidth // 2)),
        "bottom": ((100 - areaHeight, 100), (50 - areaWidth // 2, 50 + areaWidth // 2 ))
        }

    images = {
        "top": letter[areas["top"][0][0]:areas["top"][0][1], areas["top"][1][0]:areas["top"][1][1]],
        "middle": letter[areas["middle"][0][0]:areas["middle"][0][1], areas["middle"][1][0]:areas["middle"][1][1]],
        "bottom": letter[areas["bottom"][0][0]:areas["bottom"][0][1], areas["bottom"][1][0]:areas["bottom"][1][1]]
        }

    counts = {}
    acceptanceThreshold = 50

    for key in images.keys():
        count = 0
        for row in images[key]:
            for pixel in row:
                if pixel == 255:
                    count += 1
        counts[key] = count > acceptanceThreshold

    letters = {
        "H":{'top': False, 'middle': True, 'bottom': False},
        "S":{'top': True, 'middle': True, 'bottom': True},
        "U":{'top': False, 'middle': False, 'bottom': True}
        }

    for letterKey in letters.keys():
        if counts == letters[letterKey]:
            finalLetter = letterKey
            break

    return finalLetter


print(classifyVictim(img))
cv.waitKey(1) # Función propia de OpenCV