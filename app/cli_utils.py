import os
import argparse


class CliUtils:

    # Constants that the class will suer throughout the object
    ERR_INVALID_FILETYPE = 'Error: Invalid file format. {0} must be a .txt file.'
    ERR_INVALID_PATH = 'Error: Invalid path. Path {0} doesn\'t exist.'

    """
    Automatically sets up the needed arguments that the program will handle
    and parses them to be able to access them immediately.

    Args:
        self: the class object
        description: the application's description for when the user executes '<program>.py -h'

    Returns:
        None
    """
    def __init__(self, description):
        # initiallizes the parser object
        self.parser = argparse.ArgumentParser(description)

        # have the parser add support for the argument of '-I' or '--Import'
        self.parser.add_argument(
                '-I', '--Import',         # retrieve the keyword for the util's arguments
                type = str, nargs = 1,  # retrieve the input type and number of inputs to handle
                metavar = 'file_name',
                default = None,
                help = "Imports the text file.")

        # have the class automatically parses the program's arguments to be readily retrieved
        self.args = self.parser.parse_args()

    """
    Retrieve the imported data from the event that the user imports a file through the program
    ex.
        '<program>.py -I path/to/file.txt'

    Args:
        self: The class object

    Returns:
        string: The contents of the user's specified file in string form.
    """
    def get_imported_data(self):
        # initializes the output
        output = None

        # if import is not valid then return immediately 
        # (user likely did not execute the import argument)
        if self.args.Import == None:
            return output

        # retrieve the argument's value (only one entry),
        # which is the file_path that the program will access and read from
        file_path = self.args.Import[0]

        if not os.path.exists(file_path):
            # if the file path doesn't exist, then send out an 
            # error message explaining that the path specified doesn't exist.
            print(CliUtils.ERR_INVALID_PATH.replace('{0}', file_path))
            return output
        elif not file_path.endswith('.txt'):
            # if the file doesn't end with a .txt file, 
            # then don't try to access it as it has a risk of recieving an invalid input
            print(CliUtils.ERR_INVALID_FILETYPE.replace('{0}', file_path))
            return output

        # open and read the file via the file path, 
        # and store it into the output variable
        with open(file_path, 'r') as file:
            output = file.read()

        # strip the output of beginning and trailing whitespace
        return output.strip()
            



