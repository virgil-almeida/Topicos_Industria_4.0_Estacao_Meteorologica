# Topicos_Industria_4.0_Estacao_Meteorologica
Estação Meteorológica com Raspberry e Google Planilhas

Criação de um estação Meteorológica usando um RasberryPI e sensores de temperatura DS18B20 e/ou DHT11 e/ou SenorHat

# Execução fora do Docker
Modifique o arquivo MiniEstacaoMeteorologica.py alterando as linhas abaixo para os valores corretos
CITY_ID = os.environ['CITY_ID_OPENWEATHERMAP']
API_KEY = os.environ['API_KEY_OPENWEATHERMAP'] 
GDOCS_SPREADSHEET_NAME = os.environ['GDOCS_SPREADSHEET_NAME']
GOOGLE_KEY = os.environ['GOOGLE_KEY_DIR']

# Execução dentro do Docker
Modifique o arquivo Dockerfile informando os dados de acesso e a planilha de retorno
COPY certificados/SEU_CERTIFICADO_GOOGLE.json /topicos/
ENV CITY_ID_OPENWEATHERMAP 3470044
ENV API_KEY_OPENWEATHERMAP SUA_CHAVE
ENV GDOCS_SPREADSHEET_NAME Estacao01-Meteorologica
ENV GOOGLE_KEY_DIR "/topicos/SEU_CERTIFICADO_GOOGLE.json"

->Execute o comando
$ docker-compose -f "docker-compose.yml" up -d --build

Acompanhe os resultados da execução pelo 
$ docker logs -f NOMEDOVOLUME

# Fontes utilizadas #
https://www.hackster.io/idreams/make-a-mini-weather-station-with-a-raspberry-pi-447866

https://gspread.readthedocs.io/en/latest/oauth2.html

https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/

https://github.com/MichaIng/DietPi/issues/3067

https://www.filipeflop.com/blog/temperatura-umidade-dht11-com-raspberry-pi/

https://github.com/allthingsclowd/docker_rpi3_python_iot_api_dht_11_22
