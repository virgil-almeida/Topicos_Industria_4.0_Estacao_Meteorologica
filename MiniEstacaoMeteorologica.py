#!/usr/bin/python

import json
import sys
import time
import datetime

# libraries
import sys
import urllib.request #pip install urllib
import json
import gspread #pip install gspread
import random
from google.oauth2.service_account import Credentials
from datetime import datetime

#from sense_hat import SenseHat

# Nome da planilha no google.
GDOCS_SPREADSHEET_NAME = 'Estacao_Meteorologica'
# Intervalo de leitura.
FREQUENCY_SECONDS      = 30

def login_open_sheet(spreadsheet):
	"""Conecta no Google Docs spreadsheet e rotorna a planilha solecionada com nome escolhido."""
	try:
		scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
		credentials = Credentials.from_service_account_file('/Topicos_Industria_4.0_Estacao_Meteorologica/certificado.json',scopes=scope)
		gc = gspread.authorize(credentials)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except Exception as ex:
		print ('Falha no login e/ou busca de planilha. Verifique as credenciais, nome da planilha , e tenha certeza que a planilha esta compartilhada com o client_email do arquivo .json')
		print ('Erro retornado:', ex)
		sys.exit(1)


#sense = SenseHat()
#sense.clear()		
print ('Dados lidos salvos em {0} a cada {1} secondos.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print ('Ctrl-C para sair.')
worksheet = None
while True:
	# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_SPREADSHEET_NAME)

	# Attempt to get sensor reading.
	temp = random.random() #sense.get_temperature()
	temp = round(temp, 1)
	humidity = random.random() #sense.get_humidity()
	humidity = round(humidity, 1)
	pressure = random.random() #sense.get_pressure()
	pressure = round(pressure, 1)
	
	# 8x8 RGB
	#sense.clear()
	#info = 'Temperature (C): ' + str(temp) + 'Humidity: ' + str(humidity) + 'Pressure: ' + str(pressure)
	#sense.show_message(info, text_colour=[255, 0, 0])
	
	# Print
	print ("Temperatura (C): ", temp)
	print ("Humidade: ", humidity)
	print ("Pressão: ", pressure, "\n")

	# Incluir os dados coletados na planilha
	try:
		now = datetime.now()
		snow = now.strftime("%d/%m/%Y %H:%M:%S")
		worksheet.append_row((snow, temp,humidity,pressure))
	except Exception as ex:
		# Erro ao salvar, Maioria da vezes causado pela autenticação.
		print ('Erro ao salvar, tentarei novamente.Mensagem recebida:',ex)
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	# Wait 30 seconds before continuing
	print ('Linha adicionada em {0}'.format(GDOCS_SPREADSHEET_NAME))
	time.sleep(FREQUENCY_SECONDS)
