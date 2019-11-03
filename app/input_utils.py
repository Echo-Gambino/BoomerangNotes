from datetime import datetime
import os
import subprocess
from time import sleep
from app import Config


config = Config()

TEXT_EDITOR = config.TEXT_EDITOR
TEMP_PATH = config.TEMP_PATH


class InputUtils:

    # retrieve the user's inputs for prompting a 'title' input
    """
    Retrieve the user's inputs for prompting a 'title' input

    Args:
        self: The class object
        confirm: A flag to dictate if confirmation will be prompted after submitting the input

    Returns:
        A string object resulted from guiding the user to input a 'title'
    """
    def get_title(self, confirm = False):
        prompt = "What is the subject of your reminder?"
        return self.get_input_from_prompt(prompt, confirm)

    
    """
    Retrieve the user's inputs for prompting a 'description' input

    Args:
        self: The class object
        confirm: A flag to dictate if confirmation will be prompted after submitting the input

    Returns:
        A string object resulted from guiding the user to input a 'description'
    """
    def get_descr(self, confirm = False):
        prompt = "Please add to the reminder by providing a description."
        output = ""

        if (TEXT_EDITOR != ""):
            try:
                output = self.get_input_from_textfile(prompt, confirm)
            except:
                print("\n\n\n\nError: Something went wrong with getting the input from \'{0}\', the text editor, please input the description through this interface instead.\n".format(TEXT_EDITOR))
                output = self.get_input_from_prompt(prompt, confirm)
        else:
            output = self.get_input_from_prompt(prompt, confirm)

        return output


    """
    Retrieve the user's inputs for prompting a 'time' input

    Args:
        self: The class object
        confirm: A flag to dictate if confirmation will be prompted after submitting the input

    Returns:
        A datetime object resulted from guiding the user to input a 'time'
    """
    def get_time(self, confirm = False):
        prompt = 'Please set the time at which you would like to be reminded at:\n'
        return self.get_input_for_time(prompt, confirm)


    # guides the user through to input value(s) that can construct a datetime() object
    """
    Guides the user through to input value(s) that can construct a datetime() object

    Args:
        self: The class object
        prompt: The prompt string thats displayed before the input is available to be retrieved
        confirm: A flag to dictate if confirmation will be prompted after submitting the input

    Returns:
        The datetime object resulted from the user's input
    """
    def get_input_for_time(self, prompt, confirm = False):
        # initializes the user's set time (simply to declare it)
        user_time = datetime.now()

        # sets up the formatting instructions on how to input values
        # that the program can parse useful information from.
        format_instructions = "Please input in this format:\nYYYY-MM-DD hh:mm:ss"

        while True:
            # print out a custom message to prompt the user
            print(prompt)
            # update the user on the current time (designed to be used as a reference point)
            print("It is currently {}.\n".format(datetime.now()))
            # print out the formatting instructions to ensure that
            # the user can figure out how to submit the proper input.
            print(format_instructions)

            # retrieve the user's input in string form
            user_input = self.get_input()

            # this try & except statement is make an attempt to
            # parse user_input's values and convert it into datetime,
            # if the attempt fails, it prevents crashing 
            # (this is because we 99.99% know that this is due to an invalid string)
            # and restarts this process of retrieving user inputs and converting it to datetime.
            try:
                # As a way to help understand why this code performs 
                # the operation below, here is an example of a 'proper' input:
                #
                # 2010-04-29 23:21:01
                #

                # split the input by ' '
                # from the example input above, it would result in:
                #
                # ['2010-04-29', '23:21:01']
                token = user_input.split(' ')

                # split the inputs by '-' and ':' for the first and second token respectively
                # then convert the resulting values in the list to an integer
                # from the example input, it would result in:
                #
                # token_date = [2010, 4, 29]
                # token_time = [23, 21, 1]
                token_date = [int(i) for i in token[0].split('-')]
                token_time = [int(i) for i in token[1].split(':')]

                # place all the values of token_date and token_time into datetime(...)
                user_time = datetime(
                    abs(token_date[0]), abs(token_date[1]) % 13, abs(token_date[2]),
                    abs(token_time[0]) % 24, abs(token_time[1]) % 60, abs(token_time[2]) % 60)
            except:
                # print an error statement and restart the date input collection process over again
                print("Error, input not recognized, please input the time in the format specified\n")
                continue

            # print out a little message to allow the user see if this is what they truly want 
            # (good for debugging personally speaking)
            print("You have set the reminder time to be:\n{}".format(self.conv_time_to_string(user_time)))

            # if we seek confirmation (from the variable confirm),
            # then prompt the user for confirmation,
            # if the user confirms positively (normally a 'yes')
            # then break from the infinite loop and continue with the execution
            if not confirm or self.get_confirmation():
                break

        return user_time


    """
    Converts the a datetime object to a string of the format 'YYY-MM-DD hh:mm:ss'

    Args:
        self: The class object
        time: The datetime object that will be converted to string

    Returns:
        prompt: A string describing the information from the datetime object 
                (e.g. year, month, day, hour, minute, second)
    """
    def conv_time_to_string(self, time):
        # retrieve the year, month, and day 
        # (also adds '0's to ensure values like years equalling '230' is '0230')
        year = self.conv_num_to_nchar(time.year, 4)
        month = self.conv_num_to_nchar(time.month, 2)
        day = self.conv_num_to_nchar(time.day, 2)

        # retrieve the hour, minute, and seconds
        # (also adds '0's to ensure values like seconds equalling '0' is '00')
        hour = self.conv_num_to_nchar(time.hour, 2)
        minute = self.conv_num_to_nchar(time.minute, 2)
        seconds = self.conv_num_to_nchar(time.second, 2)

        # slot the values into the strings to form a full date string and a full time string
        prompt_date = "{0}-{1}-{2}".format(year, month, day)
        prompt_time = "{0}:{1}:{2}".format(hour, minute, seconds)

        # combine the date string and time string into one for the output
        prompt = "{0} {1}".format(prompt_date, prompt_time)

        return prompt

    """
    A helper function that converts a number to an string such that the string's length 
    is at least equal to the value of min_length by adding '0's to the left side of the string
    
    EXAMPLE:
        arguments:
            number = 1203
            min_length = 6
        returns:
            output = '001203'
    
        arguments:
            number = 1203
            min_length = 4
        returns:
            output = '1203'
    
    Args:
        self: The class object
        number: The integer that will be converted to string
        min_length: The minimum length (number of digits) that 
                    the converted string must at least have

    Returns:
        string: The number's string form, and '0's to the left of the given number's value
                if the number's digits are less than the value of min_length
    """
    def conv_num_to_nchar(self, number, min_length = 0):
        # converts number into a string
        string = str(number)

        # while the string's length is less than the value of min_length,
        # add a '0' to the LEFT side of string
        while len(string) < min_length:
            string = '0' + string

        return string

    
    """
    Get the user's input from a designated, temporary textfile 
    using a texteditor specified by config.py

    The reason why this is used is to allow the user to input data 
    much in the same way like a normal, modern day textbox would be 
    (like mouse support, copy and paste, etc)

    Args:
        self: The class object
        prompt: The prompt string thats displayed before the input is available to be retrieved
        confirm: A flag to dictate if confirmation will be prompted after submitting the input

    Returns:
        The string object resulted from the user's input
    """
    def get_input_from_textfile(self, prompt, confirm = False):
        user_input = ''

        # wipe all data from TEMP_PATH
        open(TEMP_PATH, 'w').close()

        while True:
            print(prompt)

            # construct command (text_editor and full path) and execute it
            # to open the designated text editor that the user can write into
            subprocess.Popen([TEXT_EDITOR, TEMP_PATH]).wait()

            # open the same file (which should be updated by the user)
            # and gather all the text within it to be placed into the data variable
            data = ''
            with open(TEMP_PATH, 'r') as file:
                data = file.read()

            # clean out the user data and place it into user_input
            user_input = data.strip()

            # print out the result of reading the tmp file
            # just to that the user can preview what they wrote down
            print('Here is what you have wrote down:')
            print(user_input)
            
            if not confirm:
                # take no further confirmation from the user
                break
            else:
                if (self.get_confirmation()):
                    # if the confirmation from the user is positive (like a 'yes' response)
                    # then continue to execution past the infinite loop
                    break
                else:
                    # set up a prompt for editing
                    edit_prompt = "would you like to continue where you left off (y), or would you like to write the description from scratch (n)?"
                    # get confirmation as to whether or not the user would like to retain their progress or not
                    user_will_edit = self.get_confirmation(edit_prompt)
                    if not user_will_edit:
                        # if the confirmation is negative, then that means that they wish to restart.
                        # so set the temporary file to a blank slate
                        open(TEMP_PATH, 'w').close()
                    continue

        # once we have what we ultimately need (the user's input in the form of a string)
        # attempt to destroy the temporary file just so that we don't leave anything sensitive behind
        # but if something goes wrong (as it normally happens in terms of getting information from IO)
        # we notify the user of this error and explain that we cannot remove it.
        try:
            os.remove(TEMP_PATH)
        except:
            print('Error, could not remove {0}'.format(TEMP_PATH))

        return user_input

    """
    Gets the input from the command line of the terminal (via python3's input() function)

    Args:
        self: The class object
        prompt: The prompt string that displayed before the input is available to be retrieved
        confirm: A flag to dictate if confirmation will be prompted after submitting the input

    Returns:
        The string object resulted from the user's input
    """
    def get_input_from_prompt(self, prompt, confirm = False):
        user_input = ''

        while True:
            # print out the prompt
            print(prompt)

            # retrieve the user's input (essentially input().strip())
            user_input = self.get_input()

            # ask for confirmation to continue or restart if confirm == True
            if not confirm or self.get_confirmation():
                break

        return user_input


    """
    The function is a generic helper function that asks the user to input a binary answer 
    (usually 'yes' or 'no'), this is normally used for confirming the user's inputs.

    Args:
        self: The class object
        prompt: The prompt string thats displayed before the input is available to be retrieved
        default: The submittion that will be defaulted if the user selects nothing
                    (i.e. inputs a whitespace, or presses the enter key)

    Returns:
        A boolean (True or False) to determine if the confirmation
        is received positively (True) or negatively (False)
    """
    def get_confirmation(self, prompt = 'Confirm?', default = 'y'):

        YES = True
        NO = False

        input_dict = {
                'y': YES,
                'n': NO
                }
        
        option0 = 'y'
        option1 = 'n'

        # set the default ('' input or *pressing enter*) to result in a True or False
        # example: 
        #   if default == 'y', then pressing enter would make this function return True
        #   if default == 'n', then pressing enter would make this function return False
        if default.lower() == 'y':
            input_dict[''] = YES
            option0 = '[Y]'
        elif default.lower() == 'n':
            input_dict[''] = NO
            option1 = '[N]'

        # assume that the user input is already 'y'
        user_input = 'y'

        while True:
            # print the prompt and its options
            print('{0} {1}/{2}'.format(prompt, option0, option1))

            # get the input (and clean it)
            user_input = self.get_input(True).replace(' ', '').replace('\n', '').replace('\t', '')

            # if user_input isn't valid (not in the input_dict's key values)
            # then it prints an error message and restarts.
            # else it breaks out of the loop and continues the execution
            if not user_input in input_dict.keys():
                print("Error, invalid input, please try typing \'y\' or \'n\'.")
                continue
            else:
                break

        return input_dict[user_input]


    """
    A helper function that retrieves the user's input 
    and does basic data sanitization (like removing beginning and trailing whitespace)

    Args:
        self: The class object
        lowercase: The flag that determines if the returned value is 
                    converted to all lowercase characters or not

    Returns:
        user_input: A string object from the user's input 
                    in the terminal interface of the program
    """
    def get_input(self, lowercase = False):
        # retrieves the user's input and strips it of beginning and trailing whitespace
        user_input = input("< ").strip()

        if (lowercase):
            # if lowercase == True, then lowercase it.
            user_input = user_input.lower()

        return user_input


    """
    A simple display output to print out a string in a noticable fashion

    Args:
        self: The class object
        string: The given string to be displayed

    Returns:
        None
    """
    def debug_display_output(self, string):
        stars = 3 * "_"

        print("{}.{}.{}".format(stars, string, stars))

    pass

