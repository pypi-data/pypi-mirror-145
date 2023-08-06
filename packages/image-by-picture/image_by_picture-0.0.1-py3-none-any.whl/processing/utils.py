import pathlib
import cv2

# salva imagem no diretório atual
def salve_image(frame_cont, frame):
    name = f'Image-{frame_cont}'
    path = pathlib.Path(__file__).parent.absolute()
    cv2.imwrite(f'{path}\\{name}.png', frame)

# tratamento da imagem
def image_treatment(frame):
    return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
