import time
import dht
import json
import network
from machine import Pin, I2C
from umqttsimple import MQTTClient
from blynk import Blynk
from lcd_api import LcdApi
from i2c_lcd import I2cLcd


led_bomba = Pin(4, Pin.OUT)  # PIN 4 para o LED (saída)
sensor = dht.DHT22(Pin(2))   # PIN 2 para o DHT22

limiar_umidade_ar = 30 # Limiar de umidade (caso a umidade fique abaixo de 30%, a irrigação é ativa)

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

# Configura o I2C para o LCD nos pinos padrão do ESP32 (GPIO21 e GPIO22)
i2c = I2C(1, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

lcd.clear()
lcd.putstr("Iniciando...")
time.sleep(1)

# Conexão com o dispositivo ao Blynk
client = Blynk(
    "XfthrEveNp6MYlBVlhnwWxn6Wz_PQoUk",
    wifi_ssid = "Wokwi-GUEST",
    wifi_password = "",
    verbose = True
)

time.sleep(2)

lcd.clear()
lcd.putstr("Wi-Fi conectado")
time.sleep(2)

lcd.clear()
lcd.putstr("Sistema Pronto!")
time.sleep(2)

# Rede WI-FI do BROKER
SSID, PASS = "Wokwi-GUEST", ""
BROKER = "broker.emqx.io"
TOPIC = b"plantacao/irrigacao"

# TENTATIVA PARA CONECTAR NA REDE WI-FI DO BROKER
w = network.WLAN(network.STA_IF); w.active(True)
w.connect(SSID, PASS)
while not w.isconnected():
    client.publish("ds/WiFi", "1")
    time.sleep(0.1)

cid = b"esp32-" + str(int(time.time()*1000)).encode()
c = MQTTClient(cid, BROKER)
c.connect()


##############################__________________################################

# INICIO

while True:
    try:
        sensor.measure() # Leitura do sensor DHT22
       
        # Obtém a umidade e a temperatura
        t, u = sensor.temperature(), sensor.humidity()
        
        # Imprime os valores no console para monitoramento
        print(f"Temperatura: {t:.1f}°C")       
        print(f"Umidade do ar: {u:.1f}%")

        client.publish("ds/Temperatura", str(t))
        client.publish("ds/Umidade", str(u))

        lcd.clear()
        lcd.putstr("Temp: " + str(t) + "C")
        lcd.move_to(0, 1)
        lcd.putstr("Umid: " + str(u) + "%")

        payload = {"Umidade": round(u, 1), "Temperatura": round(t, 1)}
        c.publish(TOPIC, json.dumps(payload))

        # Verifica se a umidade do ar está abaixo do limiar
        if u < limiar_umidade_ar:

            # Envio ao Broker
            payload1 = "Umidade do ar baixa! Ligando a bomba..."
            c.publish(TOPIC, json.dumps(payload1))

            print("Umidade do ar baixa! Ligando a bomba...")

            # Envio tela LCD
            lcd.clear()
            lcd.putstr("Umidade está")
            lcd.move_to(0, 1)
            lcd.putstr("baixa!")
            time.sleep(1) 

            # Envio tela LCD
            lcd.clear()
            lcd.putstr("Ligando bomba")
            time.sleep(2) 

            led_bomba.value(1)                # Liga o LED
            client.publish("ds/ativada", "1") # Envio ao Blynk
            time.sleep(8)                    # Aguarda a irrigação ser feita
            led_bomba.value(0)                # Desliga o LED (LOW)
            client.publish("ds/ativada", "0") # Envio ao Blynk

            lcd.clear()
            lcd.putstr("Irrigacao")
            lcd.move_to(0, 1)
            lcd.putstr("finalizada")
            time.sleep(2)

            lcd.clear()
            lcd.putstr("Bomba desligada")
            time.sleep(2)

            payload2 = "Bomba desligada"
            c.publish(TOPIC, json.dumps(payload2))
            print("Bomba desligada.")

            #print("PUB -> ", payload)
        else:
            print("Umidade do ar adequada. Nenhuma ação necessária.")
            
    except OSError as e:
        print("Erro ao ler o sensor DHT22:", e)
    
    time.sleep(2)