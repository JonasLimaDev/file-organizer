import flet as ft
from time import sleep
from file_modules.manager_files_and_paths import index_files,copy_file_to_destination



class PageAppFlet():
    def __init__(self,page: ft.Page):
        self.page = page
        self.page.title = "Organizador de Arquivos"
        self.page.window.width = 620       
        self.page.window.height = 680
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.dialogo_selecionar_pasta = ft.FilePicker(
            on_result=self.pegar_resultado_selecao
        )

        self.cabecalho = ft.Text("Organizador de Arquivos", size=20)
        self.lista_filtros = []
        self.informacao_programa = ft.Text(
            "Busca arquivos na pasta de origem e \
            suas subpastas, salvando uma cópia agrupada \
            por tipo de arquivo na pasta de destino".
            replace("            ",""),
            text_align = ft.TextAlign.CENTER,
            size=16
        )

        self.grupo_tipos_arquivos = ft.Column([
            ft.Container(ft.Text(
                "Aceita os Seguintes Grupos de Arquivos:",
                text_align = ft.TextAlign.CENTER,
                size=16),alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Checkbox(label="Imagem", value=False,
                        on_change=self.alterar_lista_filtros,
                        tooltip=ft.Tooltip(
                            message="formatos: .jpg, .jpeg, .png",
                            bgcolor= ft.Colors.BLUE_100,
                            )
                        ),
                        ft.Checkbox(
                            label="Documento", value=False,
                            on_change=self.alterar_lista_filtros,
                            tooltip=ft.Tooltip(
                                message="formatos: .doc, .docx, .pdf",
                                bgcolor= ft.Colors.BLUE_100,
                            )
                        ),
                        ft.Checkbox(
                            label="Planilha", value=False,
                            on_change=self.alterar_lista_filtros,
                            tooltip=ft.Tooltip(
                                message="formatos: .xlsx, .xls, .csv",
                                bgcolor= ft.Colors.BLUE_100,
                            )
                        ),
                        ft.Checkbox(
                            label="Vídeo", value=False,
                            on_change=self.alterar_lista_filtros,
                            tooltip=ft.Tooltip(
                                message="formatos: .mp4, .mkv, .avi",
                                bgcolor= ft.Colors.BLUE_100,
                            )),
                ],
                alignment = ft.MainAxisAlignment.CENTER),
                ),
                ]
        )

        self.botao_selecionar_pasta = ft.ElevatedButton(
                    "Selecione o Local de Origem",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=lambda _: 
                    self.dialogo_selecionar_pasta.
                    get_directory_path(
                        dialog_title="Selecione a Pasta de Origem"
                    ),
                )
        self.pasta_origem = ft.Text("Pasta de origem: ")
        self.selecionar_pasta_destino = ft.ElevatedButton(
                    "Selecione o Local de Destino",
                    icon = ft.Icons.FOLDER_OPEN,
                    on_click = lambda _:
                    self.dialogo_selecionar_pasta.
                    get_directory_path(
                        dialog_title="Selecione a Pasta de Destino"
                    ),
                )
        self.pasta_destino = ft.Text("Pasta de destino: ")
        self.botao_iniciar_processo = ft.ElevatedButton("Iniciar Cópia",on_click = self.processar_arquivos)
        self.texto_informacao_situacao = ft.Text()
        self.progresso_status = ft.ProgressRing(value=0.0)
        self.adicionar_componetes_pagina()
    
    def pegar_resultado_selecao(self, e: ft.FilePickerResultEvent):
        if e.control.dialog_title == "Selecione a Pasta de Destino":
            if e.path:
                self.pasta_destino.value = f"Pasta de destino: {e.path}"
            else:
                self.pasta_destino.value = "Pasta de destino: Nenhum Local Selecionado!"
            self.pasta_destino.update()
        else:
            if e.path:
                self.pasta_origem.value = f"Pasta de origem: {e.path}"
            else:
                self.pasta_origem.value = "Pasta de origem: Nenhum Local Selecionado!"
            self.pasta_origem.update()

    def processar_arquivos(self, evento):
        pasta_origem = self.pasta_origem.value.replace("Pasta de origem: ","")
        pasta_destino = self.pasta_destino.value.replace("Pasta de destino: ","")
        if not pasta_origem or "Nenhum Local Selecionado!" in pasta_origem :
            print("Origem Não Selecionada")
            self.generic_alert("Erro!!!","Origem Não Selecionada",3)
            return
            
        if not pasta_destino or "Nenhum Local Selecionado!"  in pasta_destino  :
            self.generic_alert("Erro!!!", "Destino Não Selecionado", 3)
            return
        if not self.lista_filtros:
            self.generic_alert("Erro!!!", "Nenhum Grupo de arquivo selecionado", 3)
            return
        self.iniciar_animcao_processo("Localizando Arquivos")
        lista_arquivos = index_files(pasta_origem)
        self.parar_animcao_processo()
        self.iniciar_animcao_processo("Copiando Arquivos")
        copy_file_to_destination(lista_arquivos, self.lista_filtros, pasta_destino)
        self.parar_animcao_processo()
    
    def iniciar_animcao_processo(self, texto_acao):
        self.texto_informacao_situacao.value = texto_acao
        self.progresso_status.value = None
        self.progresso_status.update()
        self.texto_informacao_situacao.update()

    def parar_animcao_processo(self):
        self.texto_informacao_situacao.value =""
        self.progresso_status.value = 0
        self.progresso_status.update()
        self.texto_informacao_situacao.update()
        

    def alterar_lista_filtros(self,e):
        
        if e.control.label not in self.lista_filtros:
            self.lista_filtros.append(str(e.control.label))
        else:
            self.lista_filtros.remove(str(e.control.label))

    def generic_alert(self, title, mensagem, cor=1):
        cores = {
            1: ft.Colors.GREEN_500,
            2: ft.Colors.LIGHT_BLUE_ACCENT_200,
            3: ft.Colors.RED_400,
        }
        self.page.open(ft.AlertDialog(
            title=ft.Text(f"{title}"),
            content=ft.Text(f"{mensagem}"),
            bgcolor = cores[cor]
        ))

    def adicionar_componete_em_container(self, componente):
        """
        Retorna uma instancia do comopnete Container,
        com as configurações estabeleciadas para o grupo de texto
        """
        return  ft.Container(
            content=componente,
            alignment=ft.alignment.center,
            padding=7)


    def adicionar_componetes_pagina(self):
        for atributo in self.__dict__:
            if atributo not in  ['page','lista_filtros']:
                self.page.add(
                    self.adicionar_componete_em_container(self.__getattribute__(atributo)))