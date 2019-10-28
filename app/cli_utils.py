import os
import argparse


class CliUtils:
    ERR_INVALID_FILETYPE = 'Error: Invalid file format. {0} must be a .txt file.'
    ERR_INVALID_PATH = 'Error: Invalid path. Path {0} doesn\'t exist.'


    def __init__(self, description):
        # initiallizes the parser object
        self.parser = argparse.ArgumentParser(description)

        self.parser.add_argument(
                '-I', '--Import',         # retrieve the keyword for the util's arguments
                type = str, nargs = 1,  # retrieve the input type and number of inputs to handle
                metavar = 'file_name',
                default = None,
                help = "Imports the text file.")

        self.args = self.parser.parse_args()


    def get_imported_data(self):
        output = None

        if self.args.Import == None:
            return output

        file_path = self.args.Import[0]

        if not os.path.exists(file_path):
            print(CliUtils.ERR_INVALID_PATH.replace('{0}', file_path))
            return output
        elif not file_path.endswith('.txt'):
            print(CliUtils.ERR_INVALID_FILETYPE.replace('{0}', file_path))
            return output

        with open(file_path, 'r') as file:
            output = file.read()

        return output.strip()
            



