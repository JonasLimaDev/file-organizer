from datetime import datetime


class FileData:
    def __init__(self, name, path, type_file, file_stat, *args):
        self.name = name
        self.path = path
        self.type_file = type_file
        self.path_root = args[0] if args[0] else None
        if len(args) > 1:
            self.level_hierarchy = args[1]
        else:
            self.level_hierarchy = 2
        if self.path_root:
            self.folder = self.get_folder(self.level_hierarchy, self.path_root)
        else:
            self.get_folder(self.level_hierarchy)
        self.full_path = f"{self.path}/{self.name}"
        self.size = file_stat.st_size
        self.creation_date = self.time_convert(file_stat.st_ctime)
        self.modified_date = self.time_convert(file_stat.st_mtime)

    @staticmethod
    def time_convert(atime):
        newtime = datetime.fromtimestamp(atime)
        return newtime.date()

    def get_folder(self, level, path_ignore=None):
        """Identifica a hierarquia de pasatas do arquivo"""
        path_current = (
            self.path.replace(path_ignore, "") if path_ignore else self.path
        )
        list_folders = (
            path_current.split("\\")
            if "\\" in path_current
            else path_current.split("/")
        )
        final_folder = ""
        while True:
            if len(list_folders) < level:
                level -= 1
            else:
                folders_selected = list_folders[: -(level + 1) : -1]
                for folder in folders_selected[::-1]:
                    final_folder += f"{folder}/"
                return final_folder
