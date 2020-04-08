#!/usr/bin/python

import os
import json
import sys
import time
import requests

#apenas para teste
import random

# libraries
import urllib.request #pip install urllib
import gspread #pip install gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

#from sense_hat import SenseHat

#ativa impressão local
DEBUG = 1
# DADOS DO openweathermap
CITY_ID = os.environ['CITY_ID_OPENWEATHERMAP']
API_KEY = os.environ['API_KEY_OPENWEATHERMAP'] #TODO: Trocar para a sua api key do openweathermap

# Nome da planilha no google.
GDOCS_SPREADSHEET_NAME = os.environ['GDOCS_SPREADSHEET_NAME']
GOOGLE_KEY = os.environ['GOOGLE_KEY_DIR'] #TODO: Diretorio onde está o json do sua Contas de serviço Google
# Intervalo de leitura.
FREQUENCY_SECONDS = 30


def login_open_sheet(spreadsheet):
	"""Conecta no Google Docs spreadsheet e rotorna a planilha solecionada com nome escolhido."""
	try:
		scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
		credentials = Credentials.from_service_account_file(GOOGLE_KEY,scopes=scope)
		gc = gspread.authorize(credentials)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except Exception as ex:
		print ('Falha no login e/ou busca de planilha. Verifique as credenciais, nome da planilha , e tenha certeza que a planilha esta compartilhada com o client_email do arquivo .json')
		print ('Erro retornado:', ex)
		sys.exit(1)


def read_openweathermap(city_ID,api_KEY):
	"""Conecta no openweathermap.org e retorna os dados meteorologicos."""
	base_url = "http://api.openweathermap.org/data/2.5/weather?"	 
	complete_url = base_url + "id="+city_ID+"&appid="+api_KEY  
	response = requests.get(complete_url)   
	x = response.json()   
	# "404", means city is found otherwise, 
	# city is not found 
	if x["cod"] != "404": 
		y = x["main"] 
		current_temperature = y["temp"]- 273.15 # kelvin to celcius 
		current_pressure = y["pressure"] 
		current_humidiy = y["humidity"] 
		z = x["weather"] 
		weather_description = z[0]["description"] 
		return((str(current_temperature),str(current_pressure),str(current_humidiy),str(weather_description)))
	else: 
		sys.exit(1) 

#REALIZA A LEITURA LOCAL
#sense = SenseHat()
#sense.clear()
if DEBUG:		
	print ('Dados lidos salvos em {0} a cada {1} secondos.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
	print ('Ctrl-C para sair.')

worksheet = None
while True:
	# Realiza o login caso necessário.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_SPREADSHEET_NAME)

	#Ler valores do openweather
	openweathermap = read_openweathermap(CITY_ID,API_KEY)

	# Realiza a leitura dos dados locais.
	temp = random.random()+float(openweathermap[0]) #sense.get_temperature()
	temp = round(temp, 1)
	humidity = random.random()+float(openweathermap[2]) #sense.get_humidity()
	humidity = round(humidity, 1)
	pressure = random.random()+float(openweathermap[1]) #sense.get_pressure()
	pressure = round(pressure, 1)
	
	# 8x8 RGB
	#sense.clear()
	#info = 'Temperature (C): ' + str(temp) + 'Humidity: ' + str(humidity) + 'Pressure: ' + str(pressure)
	#sense.show_message(info, text_colour=[255, 0, 0])
	
	if DEBUG:
		print("\nDados Locais")
		print ("Temperatura (C): ", temp)
		print ("Humidade: ", humidity)
		print ("Pressão: ", pressure, "\n")
		print("Dados Remotos")
		print(" Temperatura (C) = " +
							str(openweathermap[0]) + 
				"\n Pressão atmosferica (hPa) = " +
							str(openweathermap[1]) +
				"\n Humidade (porcentagem) = " +
							str(openweathermap[2]) +
				"\n Descrição = " +
							str(openweathermap[3])) 

	# Incluir os dados coletados na planilha
	try:
		now = datetime.now()
		snow = now.strftime("%d/%m/%Y %H:%M:%S")
		worksheet.append_row((snow, temp,humidity,pressure,str(openweathermap[0]),str(openweathermap[1]),str(openweathermap[2]),str(openweathermap[3])))
	except Exception as ex:
		# Erro ao salvar, Maioria da vezes causado pela autenticação.
		if DEBUG:
			print ('Erro ao salvar, tentarei novamente.Mensagem recebida:',ex)
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	if DEBUG:
		print ('Linha adicionada em {0}'.format(GDOCS_SPREADSHEET_NAME))

	time.sleep(FREQUENCY_SECONDS)
