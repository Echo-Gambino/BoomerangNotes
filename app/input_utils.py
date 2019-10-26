from datetime import datetime
import os


class InputUtils:


    def get_title(self, confirm = False):
        prompt = "What is the subject of your reminder?"
        return self.get_input_from_prompt(prompt, confirm)

    
    def get_descr(self, working_dir, confirm = False):
        prompt = "Please add to the reminder by providing a description."
        return self.get_input_from_textfile(prompt, working_dir, confirm)
        # return self.get_input_from_prompt(prompt, confirm)


    def get_time(self, confirm = False):
        prompt = 'Please set the time at which you would like to be reminded at:\n'

        return self.get_input_for_time(prompt, confirm)


    def get_input_for_time(self, prompt, confirm = False):
        user_time = datetime.now()

        format_instructions = "Please input in this format:\nYYYY-MM-DD hh:mm:ss"

        cur_time = datetime.now()

        while True:
            print(prompt)

            print("It is currently {}.\n".format(datetime.now()))

            print(format_instructions)

            user_input = self.get_input()

            try:
                token = user_input.split(' ')

                token_date = [int(i) for i in token[0].split('-')]
                token_time = [int(i) for i in token[1].split(':')]

                user_time = datetime(
                    abs(token_date[0]), abs(token_date[1]) & 12, abs(token_date[2]),
                    abs(token_time[0]) % 24, abs(token_time[1]) % 60, abs(token_time[2]) % 60)
            except:
                print("Error, input not recognized, please input the time in the format specified\n")
                continue

            print("You have set the reminder time to be:\n{}".format(self.conv_time_to_string(user_time)))
            if not confirm or self.get_confirmation():
                break

        return user_time


    def conv_time_to_string(self, time):
        year = self.conv_num_to_nchar(time.year, 4)
        month = self.conv_num_to_nchar(time.month % 12, 2)
        day = self.conv_num_to_nchar(time.day, 2)

        hour = self.conv_num_to_nchar(time.hour, 2)
        minute = self.conv_num_to_nchar(time.minute, 2)
        seconds = self.conv_num_to_nchar(time.second, 2)

        prompt_date = "{0}-{1}-{2}".format(year, month, day)
        prompt_time = "{0}:{1}:{2}".format(hour, minute, seconds)

        prompt = "{0} {1}".format(prompt_date, prompt_time)

        return prompt


    def conv_num_to_nchar(self, number, min_length = 0):
        string = str(number)

        while len(string) < min_length:
            string = '0' + string

        return string


    def get_input_from_textfile(self, prompt, working_dir, confirm):
        user_input = ''

        # generate the FULL path of the temporary file
        #working_dir = os.path.dirname(os.path.realpath(__file__))
        tmpfile_path = '/data/temp/tmp.txt'
        full_path = working_dir + tmpfile_path

        # wipe all data from full_path
        open(full_path, 'w').close()

        while True:
            print(prompt)

            # construct command (text_editor and full path) and execute it
            # to open the designated text editor that the user can write into
            text_editor = 'mousepad'
            command = '{0} {1}'.format(text_editor, full_path)
            os.system(command)

            # open the same file (which should be updated by the user)
            # and gather all the text within it to be placed into the data variable
            data = ''
            with open(full_path, 'r') as file:
                data = file.read()

            # clean out the user data and place it into user_input
            user_input = data.strip()

            # print out the result of reading the tmp file
            # just to that the user can preview what they wrote down
            print('Here is what you have wrote down:')
            print(user_input)
            
            if not confirm:
                break
            else:
                if (self.get_confirmation()):
                    break
                else:
                    edit_prompt = "would you like to continue where you left off (y), or would you like to write the description from scratch (n)?"
                    user_will_edit = self.get_confirmation(prompt)
                    if not user_will_edit:
                        open(full_path, 'w').close()
                    continue

        try:
            os.remove(full_path)
        except:
            print('Error, could not remove {0}'.format(full_path))

        return user_input


    def get_input_from_prompt(self, prompt, confirm = False):
        user_input = ''

        while True:
            print(prompt)
            user_input = self.get_input()

            if not confirm or self.get_confirmation():
                break

        return user_input


    def get_confirmation(self, prompt = 'Confirm?', default = 'y'):

        YES = True
        NO = False

        input_dict = {
                'y': YES,
                'n': NO
                }
        
        option0 = 'y'
        option1 = 'n'

        if default.lower() == 'y':
            input_dict[''] = YES
            option0 = '[Y]'
        elif default.lower() == 'n':
            input_dict[''] = NO
            option1 = '[N]'

        user_input = 'y'

        while True:

            print('{0} {1}/{2}'.format(prompt, option0, option1))

            user_input = self.get_input(True).replace(' ', '').replace('\n', '').replace('\t', '')

            if not user_input in input_dict.keys():
                print("Error, invalid input, please try typing \'y\' or \'n\'.")
                continue
            else:
                break

        return input_dict[user_input]


    def get_input(self, lowercase = False):

        user_input = input("< ").strip()

        if (lowercase):
            user_input = user_input.lower()

        return user_input


    def debug_display_output(self, string):
        stars = 3 * "_"

        print("{}.{}.{}".format(stars, string, stars))

    pass

