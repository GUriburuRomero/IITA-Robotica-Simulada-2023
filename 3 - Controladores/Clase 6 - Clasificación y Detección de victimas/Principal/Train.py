# Programa para entrenar nuestro modelo de Predicción

from ultralytics import YOLO
import os

ruta = os.getcwd()

model = YOLO('yolov8n-cls.pt')

model.train(data=(str(ruta)+"/Yolo_directory"), epochs=100, imgsz=500)