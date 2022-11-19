import cv2 
import numpy as np

from reconhecimento import * #ver de usar o nome completo nesse, deixei assim só pra não ter que mexer
from constantes import *

def centro (x: int, y: int, w: int, h: int) -> tuple[int,int]:
    return (x+w//2, y+h//2)

cap = cv2.VideoCapture(0) # Camera (alterar numero caso camera esteja em outro valor)

fonte = cv2.FONT_HERSHEY_SIMPLEX

largura_tela = int(cap.get(3))
altura_tela  = int(cap.get(4))

#vetor e dimensões do robô (mm)
altura_robo = 74 #altura do retangulo maior
altura_id   = 27 #altura do retângulo menor
distancia_centros = 22 #largura da fita

    #acha matriz de rotação #(teria como fazer menos conta aqui, mas como é só uma vez...)
seno_angulo_vetor = (altura_robo/2 - altura_id/2)/distancia_centros

while not (seno_angulo_vetor <= 1) : seno_angulo_vetor -=1 # deixa entre -1 e 1 #(mudar)
while not (seno_angulo_vetor >=-1) : seno_angulo_vetor +=1

angulo_vetor = pi/2 - asin(seno_angulo_vetor) #olhar isso do domínio
matriz_correção = np.array([
                           [cos(angulo_vetor), -sin(angulo_vetor)],
                           [sin(angulo_vetor),  cos(angulo_vetor)]
                           ])
# matriz_correção = np.array([[0,1], [-1,0]]) #90º

print(matriz_correção)


# cor dos times
time = 0 # 0 para time azul, 1 para time amarelo

if time == 0:
    cor_aliado = azul ; cor_oponente = amarelo

vet = np.array([0,40])
x_vet, y_vet = largura_tela//2, altura_tela//2
cont = 0

while True: # Loop de repetição para ret e frame do vídeo
    ret, frame = cap.read() # alterar "tela" para "frame" e utilizar a linha de baixo caso necessário diminuir a resolução da imagem
    tela = cv2.resize(frame,(0,0),fx=1,fy=1)
    # Extrair a região de interesse:
    '''roi = frame[x:x+?,y:y+?] # neste caso foi utilizada toda a imagem, mas pode ser alterado'''
    
    cont += 1
    #if not (cont % 20): 
    if True : 
        vet = np.dot(matriz_correção, vet)

    linha_desenhar = (y_vet, x_vet),(y_vet+int(vet[1]), x_vet+int(vet[0]))
    tela = cv2.arrowedLine(tela, *linha_desenhar, (240,100,0),5)

    #1 Detecção dos jogadores e bola
    hsv = cv2.cvtColor(tela, cv2.COLOR_BGR2HSV) # A cores em HSV funcionam baseadas em hue, no caso do opencv, varia de 0 a 180º (diferente do padrão de 360º)

    contornos_aliados = achar_contornos(hsv, cor_aliado)#, janela_debug="mascara_aliados")

    for cnt in contornos_aliados:

        area = cv2.contourArea(cnt)

        #Filtra retângulos com área muito distante da esperada
        if (area_ret_time*(1-tolerancia) <= area <= area_ret_time*(1+tolerancia)):

            cv2.drawContours(tela, [cnt], -1, (0, 255, 0),0) #ver magic numbers
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(tela, (x, y), (x + w, y + h), (255, 0, 0), 0)

            roi = hsv[max(y-tamanho_aumentar,0) : min(y+h+tamanho_aumentar,altura_tela), max(x-tamanho_aumentar,0) : min(x+w+tamanho_aumentar,largura_tela)] #clampa

            # detecção do num no time e direção do robô
            
            contornos_ID = achar_contornos(hsv, verde) # tem que fazer isso ser variável (por jogador, por conjunto de cores)
            # contornos_ID = achar_contornos(roi, (verde_min,verde_max)) # pra fazer assim precisa empurrar a posição pra perto do retâgulo de novo (ou talvez usar uma máscara)

            for cnt in contornos_ID:

                area = cv2.contourArea(cnt)

                #Filtra retângulos com área muito distante da esperada
                if (area_ret_ID*(1-tolerancia) <= area <= area_ret_ID*(1+tolerancia)):
                    cv2.drawContours(tela, [cnt], -1, (0, 255, 0),0)
                    xID, yID, wID, hID = cv2.boundingRect(cnt)

                    cv2.rectangle(tela, (xID, yID), (xID + wID, yID + hID), (0, 0, 0), 0)

                    linha_dir = np.array([*centro(xID, yID, wID, hID), *centro(x,y,w,h)])
                    tela = cv2.arrowedLine(tela, linha_dir[:2], linha_dir[2:], (255,0,0),5)

                    print(f"linha normal {linha_dir}")

                    vetor_normalizado = np.subtract(linha_dir[:2], linha_dir[2:])
                    print(f"vetor no zero: {vetor_normalizado}")

                    vetor_dir = np.dot(matriz_correção, vetor_normalizado)
                    print(f"vetor girado: {vetor_dir}")

                    centro_ret = centro(x, y, w, h) 
                    print(f"coordenadas ret: {centro_ret}")

                    inicial, final = (centro_ret, vetor_dir+centro_ret)
                    linha_desenhar = (int(inicial[0]), int(inicial[1])), (int(final[0]), int(final[1]))
                    print(f"linha na tela: {linha_desenhar}\n")

                    tela = cv2.arrowedLine(tela, *linha_desenhar, (240,100,0),5)

    cv2.imshow("tela", tela) #Exibe a filmagem("tela") do vídeo

    if cv2.waitKey(25) == ord('q'): break #tempo de exibição infinito (0) ou até se apertar a tecla q

cap.release()
cv2.destroyAllWindows()
