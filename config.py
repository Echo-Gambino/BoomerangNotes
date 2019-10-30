import os
working_dir = os.path.dirname(os.path.realpath(__file__))


class Config:
    APP_DESCRIPTION = 'An application that reminds you of important information!'

    WORKING_DIR = working_dir

    BASE_PATH = WORKING_DIR + '/app/template/base.html'

    ERROR_PATH = WORKING_DIR + '/app/template/error.html'

    def get_reminder_path(self, title):
        output = '{0}/data/{1}_Reminder.html'.format(self.WORKING_DIR, title)
        return output






