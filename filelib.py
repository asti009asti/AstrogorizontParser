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
        fileref.close()

    @classmethod
    def open_file_for_append(cls, file):
        fullpath = cls.get_project_folder()+file
        fileref = open(fullpath,"a")
        return fileref

    @classmethod
    def add_to_file(cls, file):
        if cls.check_file_exists(file):
            pass


class Reporting(File):

    def __init__(self):
        File.__init__(self)

    @classmethod
    def export_results_to_file(cls, file, story):
        fileref = cls.open_file_for_append(file)
        fileref.write(story)
        fileref.write("\n")
        fileref.close()
