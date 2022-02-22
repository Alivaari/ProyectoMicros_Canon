# Máscara del video, color verde

# Librerías usadas
import numpy as np #Cambia el nombre de 'numpy' a 'np'
import cv2 as cv #Cambia el nombre de 'cv2' a 'cv'

# Funcion que interpreta RGB de imagen y lo pasa a HSV
# No se está usando aún, así que pueden ignorarla
def rgb_to_hsv(rojo, verde, azul):
    rojo=float(rojo)
    verde=float(verde)
    azul=float(azul)
    r, g, b = rojo/255.0, verde/255.0, azul/255.0
    maximo = max(r, g, b)
    minimo = min(r, g, b)
    rango = maximo-minimo
    if maximo == minimo:
        h = 0
    elif maximo == r:
        h = (60 * ((g-b)/rango) + 180) % 180
    elif maximo == g:
        h = (60 * ((b-r)/rango) + 60) % 180
    elif maximo == b:
        h = (60 * ((r-g)/rango) + 120) % 180
    if maximo == 0:
        s = 0
    else:
        s = (rango/maximo)*255.0
    v = maximo*255.0
    print(str(h),', ',str(s),', ',str(v))
    return [h,s,v]

################################

cap = cv.VideoCapture(0) # Numero en paréntesis indica cuál dispositivo se usa
                         # Si solo hay una cámara, se usa '0' o '-1'
if not cap.isOpened(): #cap.isOpened() es bool, True si hay camara accesada
    print("Cámara no abre") # Si no logra accesar una cámara
    exit()

while True:
    # Captura imagen frame por frame (cuadro de video = 'frame')
    ret, frame = cap.read()
    # Si frame se lee correctamente, ret True
    if not ret:
        print("No se recibe imagen. Exiting ...")
        break
    # Procesado de imagen
    # 'cvtColor()' convierte el perfil de color BGR del frame a perfil HSV
    # Hue(tono del color),Saturation(cuánto del color),Value(valor del brillo)
    # En HSV, los colores se pueden expresar en un rango o intervalo
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
     
    # Rango de tonos verdes en HSV
    lower_green = np.array([35, 35, 140])  # Mínimo rango de color
    upper_green = np.array([65, 255, 255]) # Máximo rango de color
    # Color de prueba      Azules            Rojo           Verde
    # Var 'lower_'      [95, 35, 140]   [155, 35, 140]   [35, 35, 140]
    # Var 'upper_'      [145, 35, 140]   [25, 35, 140]   [85, 35, 140]
 
    # Overlay de la máscara
    # Mantiene pixeles con color dentro del rango, los demás pasan a ser negro
    mask = cv.inRange(hsv, lower_green, upper_green)
     
    # El negro de la máscara tiene valor de 0; al 'multiplicar' por la imagen original
    # Todo lo que no tenga verde (en este caso específico) es removido
    result = cv.bitwise_and(frame, frame, mask = mask)

    # Se abren las ventanas que muestran la imagen original, la máscara (blanco y negro)
    # y la combinación de ambas
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('result', result)
    
    if cv.waitKey(1) == ord('q'): #presionar la tecla 'Q' detiene el programa#
        break


# Al finalizar operacion, todas las ventanas se cierran y se detiene la captura de imagen
cap.release()
cv.destroyAllWindows()
