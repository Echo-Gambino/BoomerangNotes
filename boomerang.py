from app import *
from app import Config
import time
import daemon
import argparse


config = Config()

APP_DESCRIPTION = config.APP_DESCRIPTION


# main function where all processes of boomerang.py begin
def main():
    # set up cli utilities object with the app's description on '-h' as object
    cli = cli_utils.CliUtils(APP_DESCRIPTION)

    # set the reminder to be a place holder
    reminder = None

    if cli.args.Import != None:
        # if the user gives an argument of '-I' along with the app,
        # then execute the 'import' protocol.
        # (User's included text file will be parsed for fields like title, description, and time into a reminder object)
        reminder = get_reminder_via_import(cli)
    else:
        # if the user gives no argument along with the app
        # then execute the 'form' protocol.
        # (User is prompted to input fields like title, description, and time into a reminder object)
        reminder = get_reminder_via_form()

    # convert the reminder to an '.html' file to be opened at a later time
    conv_reminder_to_webpage(reminder)

    # launch a daemon whose responsibility is to notify the user at a certain time
    set_alarm(reminder)

    return


# the function that executes the 'import file' protocol 
def get_reminder_via_import(cli):
    # using the given cli object, retrieve the data from
    # the user's specified file (in the form of a string) 
    data = cli.get_imported_data()

    # parse the data (str) into a reminder object (Reminder)
    reminder = file_parser(data)

    # throw a built-in exception if the reminder is None.
    # this is because we are unale recover from this, so we might as well terminate here.
    if reminder == None:
        raise RuntimeError('import failed to retrieve reminder')

    # spits out an overview to reflect what the user has inputted
    # and what information will be reminded and at what time.
    # (great for peace of mind to review it as a user, and also great for debugging)
    print(reminder.gen_verbose_description())

    return reminder


# the function that executes the 'prompt fillable form' protocol
def get_reminder_via_form():
    # initialize the Form() object
    f = form.Form()

    # start the form (a one-stop-shop for guiding the user to fill out fields such as the title, description, time, etc)
    f.start_form()

    # retrieve the reminder from the form object
    reminder = f.get_reminder()

    return reminder


# the function that takes the data within the reminder to generate a '.html' file
def conv_reminder_to_webpage(reminder):
    # the webpage's contents in HTML format
    reminder_webpage = ""

    # open 'base.html' to be a template, and have reminder's data to be put into its designated positions
    with open('app/template/base.html', 'r') as file:
        # retrieve the file data of base.html
        data = file.read()

        # add the title and (formatted) description into its designated positions
        # its essentially 'data = " -- data's string value -- ".format(title, description)'
        data = data.replace('{0}', reminder.title)
        data = data.replace('{1}', reminder.descr.replace('\n', '<br>\n'))

        # save the data's value into reminder_webpage
        reminder_webpage = data

    # open the path to a generated reminder file and write the data into it
    with open(config.get_reminder_path(reminder.title), 'w') as file:
        data = file.write(reminder_webpage)

    return


# from the given data (str), parse it to retrieve the 
# title, description, and reminder time and compile it to a reminder object
def file_parser(data):
    # if data isn't valid, then return with nothing (as there is nothing to parse)
    if data == None: return None

    # initialize the reminder
    reminder = model.Reminder()

    # split the file data (in string form) into a list of lines
    lines = data.split('\n')

    # main loop, for each line,
    # add all but those with '#' as their first character in a line (acts as comments or special descriptors)
    # process lines with '#' as their first character to possibly retrieve information to add onto reminder (not always)
    body = ''
    for l in lines:
        if len(l) != 0:
            if l[0] == '#':
                # we leave out hashtags from the body
                # IF they are the FIRST character of the line!
                process_hash(reminder, l)
                continue
        body += l + '\n'

    # add the accumulated lines that body has amassed into reminder
    reminder.descr = body

    return reminder


def process_hash(reminder, line):
    # IF the given line is a valid metadata tag, then it should follow this format
    #
    # #<metadata category>: <value>
    #

    # Remove the beginning and trailing whitespace and newlines
    # along with the hashtag (#) character,
    # so that we can properly evaluate the string
    proc_line = line.strip()[1:]

    # if proc_line is empty without the hash, then don't bother to process
    if len(proc_line) == 0:
        return

    # split ': ' to leave only the header and its value
    proc_token = proc_line.split(': ')
   
    # for proc_token to be deemed valid, it must have exactly two tokens, 
    # so 'fail' the ones that don't meet those requirements.
    if len(proc_token) < 2:
        return
    elif len(proc_token) > 2:
        raise RuntimeError(
                'Format Error: #-tag operation can only take one \': \' on line:\n> \'{}\''.format(proc_line))

    # retrieve the header and value from proc_token
    header = proc_token[0]
    value = proc_token[1]
    
    # if any values taken from proc_token are empty (length of 0), 
    # then its not valid, and we cannot retrieve any information from it
    if len(header) == 0:
        return
    if len(value) == 0:
        return

    # perform a specialized operation depending on the header's value
    if header == 'title':
        # set the reminder's title to value
        reminder.title = value
    elif header == 'time':
        # set the reminder's reminder time to value (after conversion of course)
        reminder.alarm = reminder.conv_string_to_time(value)
    else:
        # ignore all others
        pass

    return


# a method that conveniently sets an alarm daemon that pops up a webbrowser
# displaying the reminder's information at a designated time.
def set_alarm(reminder):
    # initialize the Alarm() object
    reminder_daemon = alarm.Alarm()

    # add values into the the object (alarm time, and reminder path)
    reminder_daemon.trigger_datetime = reminder.alarm
    reminder_daemon.reminder_path = config.get_reminder_path(reminder.title)

    # start the reminder daemon to run in the background
    reminder_daemon.start()


if __name__ == "__main__":
    main()



