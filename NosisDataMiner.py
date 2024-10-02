import re
from pypdf import PdfReader

class NosisDataMiner:
    __REGEX_DICT = {
        "Score": r"Score:([0-9]*)",
        "Total de endeudamiento sistema financiero":r"Total de endeudamiento sistema financiero: (.*)",
        "Total de compromisos mensuales sistema financiero":r"Total de compromisos mensuales sistema financiero: (.*)",
        "Cheques Rechazados BCRA - Cantidad sin fondos": r"\[HC\] Cheques Rechazados BCRA\nCantidad sin fondos, no pagados - Últ\. 6 Meses: (.*)",
        "Cheques Rechazados BCRA - Monto sin fondos": r"\[HC\] Cheques Rechazados BCRA\nCantidad sin fondos, no pagados - Últ\. 6 Meses: .*\nMonto sin fondos, no pagados - Últ. 6 Meses: (.*)",
        "Situación vigente de Central de Deudores BCRA": r"Situación vigente de Central de Deudores BCRA: (.*)",
        "Registra aportes patronales": r"Registra aportes patronales (.*)",
        "Concursos y quiebras cantidad - Últ. 24 meses":r"Concursos y quiebras cantidad - Últ. 24 meses: (.*)",
        "Deudores Fiscales - Tiene deudas fiscales": r"Deudores Fiscales\nTiene deudas fiscales:(.*)"
    }

    def __init__(self, file_path: str):
        self.__data = {key: None for key in self.__REGEX_DICT}

        try:
            self.file = PdfReader(file_path)

        except Exception as e:
            print("Error al crear data miner.")
            raise(e)

    def __get_data_from_text(self):
        for key, value in self.__REGEX_DICT.items():
            self.__data[key] = re.search(value, self.text).group(1)
            print(key, ":", self.__data[key])

    def __get_text_from_file(self):
        text = ""
        for page in self.file.pages:
            text += page.extract_text()
        self.text = text

    def get_data(self):
        self.__get_text_from_file()
        self.__get_data_from_text()
        return self.__data
