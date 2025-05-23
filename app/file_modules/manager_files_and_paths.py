import os
import shutil
import logging
from .file_classes import FileData, FileTypes

# Configuração para saída em um arquivo
logging.basicConfig(filename='file_logs.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Falha')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('falhas.log',  encoding='utf-8',)
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def idenfy_type_file(file_extension, file_types):
    """
    Define o grupo do arquivo de acordo com a extensão do arquivo
    """
    file_type = "Outros"
    for name_type, extesions in file_types.items():
        if file_extension in extesions:
            file_type = name_type
            break
    return file_type


def get_file_by_name(file_class, list_files):
    """
    Retorna o primeiro arquivo encontrado na lista de acordo com o nome.

    """
    for file_item in list_files:
        if file_class.name == file_item.name:
            return file_item
    return None


def is_latest_file(file_class, second_file_class):
    """Mostra se o arquivo tem data de modificação superior ao comparado"""
    if file_class.modified_date > second_file_class.modified_date:
        return True
    else:
        return False


def is_original_file(file_class, second_file_class):
    """Mostra se o arquivo tem data de criação inferior ao comparado"""
    if file_class.creation_date < second_file_class.creation_date:
        return True
    else:
        return False


def decide_file_copies(list_files, current_file, duplicate_file, option):
    """
    Decide o comportamento de cópia de arquivo, conforme configuração passada
    """
    match option:
        case "manter":
            list_files.append(current_file)
        case "recente":
            if is_latest_file(current_file, duplicate_file):
                list_files.append(current_file)
                list_files.remove(duplicate_file)
        case "original":
            if is_original_file(current_file, duplicate_file):
                list_files.append(current_file)
                list_files.remove(duplicate_file)
        case None:
            list_files.append(current_file)
    return list_files


def index_files(folder_selected, configuration):
    """
    Busca Todos os arquivos da pasta selecionada e suas subpastas,
    criando uma lista de instâncias da classe FileData com as
    informações dos arquivos existentes.
    """
    data_list_files = os.walk(folder_selected)
    total_size_indexed_file = 0
    list_files = []
    file_types = FileTypes(configuration)
    file_types.update_types_files()

    for file_data in data_list_files:
        if any(["." in folder for folder in file_data[0].split("/")]):
            continue
        for current_file in file_data[2]:
            if current_file[0] != ".":
                if os.path.isfile(f"{file_data[0]}/{current_file}"):
                    file_size = os.stat(
                        f"{file_data[0]}/{current_file}"
                    ).st_size
                    instance_file_data = FileData(
                        current_file,
                        file_data[0],
                        idenfy_type_file(
                            current_file.split(".")[-1], file_types.types
                        ),
                        os.stat(f"{file_data[0]}/{current_file}"),
                        folder_selected,
                        configuration["niveis-mantidos"],
                    )
                    duplicate_file = get_file_by_name(
                        instance_file_data, list_files
                    )
                    if duplicate_file:
                        list_files = decide_file_copies(
                            list_files,
                            instance_file_data,
                            duplicate_file,
                            configuration["opcoes-copia"],
                        )
                    else:
                        list_files.append(instance_file_data)
                        total_size_indexed_file += file_size
    return list_files


def create_folder_hierarchy(full_path, ignore_paths=None):
    """
    Cria a hierarquinha de pastas de destino dos arquivos agrupados
    """
    corrent_path = ""
    full_path = (
        full_path.replace(ignore_paths, "") if ignore_paths else full_path
    )
    folders = (
        full_path.split("\\") if "\\" in full_path else full_path.split("/")
    )
    for folder in folders:
        corrent_path += f"{folder}/"
        if not os.path.isdir(f"{ignore_paths}/{corrent_path}"):
            os.mkdir(f"{ignore_paths}/{corrent_path}")


def get_name_to_save(full_path, name_file):
    """
    Faz numeração dos nomes de arquivos com cópias para salvar no mesmo destino
    """
    prefix = name_file.split(".")[0]
    extension = name_file.split(".")[1]
    new_name_file = name_file.replace("\n","")
    counter_copies = 1
    while True:
        if os.path.isfile(f"{full_path}/{new_name_file}"):
            new_name_file = f"{prefix}_{counter_copies}.{extension}"
            counter_copies += 1
        else:
            return new_name_file


def copy_file_to_destination(list_files, list_filters, destination, option):
    """
    Copia todos os arquivos para a pasta de destino conforme
    grupos de cada arquivo.
    """
    for file_item in list_files:
        if file_item.type_file in list_filters:
            if not os.path.isdir(f"{destination}/{file_item.type_file}"):
                os.mkdir(f"{destination}/{file_item.type_file}")
            destination_copy = (
                f"{destination}/{file_item.type_file}/{file_item.folder}"
            )
            create_folder_hierarchy(
                destination_copy, f"{destination}/{file_item.type_file}"
            )
            if option == "manter":
                name_to_save = get_name_to_save(
                    destination_copy, file_item.name
                )
            else:
                name_to_save = file_item.name
            try:
                shutil.copy2(
                    file_item.full_path,
                    f"{destination_copy}{name_to_save}",
                )
                logging.info(f'Copia Realizada - {file_item.full_path} para {destination_copy}{name_to_save}')
            except  Exception as e:
                # print(f"Erro ao tentar copiar arquivo: {name_to_save}")
                logging.error(f'Erro: {e}')
                logging.error(f'Não Foi Possível Copiar - {file_item.full_path}')
                logger.info(f' {file_item.full_path} | para | {destination_copy}{name_to_save}')
                
