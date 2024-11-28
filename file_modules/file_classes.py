from threading import Thread

class FileData:
    def __init__(self, name, path, type_file, size, path_root=None, level_hierarchy=2):
        self.name = name
        self.path = path
        self.type_file = type_file
        self.size = size
        # self.folder = path.split("\\")[-1] if "\\" in path else path.split('/')[-1]
        self.folder = self.get_folder(level_hierarchy,path_root) if path_root else self.get_folder(level_hierarchy) 
        self.full_path = f"{self.path}/{self.name}"
        print(self.get_folder(2))
        # self.folder_level = 
    
    def get_folder(self, level, path_ignore=None):
        
        
        path_current = self.path.replace(path_ignore,"") if path_ignore else self.path
        list_folders = path_current.split("\\") if "\\" in path_current else path_current.split('/')
        final_folder = ""
        while True:
            if len(list_folders) < level:
                level-=1
            else:
                folders_selected = list_folders[:-(level+1):-1]
                for folder in folders_selected[::-1]:
                    final_folder += f"{folder}/"
                # folder = [f"{pasta}/" for pasta in list_folders[::-(level)]]
                # print(folder)
                return final_folder


