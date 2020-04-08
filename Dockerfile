FROM python:3
RUN mkdir /topicos
WORKDIR /topicos
COPY MiniEstacaoMeteorologica.py /topicos/
COPY certificados/SEU_CERTIFICADO_GOOGLE.json /topicos/
ENV CITY_ID_OPENWEATHERMAP 3470044
ENV API_KEY_OPENWEATHERMAP SUA_CHAVE
ENV GDOCS_SPREADSHEET_NAME Estacao01-Meteorologica
ENV GOOGLE_KEY_DIR "/topicos/SEU_CERTIFICADO_GOOGLE.json"
ENV PYTHONUNBUFFERED 1
RUN pip install requests
RUN pip install gspread
RUN pip install urllib3
