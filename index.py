from iqoptionapi.stable_api import IQ_Option
import time

API = IQ_Option('login', 'senha')
API.set_max_reconnect(5)
API.change_balance('PRACTICE') # PRACTICE / REAL

while True:
    if API.check_connect() == False:
        print('Erro ao se conectar.')
        API.reconnect()
    else:
        print('Conetado com sucesso')
        break
    time.sleep(1)
