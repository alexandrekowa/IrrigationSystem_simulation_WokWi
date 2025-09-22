#Projeto prático: sistema de monitoramento de temperatura/umidade e irrigação automatizada de uma plantação

###Introdução
Este trabalho tem como objetivo informar o que foi criado no simulador WokWi, 
criando um projeto de monitoramento de temperatura e umidade, e com a baixa 
umidade, o sistema liga automaticamente o sistema de irrigação.

###Dispositivo controlador: Utilizando um dispositivo ESP32, ele realiza a 
automação do processo de leitura da umidade e temperatura e a ligação da 
irrigação. Ele faz a conexão com o BROKER, para enviar as mensagens que 
ocorrem para o tópico: “plantação/irrigacao”;

###Sensores: utiliza o sensor DHT22 para o monitoramento de temperatura e 
umidade;

###Sistema de irrigação: simulação utilizando um led vermelho. Caso a umidade
chegue abaixo de 30%, o sistema é ativado automaticamente, até que umidade 
suba acima de 30%.

###Painel informativo: utiliza um modelo LCD 16x2 (l2c), para fins informativos, 
indicando a temperatura e umidade juntamente com a ativação da irrigação no 
local;

###Sistema de comunicação e envio de dados: com o protocolo MQTT, envia os 
dados ao cliente MQTTX, com as informações de temperatura e umidade, 
juntamente com o aviso de irrigação ativa.

Realiza também a conexão com o cliente Blynk, onde envia os dados de 
temperatura, umidade e irrigação ativa para um dashboard na plataforma Blynk;
