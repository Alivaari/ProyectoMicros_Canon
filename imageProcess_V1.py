############# Librerías usadas #############

import cv2 as cv #........... Cambia el nombre de 'cv2' a 'cv'
import imutils
import keyboard as kb #...... Cambia el nombre de 'keyboard' a 'kb'
import multiprocessing
import numpy as np #......... Cambia el nombre de 'numpy' a 'np'
import threading
import time

############# Archivos importados #############

#import colorSelection as cs

############# Funciones #############

#"colorSelect" permite al programa cambiar el rango de color que se desea
# Al presionar las teclas indicadas


def colorSelect(a):
    if kb.is_pressed("r"): #.... Detecta si se está presionando la tecla "R"
        a=0 #..................... Valor usado para el rango de "rojos"
    elif kb.is_pressed("g"): #.. Detecta si se está presionando la tecla "G"
        a=1 #..................... Valor usado para el rango de "verdes"
    elif kb.is_pressed("b"): #.. Detecta si se está presionando la tecla "B"
        a=2 #..................... Valor usado para el rango de "azules"
    elif kb.is_pressed("n"): #.. Detecta si se está presionando la tecla "N"
        a=3 #..................... Valor usado para el rango de "negros/grises"
    else:
        a=a #..................... Valor que previamente tenía (no cambia)
    return a #.............. Retorna el valor de la variable 'a'


#############################################################################
###### Función principal ######

def main():
    ######## Variables #########

    color=0
    # Define el rango de colores que se busca, con base en un número
    # color = {0,1,2,3} es, respectivamente {Rojos, Verdes, Azules, Negros/Grises}
    # Valor por defecto en 'color=4' (Negro)
    # -  -  -  -  -  -  -  -  -  -  -  -  -  -

    lower_color1 = np.array ([0, 0, 0])
    upper_color1 = np.array ([90, 25, 127])
    lower_color2 = np.array ([90, 0, 0])
    upper_color2 = np.array ([180, 25, 127])
    # Cuatro valores tipo 'array', c/u definen colores en formato HSV
    # HSV= [Hue,Saturation,Value]. Ver: http://omes-va.com/wp-content/uploads/2019/09/gyuw4.png
        # Hue: tono de color (rojo, verde, azul o combinados), definido de 0° a 180°
        # Saturation: presencia del color, color más "fuerte" a mayor su valor (de 0 a 255)
        # Value: similar al "Brillo", bajos valores indican color más oscuro (de 0 a 255)
    # Las vars definen límites inferior (lower) y superior (upper) de un rango de colores
    #  antes y después del color a buscar (rojo, verde, azul, negro). Para el último, la distribución
    #  del rango es distinto a los otros 3.

    radioMin=10 # Radio mínimo de pixeles detectados en la imagen, es dato del contorno

    #################################################
    
    cap = cv.VideoCapture(1) #......... Numero en paréntesis indica cuál dispositivo se usa
                             #           Si solo hay una cámara, se usa '0' o '-1'
                             # En laptop, conectar camara externa a usb derecha, con número (1)
    time.sleep(2.0)#................... 'sleep' da tiempo a la cámara para abrir (calentar)
    if not cap.isOpened(): #.......... cap.isOpened() es bool, True si hay camara accesada
        print("Cámara no abre") #..... Si no logra accesar una cámara
        exit()
        
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)#... Resolucion en horizontal
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)#.. Resolución en vertical
    cap.set(cv.CAP_PROP_AUTOFOCUS,0)#........ Apaga el enfoque automatico
    cap.set(cv.CAP_PROP_EXPOSURE,-4)#........ Define tiempo fijo de exposición

#    cap.set(3 , 640  ) # width        
#    cap.set(4 , 480  ) # height       
#    cap.set(10, 120  ) # brightness     min: 0   , max: 255 , increment:1  
#    cap.set(11, 50   ) # contrast       min: 0   , max: 255 , increment:1     
#    cap.set(12, 70   ) # saturation     min: 0   , max: 255 , increment:1
#    cap.set(13, 13   ) # hue         
#    cap.set(14, 50   ) # gain           min: 0   , max: 127 , increment:1
#    cap.set(15, -3   ) # exposure       min: -7  , max: -1  , increment:1
#    cap.set(17, 5000 ) # white_balance  min: 4000, max: 7000, increment:1
#    cap.set(28, 0    ) # focus          min: 0   , max: 255 , increment:5

    while True:
        # Captura imagen frame por frame (cuadro de video = 'frame')
        ret, frame = cap.read()
        # Si frame se lee correctamente, ret True
        if not ret:
            print("No se recibe imagen. Saliendo ...")
            break

        ###### Procesado de imagen ######
        # 'cvtColor()' convierte el perfil de color BGR del frame a perfil HSV
        # Hue(tono del color),Saturation(cuánto del color),Value(valor del brillo)
        # En HSV, los colores se pueden expresar en un rango o intervalo

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # 'hsv' es la imagen con colores definidos
        #                                             por HSV y no RGB

        ###### Selección de color ######
        color=colorSelect(color) # Determina qué color está eligiendo el usuario
        if color == 0: #................................ Define rangos de "Rojo"
            lower_color1 = np.array ([0, 100, 140])
            upper_color1 = np.array ([15, 255, 255])
            lower_color2 = np.array ([165, 100, 140])
            upper_color2 = np.array ([180, 255, 255])
        elif color == 1: #.............................. Define rangos de "Verde"
            lower_color1 = np.array ([45, 100, 140])
            upper_color1 = np.array ([60, 255, 255])
            lower_color2 = np.array ([60, 100, 140])
            upper_color2 = np.array ([75, 255, 255])
        elif color == 2: #.............................. Define rangos de "Azul"
            lower_color1 = np.array ([105, 100, 140])
            upper_color1 = np.array ([120, 255, 255])
            lower_color2 = np.array ([120, 100, 140])
            upper_color2 = np.array ([135, 255, 255])
        elif color == 3: #.............................. Define rangos de "Negro"
            lower_color1 = np.array ([0, 0, 0])
            upper_color1 = np.array ([90, 25, 127])
            lower_color2 = np.array ([90, 0, 0])
            upper_color2 = np.array ([180, 25, 127])
        
        
        ###### Overlay de la máscara ######
        # Mantiene pixeles con color dentro del rango (los muestra como blanco),
        #  los demás pasan a ser negro
        mask = cv.inRange(hsv, lower_color1, upper_color1)#.... Máscara de medio rango (parte inferior)
        mask2 = cv.inRange(hsv, lower_color2, upper_color2) #.. Máscara de medio rango (parte superior)
         
        # El negro de la máscara tiene valor de 0; al 'multiplicar' por la imagen original
        # Todo lo que no tenga el color en el rango de colores (en este caso específico) es removido

        fullMask=cv.bitwise_or(mask, mask2)
        # Operación OR de los pixeles de las máscaras con pixeles B/N. Combina las dos máscaras
        #   y muestra los pixeles blancos si estos son blancos en al menos una de las máscaras
        # Sea pixel de coords (x,y) en 'mask' y pixel2 de coords (x2,y2) en 'mask2',
        #  con x=x2=X, y=y2=Y, Color negro es 0 y el blanco es 1, se tiene la tabla de verdad:
        #
        #           Pixel(X, Y)  |  0  |  0  |  1  |  1  |
        #           ---------------------------------------
        #           Pixel2(X, Y) |  0  |  1  |  0  |  1  |
        #        ------------------------------------------
        #        Pixel OR Pixel2 |  0  |  1  |  1  |  1  |
        #
        #
        
        
        result = cv.bitwise_and(frame, frame, mask = fullMask)
        # Se toma la máscara B/N y se le aplica un AND con la captura original. Si el pixel (x,y)
        #  de 'fullMask' es blanco, el pixel (x,y) de 'result' toma el color del pixel (x,y) de
        #  'frame'


        ###### Coordenadas media de los pixeles ######

        # 'kernel' define un área de pixeles blancos ('np.ones') de 5x5, con datos de tipo 'uint8' (similar a 'long int')
        # 'morphologyEx' procesa la imagen de 'fullMask' según operador 'cv.MORPH...' en areas definidas por 'kernel'
        # 'cv.MORPH_OPEN' realiza "opening" y "cv.MORPH_CLOSE" realiza "closing"
        
        kernel=np.ones((5,5), np.uint8)
        fullMask=cv.morphologyEx(fullMask, cv.MORPH_OPEN, kernel)
        fullMask=cv.morphologyEx(fullMask, cv.MORPH_CLOSE, kernel)

        # 'findContours' encuentra los contornos de una copia de la imagen en 'fullMask' (dada por 'fullMask.copy()')
        #   y retorna el contorno indicado por el operador ('cv.RETR_EXTERNAL' en este caso) ya sea completo o simple
        #   (operador 'cv.CHAIN_APPROX_SIMPLE' retorna contorno simple)
        # 'imutils.grab_contours' procesa los contornos encontrados y lo guarda en 'contorno'
        # 'centro' es el punto central del contorno, similar al promedio de las coordenadas de todos
        #   los pixeles de la imagen
        
        contorno = cv.findContours(fullMask.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        contorno = imutils.grab_contours(contorno)
        centro = None

        if len(contorno) > 0:#.......... Comprobar la existencia de un contorno
            # 'max' toma el mayor contorno de la lista 'contorno', al comparar sus areas según se indica con 'key=cv.contourArea'
            # 'cv.minEnclosingCircle(c)' obtiene el mínimo círculo capaz de encerrar el contorno 'c'; su ubicación en
            #    la imagen es guardada en el punto '(x, y)', y su radio se guarda en 'radio'
            
            c = max(contorno,key=cv.contourArea)
            ((x, y), radio) = cv.minEnclosingCircle(c)

            # 'cv.moments(c)' encuentra el equivalente digital del momento de inercia de una figura, con base en la
            #    cantidad y características de pixeles. Cada pixel posee un "peso" proporcional a su intensidad y
            #    la función calcula los momentos a partir de esta equivalencia.
            # El centroide "C" de una figura se puede obtener si se conocen sus momentos. Se sigue una lógica similar
            #    para encontrar el centroide del contorno 'c', cuyo valor son coordenadas (Cx,Cy)
            # Se tiene:      Cx=M10/M00        Cy=M01/M00
            # A 'centro' se le da el valor del centroide (Cx,Cy)
                        
            moments = cv.moments(c)
            centro=(int(moments["m10"]/moments["m00"]),int(moments["m01"]/moments["m00"]))

            if radio > radioMin: # El círculo debe tener un tamaño mayor a 'radioMin'
                
                # 'cv.circle' dibuja un circulo en la captura 'frame' con centro en '(x,y)' ('x' y 'y' deben convertirse
                #    a enteros, dado que no existen 0.5 pixeles, por ejemplo), radio dado por 'radio' (también convertido
                #    a entero, de color (R,G,B) y grosor de línea 2
                # El 2do 'cv.circle' dibuja un punto en el centro. Como su grosor se indica con '-1' significa que se
                #    rellena con el color dado para este.
                
                cv.circle(frame,(int(x),int(y)),int(radio),(0,255,255),2)
                cv.circle(frame, centro, 5, (0, 0, 255), -1)
                print(centro)
        
        


        ###### Mostrar imágenes obtenidas ######
        # Se abren las ventanas que muestran la imagen original, la máscara (blanco y negro)
        #   y la combinación de ambas (su fin es para test e ilustrativo)
        cv.imshow('frame', frame)
        #cv.imshow('mask', mask)
        #cv.imshow('mask2',mask2)
        #cv.imshow('result', result)
        cv.imshow('fullMask',fullMask)
        #cv.imshow('opening',opening)
        #cv.imshow('closing',closing)



        ###### Rotura del ciclo ######
        # Forma de detener la captura de imagen (sujeto a cambios)
        if cv.waitKey(1) == ord('q'): #presionar la tecla 'Q' detiene el programa#
            break

    # Al finalizar operacion, todas las ventanas se cierran y se detiene la captura de imagen
    cap.release()
    cv.destroyAllWindows()    

#################################################################

###### Ejecución del archivo ######

main()
