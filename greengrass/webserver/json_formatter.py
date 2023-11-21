import sys
import os.path

class JsonFormatter():
    def __init__(self):
        pass

    def convert_to_string(self, file):
        # check file exists
        if os.path.isfile(file) is False:
            print('File not found: ' + file)

        # get a file object and read it in as a string
        fileobj = open(file)
        jsonstr = fileobj.read()
        fileobj.close()

        # do character conversion here
        outstr = jsonstr.replace('"', '"').replace('\n', '').replace(' ', '')

        # return the converted string
        return outstr