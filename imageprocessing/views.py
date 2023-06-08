import os
import numpy as np
import cv2
from django.conf import settings
from django.shortcuts import render
from .models import Image

def process_image(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES['image']
            image_data = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            # Ejemplo de procesamiento de imagen: Convertir a escala de grises
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Guardar la imagen procesada en la base de datos
            processed_image = Image.objects.create(name=image_file.name, image_file=image_file)
            processed_image.save()

            # Guardar la imagen procesada en la carpeta de medios
            destination_path = os.path.join(settings.MEDIA_ROOT, processed_image.image_file.name)
            cv2.imwrite(destination_path, gray_image)

            context = {'processed_image': processed_image}
            return render(request, 'result.html', context)

        except Exception as e:
            error_message = str(e)
            context = {'error_message': error_message}
            return render(request, 'error.html', context)

    return render(request, 'process.html')
