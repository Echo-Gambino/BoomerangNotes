from datetime import datetime


class Reminder:

    def __init__(self):
        self.title = ""
        self.descr = ""
        self.alarm = datetime.now()


    def __repr__(self):
        return '<Reminder \"{}\" @ {}>'.format(self.title, self.alarm);
  
    
    def gen_verbose_description(self):
        output = ''

        output += "title:\n> {}\n\n".format(self.title)
        output += "description:\n> {}\n\n".format(self.descr)
        output += "delay:\n> {}\n".format(self.conv_time_to_string(self.alarm))

        return output


    def conv_time_to_string(self, time):
        year = self.conv_num_to_nchar(time.year, 4)
        month = self.conv_num_to_nchar(time.month, 2)
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




