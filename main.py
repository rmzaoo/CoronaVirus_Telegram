import requests
import time
from datetime import datetime
import json

print("\n\n=========================")
print("https://github.com/rmzaoo")
print("=========================\n\n")


class Config:
    ApiCasos = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID_Concelhos_ARS_View2/FeatureServer/0/query?f=json&where=ARSNome%3D%27Nacional%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50&resultType=standard&cacheHint=true'
    ApiVacinas = 'https://services5.arcgis.com/eoFbezv6KiXqcnKq/arcgis/rest/services/Covid19_Total_Vacinados/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B"statisticType"%3A"sum"%2C"onStatisticField"%3A"Vacinados"%2C"outStatisticFieldName"%3A"value"%7D%5D&resultType=standard&cacheHint=true'
    ApiTestes = 'https://services5.arcgis.com/eoFbezv6KiXqcnKq/arcgis/rest/services/Covid19_Amostras/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B"statisticType"%3A"sum"%2C"onStatisticField"%3A"Total_Amostras_Novas"%2C"outStatisticFieldName"%3A"value"%7D%5D&resultType=standard&cacheHint=true'
    TelegramToken = '' # telegram bot token
    TelegramChannelID = '' # telegram channel id 

def sendtochannel(bot_message):
    
    send_text = 'https://api.telegram.org/bot' + Config.TelegramToken + '/sendMessage?chat_id=' + Config.TelegramChannelID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()



while True:
    responsecasos = requests.get(Config.ApiCasos).json()
    ativos = responsecasos['features'][0]['attributes']['Activos_ARS']
    recuperados = responsecasos['features'][0]['attributes']['Recuperados_ARS']
    obitos = responsecasos['features'][0]['attributes']['Obitos_ARS']
    confirmados = responsecasos['features'][0]['attributes']['ConfirmadosAcumulado_ARS']

    responsecasos = requests.get(Config.ApiTestes).json()
    testesfeitos = responsecasos['features'][0]['attributes']['value']


    responsecasos = requests.get(Config.ApiVacinas).json()
    vacinasdadas = responsecasos['features'][0]['attributes']['value']

    try:
        with open('data.bin') as json_file:
            data = json.load(json_file)

        Aativos = data["ativos"]
        Arecuperados = data["recuperados"]
        Aobitos = data["obitos"]
        Aconfirmados = data["confirmados"]
        Atestesfeitos = data["testesfeitos"]
        Avacinasdadas = data["vacinasdadas"]
    except:
        Aativos = ativos
        Arecuperados = recuperados
        Aobitos = obitos
        Aconfirmados = confirmados
        Atestesfeitos = testesfeitos
        Avacinasdadas = vacinasdadas        


    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    text = 'Covid-19 Portugal - Atualização '+current_time+'\n\n'

    a = (Aativos - ativos)
    if a >= 0:
        if a != 0:
            text = text + 'Subida de `'+str(a)+'` Caso/s Ativos | `'+str(ativos)+'` \n\n'
    else:
        text = text + 'Descida de `'+str(a)+'` Caso/s Ativos | `'+str(ativos)+'` \n\n'

    a = (Arecuperados - recuperados)
    if a >= 0:
        if a != 0:
            text = text + 'Subida de `'+str(a)+'` Recuperado/s | `'+str(recuperados)+'` \n\n'
    else:
        text = text + 'Descida de `'+str(a)+'` Recuperado/s | `'+str(recuperados)+'` \n\n'
    
    a = (Aobitos - obitos)
    if a >= 0:
        if a != 0:
            text = text + 'Subida de `'+str(a)+'` Obito/s | `'+str(obitos)+'` \n\n'
    else:
        text = text + 'Descida de `'+str(a)+'` Obito/s | `'+str(obitos)+'` \n\n'


    a = (Aconfirmados - confirmados)
    if a >= 0:
        if a != 0:
            text = text + 'Subida de `'+str(a)+'` Confirmado/s | `'+str(confirmados)+'` \n\n'
    else:
        text = text + 'Descida de `'+str(a)+'` Confirmado/s | `'+str(confirmados)+'` \n\n'


    a = (Atestesfeitos - testesfeitos)
    if a >= 0:
        if a != 0:
            text = text + 'Subida de `'+str(a)+'` Teste/s Feito/s | `'+str(testesfeitos)+'` \n\n'
    else:
        text = text + 'Descida de `'+str(a)+'` Teste/s Feito/s | `'+str(testesfeitos)+'` \n\n'

    a = (Avacinasdadas - vacinasdadas)
    if a >= 0:
        if a != 0:
            text = text + 'Subida de `'+str(a)+'` Vacinado/s | `'+str(vacinasdadas)+'` \n\n'
    else:
        text = text + 'Descida de `'+str(a)+'` Vacinado/s | `'+str(vacinasdadas)+'` \n\n'


    if Aativos != ativos:
        response = sendtochannel(text)
        print("API: Foi encontrado novos dados")

        if response['ok'] == False :
            print('Telegram Bot: Ocorreu um erro a enviar a mensagem.\n\n'+str(response)+'\n')
        else:
            print("Telegram Bot: Foi envido uma atualização dos novos dados")
    else:
        print("API: Não existe ainda nenhuma atualização dos dados")

    data_set = {}
    data_set['ativos'] = ativos
    data_set['recuperados'] = recuperados
    data_set['obitos'] = obitos
    data_set['confirmados'] = confirmados
    data_set['testesfeitos'] = testesfeitos
    data_set['vacinasdadas'] = vacinasdadas

    with open('data.bin', 'w') as outfile:
        json.dump(data_set, outfile)

    print("APP: Dados Guardados com Sucesso")

    time.sleep(10800) #3 horas


