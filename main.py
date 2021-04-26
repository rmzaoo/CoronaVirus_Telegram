import requests
import time

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
    recuperados = responsecasos['features'][0]['attributes']['Activos_ARS']
    obitos = responsecasos['features'][0]['attributes']['ConfirmadosAcumulado_ARS']
    confirmados = responsecasos['features'][0]['attributes']['Activos_ARS']

    responsecasos = requests.get(Config.ApiTestes).json()
    testesfeitos = responsecasos['features'][0]['attributes']['value']


    responsecasos = requests.get(Config.ApiVacinas).json()
    vacinasdadas = responsecasos['features'][0]['attributes']['value']


    sendtochannel("Ativos: {0}| Recuperados: {1}| Óbitos: {2} | Confirmados: {3} | Total de Testes: {4} | Vacinas Adminstradas: {5} ".format(
        ativos, recuperados, obitos, confirmados, testesfeitos, vacinasdadas))
        
    print("Informação Enviada")

    print("updated")

    time.sleep(21600) #6 horas


