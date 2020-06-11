from iqoptionapi.stable_api
import IQ_Option
import time

API = IQ_Option('login', 'senha')

while True:
    if API.check_connect() == False:
        print('Erro ao se conectar.')
        API.reconnect()
    else:
        print('Conetado com sucesso')
        break
