import flet as ft

from app.classe import PageAppFlet
from configs.configuration_manager import PATH_CONFIG, Configuration

if __name__ == "__main__":
    initial_configuration = {
        "niveis-mantidos": 2,
        "formatos-imagem": ".jpg, .jpeg, .png",
        "formatos-documento": ".doc, .docx, .pdf",
        "formatos-planilha": ".xlsx, .xls, .csv",
        "formatos-audio": "mp3, mva",
        "formatos-video": "mp4, mkv, avi ",
        "opcoes-copia": "manter",
    }
    config = Configuration(PATH_CONFIG)
    config.load_configurations()
    if not config.configurations:
        config.create_initial_configuration(initial_configuration)
    ft.app(PageAppFlet)
