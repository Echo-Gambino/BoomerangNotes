from app import *
from app import Config
import time
import daemon
import argparse


config = Config()

APP_DESCRIPTION = config.APP_DESCRIPTION

def main():
    # What is needed
    #   title
    #   description
    #   reminder time

    cli = cli_utils.CliUtils(APP_DESCRIPTION)

    reminder = None

    if cli.args.Import != None:
        reminder = get_reminder_via_import(cli)
    else:
        reminder = get_reminder_via_form()

    conv_reminder_to_webpage(reminder)

    set_alarm(reminder)

    return


def get_reminder_via_import(cli):
    data = cli.get_imported_data()

    reminder = file_parser(data)

    if reminder == None:
        raise RuntimeError('import failed to retrieve reminder')

    print(reminder.gen_verbose_description())

    return reminder


def get_reminder_via_form():
    f = form.Form()

    f.start_form()

    reminder = f.get_reminder()

    return reminder


def conv_reminder_to_webpage(reminder):
    reminder_webpage = ""

    with open('app/template/base.html', 'r') as file:
        data = file.read()

        data = data.replace('{0}', reminder.title)
        data = data.replace('{1}', reminder.descr.replace('\n', '<br>\n'))

        reminder_webpage = data

    with open(config.get_reminder_path(reminder.title), 'w') as file:
        data = file.write(reminder_webpage)

    return


def file_parser(data):
    if data == None: return

    reminder = model.Reminder()

    # split the file data (in string form) into a list of lines
    lines = data.split('\n')

    body = ''
    for l in lines:
        if len(l) != 0:
            if l[0] == '#':
                # we leave out hashtags from the body
                # IF they are the FIRST character of the line!
                process_hash(reminder, l)
                continue
        body += l + '\n'

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

    proc_token = proc_line.split(': ')
   
    if len(proc_token) < 2:
        return
    elif len(proc_token) > 2:
        raise RuntimeError(
                'Format Error: #-tag operation can only take one \': \' on line:\n> \'{}\''.format(proc_line))

    header = proc_token[0]
    value = proc_token[1]
    
    if len(header) == 0:
        return
    if len(value) == 0:
        return

    if header == 'title':
        reminder.title = value
    elif header == 'time':
        reminder.alarm = reminder.conv_string_to_time(value)
    else:
        pass

    return


def set_alarm(reminder):
    reminder_daemon = alarm.Alarm()

    reminder_daemon.trigger_datetime = reminder.alarm
    reminder_daemon.reminder_path = config.get_reminder_path(reminder.title)

    reminder_daemon.start()


if __name__ == "__main__":
    main()



