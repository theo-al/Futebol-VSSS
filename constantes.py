from numpy import ndarray, array

from dataclasses import dataclass

@dataclass(slots=True)
class faixa :
    MIN: ndarray
    MAX: ndarray

def nada (x): pass

#thresholds:
distancia = 300 # em milimetros

area_ret_time = 18000*(100**2)/(distancia**2) # formula(d) = (areapixelsmedida*distanciamedida^2)/(d)^2
area_roi_robo = area_ret_time*(7412/1200) #multiplica a "azul" pela proporção entre os retângulos pra achar o robo inteiro
area_ret_ID   = area_ret_time*(280/1200)  #multiplica a "azul" pela proporção entre os retângulos pra achar a "rosa"

area_bola = area_ret_time*(280/1200)*3/2 # TODO: mudar pro valor de verdade da bola

tamanho_aumentar = int((area_roi_robo**(1/2))/2)
tolerancia = 50/100

#    cores (alterar de acordo com a cor utilizada no robo fisico)
ajuste_cor = 20
#             times 
azul     = faixa(array([100, 80, 80]), array([110,255,255]))
amarelo  = faixa(array([ 26, 50, 50]), array([ 46,255,255]))
#             ids (ajustar (nesses só o verde ok))
verde    = faixa(array([ 80, 50, 50]), array([ 90,255,255])) 
roxo     = faixa(array([ 80, 50, 50]), array([ 90,255,255]))
ciano    = faixa(array([ 80, 50, 50]), array([ 90,255,255]))
rosa     = faixa(array([ 80, 50, 50]), array([ 90,255,255]))
vermelho = faixa(array([ 80, 50, 50]), array([ 90,255,255]))
#             (bola)
# cor_bola = faixa(array([ 0, 50, 50]), array([16,255,255]))
cor_bola = faixa(array([ 4, 50, 50]), array([ 7,255,255]))

