from app import *
import time
import daemon

DATA_PATH = '/data/'

def main():
    # What is needed
    #   title
    #   description
    #   reminder time

    f = form.Form()
    
    f.start_form()

    reminder = f.get_reminder()

    # reminder = model.Reminder()

    """
    reminder.title = input("title: ")

    reminder.descr = input("description: ")

    reminder.alarm = input("reminder time: ")
    """

    """
    print("\n\n\n")
    print(20 * "* ")
    print("\n")

    print("title: {0}".format(reminder.title))
    print("description: {0}".format(reminder.descr))
    print("reminder_time: {0}".format(reminder.alarm))

    print("\n")
    print(reminder)
    print("\n")
    """

    reminder_webpage = ""

    with open('app/template/base.html', 'r') as file:
        data = file.read()

        data = data.replace('{0}', reminder.title)
        data = data.replace('{1}', reminder.descr)

        reminder_webpage = data

    with open('.' + gen_reminder_path(reminder), 'w') as file:
        data = file.write(reminder_webpage)

    set_alarm(reminder)

def gen_working_dir():
    return os.path.dirname(os.path.realpath(__file__))

def gen_reminder_path(reminder):
    output = "{0}{1}_Reminder.html".format(DATA_PATH, reminder.title)
    return output

def set_alarm(reminder):
    reminder_daemon = alarm.Alarm()

    reminder_daemon.alarm_delay = 2
    reminder_daemon.path_to_reminder = gen_reminder_path(reminder)
    reminder_daemon.working_dir = gen_working_dir()

    reminder_daemon.start()

if __name__ == "__main__":
    main()



