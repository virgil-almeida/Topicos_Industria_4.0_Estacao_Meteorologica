FROM python
ENV API_KEY_OPENWEATHERMAP f0c8b4975f94531f579ae6614d6420f4
ENV CITY_ID_OPENWEATHERMAP 3470044
ENV GDOCS_SPREADSHEET_NAME Estacao01-Meteorologica
ENV GOOGLE_KEY_DIR "/Topicos_Industria_4.0_Estacao_Meteorologica/certificados/estacao-meteorologica-273314-973d6bcbd34f.json"
RUN git clone https://github.com/virgil-almeida/Topicos_Industria_4.0_Estacao_Meteorologica.git
RUN pip install requests
RUN pip install gspread
RUN pip install urllib3
