import time
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from sp_api.api import Reports
import apiclient

class AmazonReports():  
    def __init__(self):
        self.get_data = self.get_data()
        credentials_file = 'sheets_keys.json'
        self.spreadsheet_id = '1MEz4_UbiAPRBfdlwhSPddUF4LvQ7QfT4VJi2FtPLVFs'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file,['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive']
        )
        data = self.req('document')
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
        values = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range = "test1!A1",
            valueInputOption = "RAW",
            body = {"values": [line.split('\t') for line in data.split('\n')] }
            
        ).execute()
        
        
    def get_data(self): 

        client_config = dict(  
            refresh_token= "Your Token",
            lwa_client_secret ="Client secret",
            lwa_app_id = "App client",
            aws_secret_key = "",
            aws_access_key = "", 
            role_arn = "",
        )   
        rep = Reports(credentials=client_config).create_report(
            reportType="GET_FBA_FULFILLMENT_INVENTORY_SUMMARY_DATA",
            reportOptions = {
                "aggregateByLocation":"COUNTRY",
                "aggregatedByTimePeriod":"MONTHLY"                
                },
            
            marketplaceIds=["ATVPDKIKX0DER"],
        )
        res=Reports(credentials=client_config).get_report(reportId=rep('reportId'))
        
        while res('processingStatus') != "DONE":
            time.sleep(20)
            res = Reports(credentials=client_config).get_report(reportId=rep('reportId'))
        self.req = Reports(credentials=client_config).get_report_document(res("reportDocumentId"),download=True,decrypt=True)
    
    

if __name__ == '__main__':
    print("Start script.")
    am = AmazonReports()
    print("Done.")