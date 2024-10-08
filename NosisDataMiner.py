import re
from pypdf import PdfReader

class NosisDataMiner:
    __REGEX_DICT = {
        "Score": {
          "Salesforce API Name":"Score__c",
          "regex":r"Score: ([0-9]*)"
        },
        "Total de endeudamiento sistema financiero":{
          "Salesforce API Name":"Total_de_endeudamiento_sistema_financier__c",
          "regex":r"Total de endeudamiento sistema financiero: (.*)"
        },
        "Total de compromisos mensuales sistema financiero":{
          "Salesforce API Name":"Total_compromisos_mensuales_sistema_fina__c",
          "regex":r"Total de compromisos mensuales sistema financiero: (.*)"
        },
        "Cheques Rechazados BCRA - Cantidad sin fondos": {
          "Salesforce API Name":"Cheques_Rechazados_BCRA_Cant_sin_fondos__c",
          "regex":r"\[HC\] Cheques Rechazados BCRA\nCantidad sin fondos, no pagados - Últ\. 6 Meses: (.*)"
        },
        "Cheques Rechazados BCRA - Monto sin fondos": {
          "Salesforce API Name":"Cheques_Rechazados_BCRA_Monto_sin_fondos__c",
          "regex":r"\[HC\] Cheques Rechazados BCRA\nCantidad sin fondos, no pagados - Últ\. 6 Meses: .*\nMonto sin fondos, no pagados - Últ. 6 Meses: (.*)"
        },
        "Situación vigente de Central de Deudores BCRA": {
          "Salesforce API Name":"Situacion_vigente_Central_Deudores_BCRA__c",
          "regex":r"Situación vigente de Central de Deudores BCRA: (.*)"
        },
        "Registra aportes patronales": {
          "Salesforce API Name":"Registra_aportes_patronales__c",
          "regex":r"Registra(.*)aportes patronales (.*)"
        },
        "Concursos y quiebras cantidad - Últ. 24 meses":{
          "Salesforce API Name":"Concursos_y_quiebras_cantidad__c",
          "regex":r"Concursos y quiebras cantidad - Últ. 24 meses: (.*)"
        },
        "Deudores Fiscales - Tiene deudas fiscales": {
          "Salesforce API Name":"Deudores_Fiscales_Tiene_deudas_fiscale__c",
          "regex":r"Deudores Fiscales\nTiene deudas fiscales:(.*)"
        }
    }

    def __init__(self, file_path: str):
        __aux_keys = [value["Salesforce API Name"] for key, value in self.__REGEX_DICT.items()]
        self.__data = {key: None for key in __aux_keys}

        try:
            self.file = PdfReader(file_path)

        except Exception as e:
            print("Error al crear data miner.")
            raise(e)

    def __get_data_from_text(self):
        for key, value in self.__REGEX_DICT.items():
          try:
            if key == "Registra aportes patronales":
              self.__data[key] = re.search(value, self.text).group(0)
            else:
              self.__data[key] = re.search(value, self.text).group(1)
          except Exception as e:
            print(f"\tError al obtener {key}")
            raise e

    def __get_text_from_file(self):
        text = ""
        for page in self.file.pages:
            text += page.extract_text()
        self.text = text

    def get_data(self):
        self.__get_text_from_file()
        self.__get_data_from_text()
        return self.__data