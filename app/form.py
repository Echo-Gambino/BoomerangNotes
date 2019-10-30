from app import model
from app import input_utils


class Form:

    GAP = 2 * "\n"

    def __init__(self):
        self.reminder = model.Reminder()
        pass


    def get_reminder(self):
        return self.reminder


    def start_form(self, confirm = False):
        iUtils = input_utils.InputUtils()

        self.splash_intro()

        while True:
            self.reminder.title = iUtils.get_title(True)

            self.reminder.descr = iUtils.get_descr(True)

            self.reminder.alarm = iUtils.get_time(True)

            self.show_results()

            if confirm or iUtils.get_confirmation():
                break

        self.splash_outro()

        pass


    def splash_intro(self):
        message = "----B-O-0-M-E-R-A-N-G- - <" 

        prompt = Form.GAP + message + Form.GAP

        print(prompt)


    def splash_outro(self):
        message = "--- Boomerang thrown, have a nice day! --<"

        prompt = Form.GAP + message + Form.GAP

        print(prompt)


    def show_results(self):
        message0 = "Please review reminder info:\n"
        message1 = self.reminder.gen_verbose_description()

        prompt = Form.GAP + message0 + message1 + Form.GAP

        print(prompt) 

