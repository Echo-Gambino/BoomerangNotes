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
        year = time.year
        month = time.month
        day = time.day

        hour = time.hour
        minute = time.minute
        seconds = time.second

        prompt_date = "{0}-{1}-{2}".format(year, month, day)
        prompt_time = "{0}:{1}:{2}".format(hour, minute, seconds)

        prompt = "{0} {1}".format(prompt_date, prompt_time)

        return prompt



