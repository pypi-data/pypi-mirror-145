def cut(reducesize=0, figSelect='', kernelSize=0, ApplyTimes=0):
    import numpy as np
    import cv2
    from imutils import contours
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    import promptlib
    import os
    import logging
    import subprocess
    logging.basicConfig(filename="cutmessages.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    Tk().withdraw()
    filename = askopenfilename()
    if not filename:
        return
    else:
        # Carga la imagen en escala de grises, evalúa la reducción de tamaño de cada una.
        # Recomendable solo bajar la escala 1 vez.
        # Recomendable no bajar la escala si la imagen es muy pequeña.
        if reducesize == 0:
            image = cv2.imread(filename)
        elif reducesize == 1:
            image = cv2.imread(filename, cv2.IMREAD_REDUCED_COLOR_2)
        elif reducesize == 2:
            image = cv2.imread(filename, cv2.IMREAD_REDUCED_COLOR_4)
        elif reducesize == 3:
            image = cv2.imread(filename, cv2.IMREAD_REDUCED_COLOR_8)
        else:
            pass
        # Se aplica el filtro Gaussiano y detección de bordes Canny.
        orig = image.copy()
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(imgray, (3, 3), 0)
        canny = cv2.Canny(blur, 120, 255, 1)
        close = None
        if figSelect == 'square':
            # Recomendado tener un Kernel de 3x3, con 3 iteraciones si se reduce el tamaño 1 vez.
            # Recomendado tener kernel de 5x5, con 4 iteraciones si no se reduce el tamaño.
            if kernelSize == 0:
                if reducesize == 0:
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
                elif reducesize == 1:
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
                else:
                    pass
            else:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernelSize, kernelSize))
            if ApplyTimes == 0:
                if reducesize == 0:
                    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=4)
                elif reducesize == 1:
                    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=3)
                else:
                    pass
            else:
                close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=ApplyTimes)

        elif figSelect == 'circle':
            # Recomendado tener un Kernel de 5x5, con 7 iteraciones si se reduce el tamaño 1 vez.
            if kernelSize == 0:
                if reducesize == 0:
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
                elif reducesize == 1:
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                else:
                    pass

            else:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernelSize, kernelSize))
            if ApplyTimes == 0:
                if reducesize == 0:
                    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=4)
                elif reducesize == 1:
                    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=7)
                else:
                    pass
            else:
                close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=ApplyTimes)

        elif figSelect == 'triangle':
            # Recomendado tener un Kernel de 5x5, con 6 iteraciones si se reduce el tamaño 1 vez.
            if kernelSize == 0:
                if reducesize == 0:
                    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
                elif reducesize == 1:
                    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
                else:
                    pass
            else:
                kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (kernelSize, kernelSize))
            if ApplyTimes == 0:
                if reducesize == 0:
                    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=6)
                elif reducesize == 1:
                    close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=6)
                else:
                    pass
            else:
                close = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel, iterations=ApplyTimes)

        # Encuentra los contornos de las imágenes.
        # Inicia una variable para una lista de contornos.
        contour_list = []
        # Se inicializa una variable para contabilizar las imagenes.
        ROI_number = 0
        # Se usa la función de findContours para detectar contornos de la imagen, la función RETR_EXTERNAL devuelve solo los contornos externos si encuentra otros.
        # La función de CHAIN_APPROX_SIMPLE une puntos de los bordes de una imagen para consumir menos espacio de memoria.
        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts, _ = contours.sort_contours(cnts, method="left-to-right")
        prompt = promptlib.Files()
        directory = prompt.dir()
        for c in cnts:
            # Se obtiene el rectángulo que genera cada contorno.
            x, y, w, h = cv2.boundingRect(c)

            # Encuentra la sección de interés del contorno.
            roi = image[y:y + h, x:x + w]

            # Dibuja la caja de contorno y se corta utilizando Numpy
            # Un rectángulo se dibuja sobre cada región de interés (los contornos detectados).
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
            ROI = orig[y:y + h, x:x + w]
            cv2.imwrite(f"{directory}/" + "CUT_{}.jpg".format(ROI_number), ROI)
            contour_list.append(c)
            ROI_number += 1

        logger.info("Contornos detectados: {}".format(len(contour_list)))
        cv2.waitKey()
        subprocess.Popen(f'explorer /select, {directory}')
        logger.info("Eliminar las imagenes no candidatas para el entrenamiento.")
        cv2.waitKey()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    cut()
