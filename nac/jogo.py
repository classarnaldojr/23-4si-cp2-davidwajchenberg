import cv2
import numpy as np
import time
import math

def escreve_texto(img, text, origem, color):
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(img, text, origem, font, 1, color, 2, cv2.LINE_AA)

esquerda = 0
direita = 0

vc = cv2.VideoCapture("pedra-papel-tesoura.mp4")

while vc.isOpened():
    ret, img = vc.read()

    sizex = 100
    sizey = 40
    color = (0,0,0)

    if img is None:
       cv2.destroyWindow('Pedra Papel e Tesoura')
       vc.release()   
    else:
        img = cv2.resize(img, (800, 600))

        crop_img = img[100:600, 100:450]
        crop_img1 = img[100:600, 350:800]

        grey1 = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        grey2 = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)

        k_size = (35, 35)
        filtro_blur1 = cv2.GaussianBlur(grey1, k_size, 0)
        filtro_blur2 = cv2.GaussianBlur(grey2, k_size, 0)

        _, thresh = cv2.threshold(filtro_blur1, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        _, thresh1 = cv2.threshold(filtro_blur2, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(thresh.copy(), \
            cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        contours1, hierarchy1 = cv2.findContours(thresh1.copy(), \
            cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        max_area = -1
        max_area1 = -2
        aux1 = None
        aux12 = None

        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > max_area:
                aux1 = contours[i]
                max_area = area

        for i in range(len(contours1)):
            area1 = cv2.contourArea(contours1[i])
            if area1 > max_area1:
                aux12 = contours1[i]
                max_area1 = area1
       

        cnt = aux1

        def get_center_of_mass(cnt):
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            else:
                M["m00"] = 0.1
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            return (cx, cy)

        cx, cy = get_center_of_mass(cnt)
        cx1, cy1 = get_center_of_mass(aux12)


        drawing = np.zeros(crop_img.shape,np.uint8)
        drawing1 = np.zeros(crop_img1.shape,np.uint8)
        
        def get_gesture_text(max_area):
            if max_area > 14500 and max_area < 17000:
                return "PAPEL"
            elif max_area > 11500 and max_area < 14000:
                return "PEDRA"
            elif max_area < 11500 and max_area > 6000:
                return "TESOURA"
            else:
                return ""

        txt = get_gesture_text(max_area)
        escreve_texto(img, txt, (100, 100), (0, 255, 0))

        txt1 = get_gesture_text(max_area1)
        escreve_texto(img, txt1, (500, 100), (0, 255, 0))


        moves_dict = {
        "PEDRA": "TESOURA",
        "PAPEL": "PEDRA",
        "TESOURA": "PAPEL"
        }

        if txt == txt1:
            escreve_texto(img, "Empate", (320, 40), (0, 0, 255))
        elif moves_dict[txt] == txt1:
            escreve_texto(img, "Jogador da esquerda venceu", (150, 40), (255, 0, 0))
            esquerda += 1
        else:
            escreve_texto(img, "Jogador da direita venceu", (150, 40), (0, 255, 0))
            direita += 1


        
        def calcular_pontuacao(jogador):
            return round((jogador / 100) * 1.17)

        esquerda_pct = calcular_pontuacao(esquerda)
        direita_pct = calcular_pontuacao(direita)

        texto = "esquerdauerda: {} X direitaeita: {}".format(esquerda_pct, direita_pct)
        escreve_texto(img, texto, (150, 70), (70, 14, 111))

        cv2.imshow('Pedra Papel e Tesoura', img)
        
        k = cv2.waitKey(10)
        if k == 27:
            break
    