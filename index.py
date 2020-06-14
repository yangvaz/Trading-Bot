from iqoptionapi.stable_api import IQ_Option
import time, json
from datetime import datetime
from dateutil import tz

API = IQ_Option('email', 'senha') #Insira seu e-mail e senha aqui
API.connect()
API.change_balance('PRACTICE') # PRACTICE / REAL

while True:
    if API.check_connect() == False:
        print('Erro ao se conectar.')
        API.connect()
    else:
        print('Conetado com sucesso.')
        break
    time.sleep(1)

def perfil():
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))

    return perfil

x = perfil()

def timestamp_converter(x):
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H: %M: %S'),'%Y-%m-%d %H: %M: %S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))

    return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

print('Saldo na conta: ',API.get_balance())

print(x['name'])
print(x['nickname'])
print(x['currency'])
print('Data de cadastro na IQ Option: ',timestamp_converter(x['created']))

par = API.get_all_open_time()

def payout(par, tipo, timeframe = 1):
    if tipo == 'turbo':
        a = API.get_all_profit()
        return int(100 * a[par]['turbo'])

    elif tipo == 'digital':
        API.subscribe_strike_list(par, timeframe)
        while True:
            d = API.get_digital_current_profit(par, timeframe)
            if d != False:
                d = int(d)
                break
            time.sleep(1)
        API.unsubscribe_strike_list(par, timeframe)
        return d

for paridade in par ['turbo']:
    if par['turbo'][paridade]['open'] == True:
        print('[ BINARIA ]: '+paridade+ ' | Payout: ' +str(payout(paridade, 'turbo')))

print ('\n')

for paridade in par ['digital']:
    if par['digital'][paridade]['open'] == True:
        print('[ DIGITAL ]: ' +paridade+ ' | Payout: ' +str(payout(paridade, 'digital')))

#Pegando velas em tempo real
parEur = 'EURUSD-OTC'

API.start_candles_stream(parEur, 60, 1)
time.sleep(1)

while True:
    vela = API.get_realtime_candles(parEur, 60)
    for velas in vela:
        print (vela[velas]['close'], flush=True)
    time.sleep(1)
API.stop_candles_stream(parEur, 60)
