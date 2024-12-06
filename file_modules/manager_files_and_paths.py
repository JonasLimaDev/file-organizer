import os
from .file_classes import FileData
import shutil


def idenfy_type_file(file_extension):
    """
    Define o grupo do arquivo de acordo com a extensão do arquivo
    """
    file_types = {
        "Imagem": ["jpg", "jpeg", "png"],
        "Documento": ["doc", "docx", "pdf"],
        "Planilha": ["xlsx", "csv", "xls"],
        "Vídeo": ["mp4", "mkv", "avi"],
    }
    file_type = "Outros"
    for type in file_types.keys():
        if file_extension in file_types[type]:
            file_type = type
            break
    return file_type


def index_files(folder_selected):
    """
    Busca Todos os arquivos da pasta selecionada e suas subpastas,
    criando uma lista de instâncias da classe FileData com as informações dos arquivos existentes.  
    """
    data_list_files = os.walk(folder_selected)
    total_size_indexed_file = 0
    list_files = []
    for file_data in data_list_files:
        for current_file in file_data[2]:
            if os.path.isfile(f"{file_data[0]}/{current_file}"):
                file_size = os.stat(f"{file_data[0]}/{current_file}").st_size
                list_files.append(
                    FileData(
                        current_file,
                        file_data[0],
                        idenfy_type_file(current_file.split('.')[-1]),
                        os.stat(f"{file_data[0]}/{current_file}"),
                        folder_selected))
                total_size_indexed_file += file_size
                # print(f"localizando arquivos: {total_size_indexed_file / (1024 * 1024) :.2f} MB indexados", end="\r")
    return list_files



def create_folder_hierarchy(full_path, ignore_paths=None):
    """
    Cria a hierarquinha de pastas de destino dos arquivos agrupados
    """
    corrent_path = ""
    full_path = full_path.replace(ignore_paths,"") if ignore_paths else full_path
    folders = full_path.split("\\") if "\\" in full_path else full_path.split("/")
    for folder in folders:
        corrent_path += f"{folder}/"
        if not os.path.isdir(f"{ignore_paths}/{corrent_path}"):
                os.mkdir(f"{ignore_paths}/{corrent_path}")


def get_name_to_save(full_path,name_file):
    prefix = name_file.split('.')[0]
    extension = name_file.split('.')[1]
    new_name_file = name_file
    counter_copies = 1
    while True:
        if os.path.isfile(f"{full_path}/{new_name_file}"):
            new_name_file = f"{prefix}_{counter_copies}.{extension}"
            counter_copies += 1
        else:
            return new_name_file 


def copy_file_to_destination(list_files, list_filters, destination):
    """
    Copia todos os arquivos para a pasta de destino conforme grupos de cada arquivo.
    """
    for file_item in list_files:
        if file_item.type_file in list_filters:
            if not os.path.isdir(f"{destination}/{file_item.type_file}"):
                os.mkdir(f"{destination}/{file_item.type_file}")
            destination_copy = f"{destination}/{file_item.type_file}/{file_item.folder}"
            create_folder_hierarchy(destination_copy,f"{destination}/{file_item.type_file}")
            # print(f"{destination_copy}{file_item.name}")
            name_to_save = get_name_to_save(destination_copy,file_item.name)
            shutil.copy2(file_item.full_path,f"{destination_copy}{name_to_save}",)
            print(f"Copiado: {file_item.name}")