import os
import shutil

from .file_classes import FileData


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
    for name_type, extesions in file_types.items():
        if file_extension in extesions:
            file_type = name_type
            break
    return file_type


def get_file_by_name(file_class, list_files):
    for file_item in list_files:
        if file_class.name == file_item.name:
            return file_item
    return None


def is_latest_file(file_class, second_file_class):
    if file_class.modified_date > second_file_class.modified_date:
        return True
    else:
        return False


def is_original_file(file_class, second_file_class):
    if file_class.creation_date < second_file_class.creation_date:
        return True
    else:
        return False


def decide_file_copies(list_files, current_file, duplicate_file, option):
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


def index_files(folder_selected, configuration=None):
    """
    Busca Todos os arquivos da pasta selecionada e suas subpastas,
    criando uma lista de instâncias da classe FileData com as
    informações dos arquivos existentes.
    """
    data_list_files = os.walk(folder_selected)
    total_size_indexed_file = 0
    list_files = []

    for file_data in data_list_files:
        if "." in str(file_data[0]):
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
                        idenfy_type_file(current_file.split(".")[-1]),
                        os.stat(f"{file_data[0]}/{current_file}"),
                        folder_selected,
                    )
                    duplicate_file = get_file_by_name(
                        instance_file_data, list_files
                    )
                    if duplicate_file:
                        list_files = decide_file_copies(
                            list_files,
                            instance_file_data,
                            duplicate_file,
                            configuration,
                        )
                    else:
                        list_files.append(instance_file_data)
                        total_size_indexed_file += file_size

                # print(f"localizando arquivos:
                # {total_size_indexed_file / (1024 * 1024) :.2f}
                #  MB indexados", end="\r")
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
    prefix = name_file.split(".")[0]
    extension = name_file.split(".")[1]
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
            # print(f"{destination_copy}{file_item.name}")
            name_to_save = get_name_to_save(destination_copy, file_item.name)
            shutil.copy2(
                file_item.full_path,
                f"{destination_copy}{name_to_save}",
            )
            print(f"Copiado: {file_item.name}")
