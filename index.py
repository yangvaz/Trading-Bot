from iqoptionapi.stable_api import IQ_Option
import time, json
from datetime import datetime
from dateutil import tz

API = IQ_Option('login', 'senha')
API.connect()
API.change_balance('PRACTICE') # PRACTICE / REAL

while True:
    if API.check_connect() == False:
        print('Erro ao se conectar.')
        API.connect()
    else:
        print('Conetado com sucesso')
        break
    time.sleep(1)

def perfil():
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))

    return perfil

def timestamp_converter(x):
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H: %M: %S'),'%Y-%m-%d %H: %M: %S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))

    return str(hora)[:-6]

print('Saldo na conta: ',API.get_balance())

x = perfil()

print(x['name'])
print(x['nickname'])
print(x['currency'])
print(timestamp_converter(x['created']))

#print(perfil())
