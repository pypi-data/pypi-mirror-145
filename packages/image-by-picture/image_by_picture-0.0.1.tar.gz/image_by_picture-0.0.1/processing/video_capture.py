import imutils
import cv2
from processing import utils

# processamento da imagem
def processing_image():
    # inicializa a trasmissão do video
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    frame_cont = 0
    while True:
        frame_cont += 1
        _, frame = video_capture.read()
        if not _:
            break

        # redimensiona o tamanho do frame para acelerar o processamento e mostra o frames
        frame = imutils.resize(frame, width=320)
        cv2.imshow('Webcam_Image', frame)

        if frame_cont == 1:
            utils.salve_image(frame_cont, frame)
        elif frame_cont == 50:
            # converte as cores para tons de cinza
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #salvar imagem alterada
            utils.salve_image(frame_cont, utils.image_treatment(frame))
            video_capture.release()
            cv2.destroyWindow('Webcam_Image')
            break


