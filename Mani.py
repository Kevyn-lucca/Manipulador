
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1_IgnXSEQqR_vsUmitN2DQZPYi9q5DWSdJ42ETxo_IDY'
SAMPLE_RANGE_NAME = 'Página1!A1:D6'


def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Cred.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Ler informacoes do Google Sheets
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        valores = result['values']
        print(valores)
        
        valores_adicionar = [
            ["Media dano"],
        ]
        
        for i, linha in enumerate(valores):
            if i > 0:
                danoMax = linha[1]
                danoSeg = linha[2]
                danoSeg = float(danoSeg.replace(",", "."))
                danoMax = float(danoMax.replace(",", "."))
                danoMed = danoMax + danoSeg/2
                danoMed = f'{danoMed}'.replace(".", ",")
                valores_adicionar.append([danoMed])
        
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="D1", valueInputOption="USER_ENTERED",
                              body={'values': valores_adicionar}).execute()
        # adicionar/editar uma informação
        
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()






