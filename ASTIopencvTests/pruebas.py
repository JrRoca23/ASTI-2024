from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (1920, 1080)  # Establece la resolución de la imagen
camera.start_preview()  # Inicia la vista previa de la cámara

# Espera un momento para que la cámara se ajuste
time.sleep(2)

# Captura una imagen y la guarda como "test.jpeg"
camera.capture("test.jpeg")
print("Imagen guardada como test.jpeg")

# Detiene la vista previa y libera los recursos de la cámara
camera.stop_preview()
camera.close()