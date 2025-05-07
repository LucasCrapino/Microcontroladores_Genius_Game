from machine import Pin
import utime
import random

led_red = Pin(15, Pin.OUT)
btn_red = Pin(0, Pin.IN, Pin.PULL_UP)

led_blue = Pin(16, Pin.OUT)
btn_blue = Pin(1, Pin.IN, Pin.PULL_UP)

led_green = Pin(17, Pin.OUT)
btn_green = Pin(3, Pin.IN, Pin.PULL_UP)

led_yellow = Pin(18, Pin.OUT)
btn_yellow = Pin(2, Pin.IN, Pin.PULL_UP)

led_acerto = Pin(4, Pin.OUT)

led_sequencia = Pin(19, Pin.OUT)

def piscar_aleatorio(piscadas):
    lista = []
    
    for num in range(piscadas):
        num_aleatorio = random.randint(1, 4)
        
        if num_aleatorio == 1:
            print("Azul")
            led_blue.value(1)
            utime.sleep(0.5)
            led_blue.value(0)
            utime.sleep(0.5)
            lista.append("azul")
        elif num_aleatorio == 2:
            print("Vermelho")
            led_red.value(1)
            utime.sleep(0.5)
            led_red.value(0)
            utime.sleep(0.5)
            lista.append("vermelho")
        elif num_aleatorio == 3:
            print("Amarelo")
            led_yellow.value(1)
            utime.sleep(0.5)
            led_yellow.value(0)
            utime.sleep(0.5)
            lista.append("amarelo")
        elif num_aleatorio == 4:
            print("Verde")
            led_green.value(1)
            utime.sleep(0.5)
            led_green.value(0)
            utime.sleep(0.5)
            lista.append("verde")
    
    return lista


def obter_valor_botao(lista):
    piscadas = len(lista)
    botoes = []
    pressionadas = 0
    
    while pressionadas < piscadas:
        led_sequencia.value(1)
        if btn_red.value() == 0:
            botoes.append("vermelho")
            led_red.value(1)
            utime.sleep(0.5)
            led_red.value(0)
            print(f"{pressionadas + 1} - vermelho")
            pressionadas += 1
            while btn_red.value() == 0:
                utime.sleep(0.05)
                
        elif btn_blue.value() == 0:
            botoes.append("azul")
            led_blue.value(1)
            utime.sleep(0.5)
            led_blue.value(0)
            print(f" {pressionadas + 1} - azul")
            pressionadas += 1
            while btn_blue.value() == 0:
                utime.sleep(0.05)
                
        elif btn_green.value() == 0:
            botoes.append("verde")
            led_green.value(1)
            utime.sleep(0.5)
            led_green.value(0)
            print(f"{pressionadas + 1} - verde")
            pressionadas += 1
            while btn_green.value() == 0:
                utime.sleep(0.05)
                
        elif btn_yellow.value() == 0:
            botoes.append("amarelo")
            led_yellow.value(1)
            utime.sleep(0.5)
            led_yellow.value(0)
            print(f"{pressionadas + 1} - amarelo")
            pressionadas += 1
            while btn_yellow.value() == 0:
                utime.sleep(0.05)
    led_sequencia.value(0)
    return botoes

def comparar_sequencia(lista_piscadas, botoes_pressionados):
    if lista_piscadas == botoes_pressionados:
        return True  
    led_yellow.value(1)
    led_green.value(1)
    led_red.value(1)
    led_blue.value(1)
    
    utime.sleep(0.5)
    
    led_yellow.value(0)
    led_green.value(0)
    led_red.value(0)
    led_blue.value(0)
    return False  


def jogar(rodada):
    rodada_atual = rodada 
    perdeu = False

    while not perdeu:
        
        print(f"Iniciando rodada {rodada_atual}")
        
        utime.sleep(0.5)
        led_acerto.value(1)
        utime.sleep(0.5)
        led_acerto.value(0)
        utime.sleep(0.5)
        led_acerto.value(1)
        utime.sleep(0.5)
        led_acerto.value(0)
        utime.sleep(1)
        
        lista_piscadas = piscar_aleatorio(rodada_atual)
        
        print(f"Agora, aperte na sequencia dos leds!")
        
        # utime.sleep(0.5)
        # led_sequencia.value(1)
        # utime.sleep(0.5)
        # led_sequencia.value(0)
        
        botoes_pressionados = obter_valor_botao(lista_piscadas)
        
        resultado = comparar_sequencia(lista_piscadas, botoes_pressionados)
        
        if resultado:  
            rodada_atual += 1
            print(f"Passou para a rodada {rodada_atual}")
        else:  
            perdeu = True  
            print(f"Você perdeu na rodada {rodada_atual}!")

    return

jogar(1)
