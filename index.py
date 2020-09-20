from iqoptionapi.stable_api import IQ_Option
import time, json
from datetime import datetime
from dateutil import tz

API = IQ_Option('LOGIN', 'SENHA') #Insira seu e-mail e senha aqui
API.connect()
API.change_balance('PRACTICE') # PRACTICE / REAL

while True:
    if API.check_connect() == False:
        print('Erro ao se conectar. \n')
        API.connect()
    else:
        print('Conetado com sucesso. \n')
        break
    time.sleep(1)

def perfil():   #Carregando dados do perfil
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))

    return perfil

x = perfil()

def timestamp_converter(x): #Função que converte o formato TimeStamp
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H: %M: %S'),'%Y-%m-%d %H: %M: %S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))

    return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

#Exibição de alguns dados do perfil na IQ Option
#print('Saldo na conta: ',API.get_balance())
#print(x['name'])
#print(x['nickname'])
#print(x['currency'])
#print('Data de cadastro na IQ Option: ',timestamp_converter(x['created']))

par = API.get_all_open_time()   #Pega as moedas que estão abertas no momento

def payout(par, tipo, timeframe = 1):   #Função que puxa a moeda, tipo e payout de acordo com tempo (1m,5m,15m)
    if tipo == 'turbo': #Binária
        a = API.get_all_profit()
        return int(100 * a[par]['turbo'])

    elif tipo == 'digital': #Digital
        API.subscribe_strike_list(par, timeframe)
        while True:
            d = API.get_digital_current_profit(par, timeframe)
            if d != False:
                d = int(d)
                break
            time.sleep(1)
        API.unsubscribe_strike_list(par, timeframe)
        return d

for paridade in par ['turbo']:  #Mostra as binárias
    if par['turbo'][paridade]['open'] == True:
        print('[ BINARIA ]: '+paridade+ ' | Payout: ' +str(payout(paridade, 'turbo')))

print ('\n')

for paridade in par ['digital']:    #Mostra as digitais
    if par['digital'][paridade]['open'] == True:
        print('[ DIGITAL ]: ' +paridade+ ' | Payout: ' +str(payout(paridade, 'digital')))

#Pegando velas em tempo real
#parEur = 'EURUSD'   #Testando com apenas um tipo de moeda

#API.start_candles_stream(parEur, 60, 1)
#time.sleep(1)

#while True:
#    vela = API.get_realtime_candles(parEur, 60)
#    for velas in vela:
#        print (vela[velas]['close'], flush=True)
#    time.sleep(1)
#API.stop_candles_stream(parEur, 60)

#Puxar histórico de entradas feitas
status,historico = API.get_position_history_v2('DIGITAL', 10, 0, 0, 0) #Alternar para "turbo-option" caso queira exibir binária

#Algumas sugestões do que se pode pegar
'''
Final da operação: close_time
Início da operação: open_time
Lucro: close_profit
Entrada: invest

/ raw_event
Paridade: instrument_underlying / TURBO: active
Direção: instrument_dir / TURBO: direction
Valor: buy_amount
'''
print('\n')
#Exibir histórico de entradas e seu resultado
#for x in historico['positions']: #Para exibir os dados desejados
    #print('PAR: ' +str(x['raw_event']['instrument_underlying']) + ' / ' + 'DIRECAO: ' +str(x['raw_event']['instrument_dir']) + ' / VALOR: ' +str(x['invest']))
   # print('RESULTADO: ' +str(x['close_profit']- x['invest'] if x['close_profit'] == 0 else round(x['close_profit'] - x['invest'], 2)) + ' | INICIO OP: ' +str(timestamp_converter(x['open_time'] / 1000)) + ' / FIM OP: ' + str(timestamp_converter(x['close_time'] / 1000)))
    #print(' \n')

par = 'EURUSD-OTC'
entrada = 2
direcao = 'call'
timeframe = 1

status, id = API.buy(entrada, par, direcao, timeframe)

#if status:
 #   print(API.check_win_v3(id))
  #  print('\n')
#print(API.check_win_v4(id))
