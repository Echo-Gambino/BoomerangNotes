from datetime import datetime


class Reminder:

    """
    Sets the class's instance variables

    Args:
        self: The class's object
    """
    def __init__(self):
        self.title = ""
        self.descr = ""
        self.alarm = datetime.now()


    """
    Represents the class in a string format (acts like reminder.ToString() in Java)

    Args:
        self: The class's object
    """
    def __repr__(self):
        return '<Reminder \"{}\" @ {}>'.format(self.title, self.alarm);
  
    
    """
    Generates a string that describes all of the 
    reminder's data (title, description, alarm time)

    Args:
        self: The class's object
    """
    def gen_verbose_description(self):
        output = ''

        output += "title:\n> {}\n\n".format(self.title)
        output += "description:\n> {}\n\n".format(self.descr)
        output += "delay:\n> {}\n".format(self.conv_time_to_string(self.alarm))

        return output


    """
    A handy function to convert a string into a datetime object

    Args:
        self: The class's object
        string: The string to be converted into the datetime object.
                (preferrably in the format that the function can parse)

    Returns:
        time: The resulting datetime object from converting the string
    """
    def conv_string_to_time(self, string):
        time = None

        # clean the input by removing begginning and trailing whitespace
        string = string.strip()

        try:
            # split the string by the space (' ' character)
            # ex. '9876-08-10 12:30:00' -> ['9876-08-10', '12:30:00']
            token = string.split(' ')

            # convert the splitted strings into integers
            # ex. ['9876-08-10', '12:30:00'] -> [9876, 8, 10] and [12, 30, 0]
            token_date = [int(i) for i in token[0].split('-')]
            token_time = [int(i) for i in token[1].split(':')]

            # place all the integers from the integer list 
            # into the datetime object for initialization
            time = datetime(
                abs(token_date[0]), 		# year
                abs(token_date[1]) % 13, 	# month
                abs(token_date[2]), 		# day
                abs(token_time[0]) % 24, 	# hour
                abs(token_time[1]) % 60, 	# minute
                abs(token_time[2]) % 60 	# second
            )
        except:
            # if anything failed (usually an error while parsing) 
            # set the time to None to signify the operation's failure
            time = None

        return time


    """
    Convert the datetime object into a user readable string

    Args:
        self: The class object
        time: The datetime object that will be converted to string

    Returns:
        prompt: The resulting string object from converting time to string
    """
    def conv_time_to_string(self, time):
        # retrieves the year, month, and day while gauranteeing 
        # that the number of digits displayed is at least 4, 2, 2 respectively
        year = self.conv_num_to_nchar(time.year, 4)
        month = self.conv_num_to_nchar(time.month, 2)
        day = self.conv_num_to_nchar(time.day, 2)

        # retrieves the hour, minute, and seconds while gauranteeing
        # that the number of digits displayed is at least 2, 2, 2 respectively
        hour = self.conv_num_to_nchar(time.hour, 2)
        minute = self.conv_num_to_nchar(time.minute, 2)
        seconds = self.conv_num_to_nchar(time.second, 2)

        # construct the date string and time string with its required data
        prompt_date = "{0}-{1}-{2}".format(year, month, day)
        prompt_time = "{0}:{1}:{2}".format(hour, minute, seconds)

        # combine the date string and time string into one
        prompt = "{0} {1}".format(prompt_date, prompt_time)

        return prompt


    """
    Converts the number (integer type) into a string type, and ensures that 
    the resulting string's length is at least the value of min_length by
    adding '0's to the left side of the converted string.

    Args:
        self: The class's object
        number: The integer to convert
        min_length: The number of digits the resulting string has to AT LEAST have.

    Returns:
        The string from the number's conversion along 
        with added '0's to the left side if applicable.
    """
    def conv_num_to_nchar(self, number, min_length = 0):
        string = str(number)

        while len(string) < min_length:
            string = '0' + string

        return string



