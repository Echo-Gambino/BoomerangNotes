from app import model
from app import input_utils


class Form:

    # Contants for convenient usage throughout the class
    # GAP is a quick way to standardize seperation of lines 
    # and making the output feel less 'cramped'.
    GAP = 2 * "\n"

    """
    Sets the instance's fields
    
    Args:
        self: The class object

    Returns:
        Nothing
    """
    def __init__(self):
        self.reminder = model.Reminder()
        pass


    """
    Gets the reminder from the class

    Args:
        self: The class object

    Returns:
        self.reminder: The the reminder object that the form constructed and add data onto it
    """
    def get_reminder(self):
        return self.reminder

    
    """
    Begins the form protocol; 
    Guides the user to input the fields that help add information 
    into the self.reminder variable for later use or extraction

    Args:
        self: The class object
        confirm: (default = False) This is a flag indicating that the process
                of prompting the user for inputs would ask the user for confirmation 
                after each entry filled or not.

    Returns:
        None   
    """
    def start_form(self, confirm = False):
        # initialize the input utils
        iUtils = input_utils.InputUtils()

        # display the splash page to introduce the user to the form
        self.splash_intro()

        # this infinite loop is to set up a set series that can be repeated all over again
        # if the user changes their mind and wants to restart all over again.
        while True:
            # Set's the reminder's title
            self.reminder.title = iUtils.get_title(True)

            # Set's the reminder's description
            self.reminder.descr = iUtils.get_descr(True)

            # Set's the reminder's alarm
            self.reminder.alarm = iUtils.get_time(True)

            # Displays the reminder's resulting data after
            # the series of operations.
            self.show_results()

            # if confirm is True, then it it asks for the user to confirm reminder's data,
            # if user refuses (iUtils.get_confirmation() returns False), the loop restarts.
            # if user accepts (iUtils.get_confirmation() returns True), the loop breaks.
            if not confirm or iUtils.get_confirmation():
                break

        # display a splash page to as a outroduction to the program's form
        self.splash_outro()

        pass


    """
    Generates a stylish 'splash page', 
    often used at the begginning of the form protocol

    Args:
        self: The class object

    Returns:
        None
    """
    def splash_intro(self):
        message = "----B-O-0-M-E-R-A-N-G- - <" 

        prompt = Form.GAP + message + Form.GAP

        print(prompt)


    """
    Generates a stylish 'splash page',
    often used at the end of the form protocol

    Args:
        self: The class object

    Returns:
        None
    """
    def splash_outro(self):
        message = "--- Boomerang thrown, have a nice day! --<"

        prompt = Form.GAP + message + Form.GAP

        print(prompt)


    """
    Generates the information from the reminder object,
    often used for the end of the form protocol to let the user review
    the information that the user has put in. (also great for debugging)

    Args:
        self: The class object

    Returns:
        None
    """
    def show_results(self):
        message0 = "Please review reminder info:\n"
        message1 = self.reminder.gen_verbose_description()

        prompt = Form.GAP + message0 + message1 + Form.GAP

        print(prompt) 

