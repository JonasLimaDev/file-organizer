import flet as ft

# from flet import NavigationDrawer
from configs.configuration_manager import Configuration
from file_modules.manager_files_and_paths import (
    copy_file_to_destination,
    index_files,
)

initial_configuration = {
    "niveis-mantidos": 2,
    "formatos-imagem": ".jpg, .jpeg, .png",
    "formatos-documento": ".doc, .docx, .pdf",
    "formatos-planilha": ".xlsx, .xls, .csv",
    "formatos-audio": "mp3, mva",
    "formatos-video": "mp4, mkv, avi ",
    "opcoes-copia": "manter",
}
PATH_CONFIG = "./settings.config"
config = Configuration(PATH_CONFIG)
config.load_configurations()
if not config.configurations:
    config.create_initial_configuration(initial_configuration)
    config.load_configurations()


class PersonInput(ft.TextField):
    def __init__(self, label, value=None, input_filter=None):
        super().__init__()
        self.label = label
        self.value = value
        self.input_filter = input_filter
        self.text_size = 14
        self.label_style = ft.TextStyle(size=18)


class TextInfo(ft.Text):
    def __init__(self, value, size=16, text_align=ft.TextAlign.CENTER):
        super().__init__()
        self.value = value
        self.size = size
        self.text_align = text_align


class PersonTooltip(ft.Tooltip):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.bgcolor = ft.Colors.GREY_700
        self.text_style = ft.TextStyle(
            color=ft.Colors.WHITE, size=13, italic=True
        )


class SideDraer(ft.NavigationDrawer):
    def __init__(self, on_dismiss):
        super().__init__(on_dismiss=on_dismiss)

        self.niveis_mantidos = PersonInput(
            label="Número niveis mantidos",
            value=config.configurations["niveis-mantidos"],
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.formatos_imagem = PersonInput(
            label="Formatos de Imagens",
            value=config.configurations["formatos-imagem"],
        )
        # config = Configuration("./settings.config")
        # config.save_configuration_file()
        self.formatos_documento = PersonInput(
            label="Formatos de Documentos",
            value=config.configurations["formatos-documento"],
        )
        self.formatos_planilha = PersonInput(
            label="Formatos de Planilhas",
            value=config.configurations["formatos-planilha"],
        )
        self.formatos_audio = PersonInput(
            label="Formatos de Aúdios",
            value=config.configurations["formatos-audio"],
        )
        self.formatos_video = PersonInput(
            label="Formatos de Vídeos",
            value=config.configurations["formatos-video"],
        )
        self.opcoes_copia = ft.RadioGroup(
            value=config.configurations["opcoes-copia"],
            content=ft.Column(
                [
                    ft.Radio(
                        value="manter",
                        label="Manter Numerada",
                        tooltip=PersonTooltip(
                            message="Mantem cópias adicionado o número de cada\
                                \ncópia no nome do arquivo.",
                        ),
                    ),
                    ft.Radio(
                        value="recente",
                        label="Manter Recentes",
                        tooltip=PersonTooltip(
                            message="Substitui cópias, mantendo os arquivos\
                                \ncom data de modificação mais recente",
                        ),
                    ),
                    ft.Radio(
                        value="original",
                        label="Manter Originais",
                        tooltip=PersonTooltip(
                            message="Substitui cópias, mantendo os arquivos\
                                \ncom data de criação mais antiga",
                        ),
                    ),
                ]
            ),
        )

        self.controls = [
            ft.Container(height=30),
            TextInfo("Configurações"),
            ft.Divider(thickness=1),
            TextInfo("Opções de Cópia", size=14),
            self.opcoes_copia,
            ft.Divider(thickness=2),
            TextInfo("Nivel de Hierarquia de Pasta", size=14),
            self.adicionar_container_input(self.niveis_mantidos),
            ft.Divider(thickness=2),
            TextInfo("Formatos de Arquivos", size=14),
            self.adicionar_container_input(self.formatos_imagem),
            self.adicionar_container_input(self.formatos_documento),
            self.adicionar_container_input(self.formatos_planilha),
            self.adicionar_container_input(self.formatos_audio),
            self.adicionar_container_input(self.formatos_video),
            self.adicionar_container_input(
                ft.ElevatedButton("salvar", on_click=self.salvar_opcoes)
            ),
        ]

    @staticmethod
    def adicionar_container_input(conteudo):
        return ft.Container(
            margin=ft.margin.symmetric(horizontal=20, vertical=5),
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            content=conteudo,
        )

    def salvar_opcoes(self, e):
        for atributo in self.__dict__:
            if atributo[0] != "_" and atributo not in set(
                [
                    "badge",
                    "tooltip",
                    "parent",
                ]
            ):
                config.add_configuration(
                    atributo.replace("_", "-"), getattr(self, atributo).value
                )
                # print(getattr(self,atributo).value)
        config.save_configuration_file()
        self.update()


class PageAppFlet:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Organizador de Arquivos"
        self.page.window.width = 620
        self.page.window.height = 680
        self.page.theme_mode = ft.ThemeMode.DARK

        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.dialogo_escolher_pasta = ft.FilePicker(
            on_result=self.pegar_resultado_selecao
        )
        self.page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.MENU,
                on_click=self.mostra_opcoes,
            ),
            leading_width=40,
            title=ft.Text("Organizador de Arquivos"),
            center_title=True,
            bgcolor=ft.Colors.BLACK26,
        )

        self.drawer = SideDraer(on_dismiss=self.update_configs_page)

        # self.cabecalho = TextInfo("Organizador de Arquivos", size=20)
        self.lista_filtros = []
        self.informacao_programa = TextInfo(
            "Busca arquivos na pasta de origem e \
            suas subpastas, salvando uma cópia agrupada \
            por tipo de arquivo na pasta de destino".replace(
                "            ", ""
            ),
        )
        self.tooltip_imagem = PersonTooltip(
            f"formatos: {
                config.configurations['formatos-imagem']
                }"
        )
        self.tooltip_documento = PersonTooltip(
            f"formatos: {
                config.configurations['formatos-documento']
                }"
        )
        self.tooltip_planilha = PersonTooltip(
            f"formatos: {
                config.configurations['formatos-planilha']
                }"
        )
        self.tooltip_video = PersonTooltip(
            f"formatos: {
                config.configurations['formatos-video']
                }"
        )
        self.tooltip_audio = PersonTooltip(
            f"formatos: {
                config.configurations['formatos-audio']
                }"
        )
        self.grupo_tipos_arquivos = ft.Column(
            [
                ft.Container(
                    TextInfo("Aceita os Seguintes Grupos de Arquivos:"),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Checkbox(
                                label="Imagem",
                                value=False,
                                on_change=self.alterar_lista_filtros,
                                tooltip=self.tooltip_imagem,
                            ),
                            ft.Checkbox(
                                label="Documento",
                                value=False,
                                on_change=self.alterar_lista_filtros,
                                tooltip=self.tooltip_documento,
                            ),
                            ft.Checkbox(
                                label="Planilha",
                                value=False,
                                on_change=self.alterar_lista_filtros,
                                tooltip=self.tooltip_planilha,
                            ),
                            ft.Checkbox(
                                label="Vídeo",
                                value=False,
                                on_change=self.alterar_lista_filtros,
                                tooltip=self.tooltip_video,
                            ),
                            ft.Checkbox(
                                label="Áudio",
                                value=False,
                                on_change=self.alterar_lista_filtros,
                                tooltip=self.tooltip_audio,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
            ]
        )

        self.botao_selecionar_pasta = ft.ElevatedButton(
            "Selecione o Local de Origem",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=lambda _: self.dialogo_escolher_pasta.get_directory_path(
                dialog_title="Selecione a Pasta de Origem"
            ),
        )
        self.pasta_origem = ft.Text("Pasta de origem: ")
        self.selecionar_pasta_destino = ft.ElevatedButton(
            "Selecione o Local de Destino",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=lambda _: self.dialogo_escolher_pasta.get_directory_path(
                dialog_title="Selecione a Pasta de Destino"
            ),
        )
        self.pasta_destino = TextInfo("Pasta de destino: ")
        self.botao_iniciar_processo = ft.ElevatedButton(
            "Iniciar Cópia", on_click=self.processar_arquivos
        )
        self.texto_informacao_situacao = TextInfo("")
        self.progresso_status = ft.ProgressRing(value=0.0)
        self.adicionar_componetes_pagina()

    def mostra_opcoes(self, e):
        self.page.open(self.drawer)
        self.page.update()

    def pegar_resultado_selecao(self, e: ft.FilePickerResultEvent):
        if e.control.dialog_title == "Selecione a Pasta de Destino":
            if e.path:
                self.pasta_destino.value = f"Pasta de destino: {e.path}"
            else:
                self.pasta_destino.value = (
                    "Pasta de destino: Nenhum Local Selecionado!"
                )
            self.pasta_destino.update()
        else:
            if e.path:
                self.pasta_origem.value = f"Pasta de origem: {e.path}"
            else:
                self.pasta_origem.value = (
                    "Pasta de origem: Nenhum Local Selecionado!"
                )
            self.pasta_origem.update()

    def processar_arquivos(self, evento):
        pasta_origem = self.pasta_origem.value.replace("Pasta de origem: ", "")
        pasta_destino = self.pasta_destino.value.replace(
            "Pasta de destino: ", ""
        )
        if not pasta_origem or "Nenhum Local Selecionado!" in pasta_origem:
            print("Origem Não Selecionada")
            self.alerta_generico("Erro!!!", "Origem Não Selecionada", 3)
            return

        if not pasta_destino or "Nenhum Local Selecionado!" in pasta_destino:
            self.alerta_generico("Erro!!!", "Destino Não Selecionado", 3)
            return
        if not self.lista_filtros:
            self.alerta_generico(
                "Erro!!!", "Nenhum Grupo de arquivo selecionado", 3
            )
            return
        self.iniciar_animacao_processo("Localizando Arquivos")
        lista_arquivos = index_files(pasta_origem, config.configurations)
        self.parar_animacao_processo()
        self.iniciar_animacao_processo("Copiando Arquivos")
        copy_file_to_destination(
            lista_arquivos, self.lista_filtros, pasta_destino
        )
        self.parar_animacao_processo()

    def iniciar_animacao_processo(self, texto_acao):
        self.texto_informacao_situacao.value = texto_acao
        self.progresso_status.value = None
        self.progresso_status.update()
        self.texto_informacao_situacao.update()

    def parar_animacao_processo(self):
        self.texto_informacao_situacao.value = ""
        self.progresso_status.value = 0
        self.progresso_status.update()
        self.texto_informacao_situacao.update()

    def alterar_lista_filtros(self, e):
        if e.control.label not in self.lista_filtros:
            self.lista_filtros.append(str(e.control.label))
            print(self.lista_filtros)
        else:
            self.lista_filtros.remove(str(e.control.label))

    def alerta_generico(self, titulo, mensagem, cor=1):
        cores = {
            1: ft.Colors.GREEN_500,
            2: ft.Colors.LIGHT_BLUE_ACCENT_200,
            3: ft.Colors.RED_400,
        }
        self.page.open(
            ft.AlertDialog(
                title=ft.Text(f"{titulo}"),
                content=ft.Text(f"{mensagem}"),
                bgcolor=cores[cor],
            )
        )

    @staticmethod
    def adicionar_componete_em_container(componente):
        """
        Retorna uma instancia do comopnete Container,
        com as configurações estabeleciadas para o grupo de texto
        """
        return ft.Container(
            content=componente, alignment=ft.alignment.center, padding=7
        )

    def adicionar_componetes_pagina(self):
        for atributo in self.__dict__:
            if atributo not in set(
                [
                    "page",
                    "lista_filtros",
                    "drawer",
                    "tooltip_imagem",
                    "tooltip_documento",
                    "tooltip_planilha",
                    "tooltip_video",
                    "tooltip_audio",
                ]
            ):
                self.page.add(
                    self.adicionar_componete_em_container(
                        getattr(self, atributo)
                    )
                )

    def update_configs_page(self, e):
        # print(vars(self.grupo_tipos_arquivos))
        self.drawer.salvar_opcoes(e)
        config.load_configurations()
        for atributo in self.__dict__:
            if "tooltip" in atributo:
                # print(atributo)
                for config_name in config.configurations.keys():
                    if atributo.split("_")[1] in config_name:
                        getattr(self, atributo).message = f"formatos: {
                            config.configurations[config_name]
                            }"
        self.page.update()
