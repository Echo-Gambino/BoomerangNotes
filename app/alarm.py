from app import Config
import time
import daemon
import webbrowser
import datetime
import pause

config = Config()

ERROR_PATH = config.ERROR_PATH


class Alarm:

    """
    Sets the instance's fields

    Args:
        self: The class object

    Returns:
        None
    """
    def __init__(self):
        self.trigger_datetime = None
        self.reminder_path = ""

    """
    Represents the object as the reminder path and the 
    alarm time that the user needs to be notified.

    Args:
        self: The class object

    Returns:
        output: The string that describes what path is the webbrowser going to open,
                and what datetime will the daemon's managing this object will notify the user
    """
    def __repr__(self):
        output = '<Alarm for {}, will trigger at {}>'.format(
                self.reminder_path, 
                self.sec_to_trigger)
        return output


    """
    Uses the daemon library to launch a daemon executing the method _begin_alarm_daemon(...)

    Args:
        self: The class object

    Returns:
        None
    """
    def start(self):
        with daemon.DaemonContext():
            self._begin_alarm_daemon(
                    self.trigger_datetime,
                    self.reminder_path,
                    ERROR_PATH)
   

    """
    Blocks the process (suspend until instructed/signaled otherwise) 
    until the current time is at or past the given trigger_datetime object.
    Then pops open a webbrowser to the reminder '.html' file or the error file if it failed.

    Args:
        self: The class object
        trigger_datetime: The datetime object
        full_path_to_reminder: The path to the reminder '.html' file
        full_path_to_error: The path to the error '.html' file in case reminder path fails

    Returns:
        None
    """
    def _begin_alarm_daemon(
            self, 
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


