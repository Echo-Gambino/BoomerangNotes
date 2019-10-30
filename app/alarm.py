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

    def start(self):
        with daemon.DaemonContext():
            self._begin_alarm_daemon(
                    self.trigger_datetime,
                    self.reminder_path,
                    ERROR_PATH)
        
    def _begin_alarm_daemon(self, 
            trigger_datetime, 
            full_path_to_reminder,
            full_path_to_error):

        pause.until(trigger_datetime)

        try:
            webbrowser.open_new(full_path_to_reminder)
        except:
            webbrowser.open_new(full_path_to_error)

        exit()


