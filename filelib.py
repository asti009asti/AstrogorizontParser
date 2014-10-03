import os


class File:

    def __init__(self):
        pass

    @classmethod
    def get_project_folder(cls):
        folder = os.path.realpath(__file__)
        fullpath = folder[0:len(folder)-len(os.path.basename(__file__))]
        return fullpath

    @classmethod
    def check_file_exists(cls, file):
        if os.path.isfile("./"+file) and os.access("./"+file, os.R_OK):
            return True
        else:
            return False

    @classmethod
    def clear_file(cls, file):
        fullpath = cls.get_project_folder() + file
        open(fullpath, "w").close()

    @classmethod
    def create_file(cls, file):
        fullpath = cls.get_project_folder()+file
        fileref = open(fullpath, "w")
        return fileref

    @classmethod
    def add_to_file(cls,file):
        if cls.check_file_exists(file):
            pass


class ConfigFile(File):

    @classmethod
    def read_config(self, file):
        pass


class Reporting(File):

    def export_results_to_file(self):
        pass