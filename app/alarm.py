from app import Config
import time
import daemon
import webbrowser
import datetime
import pause

config = Config()

WORKING_DIR = config.WORKING_DIR
ERROR_PATH = config.ERROR_PATH

class Alarm:

    def __init__(self):
        self.trigger_datetime = None
        self.reminder_path = ""

    def __repr__(self):
        output = '<Alarm for {} with {} sec delay>'.format(
                WORKING_DIR, 
                self.sec_to_trigger)
        return output

    # a method that uses the daemon library to launch a daemon executing
    # the method _begin_alarm_daemon(...)
    def start(self):
        with daemon.DaemonContext():
            self._begin_alarm_daemon(
                    self.trigger_datetime,
                    self.reminder_path,
                    ERROR_PATH)
    
    # the function that waits until the current time 
    # (designated from the pause library, I believe is the OS's time but I'm unsure)
    # and then pops open a webbrowser to the reminder '.html' file or the error file if it failed.
    def _begin_alarm_daemon(self, 
            trigger_datetime, 
            full_path_to_reminder,
            full_path_to_error):

        # wait until the current time has reached or passed trigger_datetime 
        pause.until(trigger_datetime)

        # attempt to open the reminder's HTML file, if it failed,
        # then open a preset error file to notify the user with.
        try:
            webbrowser.open_new(full_path_to_reminder)
        except:
            webbrowser.open_new(full_path_to_error)

        # exit the process for daemons (just to make sure that they do)
        exit()


