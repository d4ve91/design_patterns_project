
import sys
import os
import re


class MenuCommand:
    def description(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    @staticmethod
    def program():
        program_py = sys.executable
        os.execl(program_py, program_py, *sys.argv)

    def event_title(self):
        new_event_title = input("Title: ")
        if not self.title(new_event_title):
            raise ValueError("Invalid input")
        return new_event_title

    def event_date(self):
        set_event_date = input("Date (DD.MM.YYYY): ")
        if not self.date(set_event_date):
            raise ValueError("Invalid input")
        return set_event_date

    def event_time(self):
        set_event_time = input("Time (HH:MM): ")
        if not self.time(set_event_time):
            raise ValueError("Invalid input")
        return set_event_time

    @staticmethod
    def title(topic):
        if re.search("[^a-zA-Z0-9-,. ]", topic):
            return False
        return True

    def date(self, new_event_date):
        if not re.match("[0-3][0-9].[0-1][0-9].202[0-9]", new_event_date):
            return False
        numbers = re.split("[.]", new_event_date)
        day = int(numbers[0])
        month = int(numbers[1])
        year = int(numbers[2])
        if month == 0 or month > 12:
            return False
        if not self.day(day, month, year):
            return False
        return True

    @staticmethod
    def day(day, month, year):
        if day == 0:
            return False
        if month == 2:
            is_leap_year = year % 4 == 0
            return (day <= 29 and is_leap_year) or (day <= 28 and not is_leap_year)
        has31days = month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12
        return (day <= 31 and has31days) or (day <= 30 and not has31days)

    @staticmethod
    def time(time):
        if not re.match("[0-2][0-9]:[0-5][0-9]", time):
            return False
        numbers = re.split("[:]", time)
        hour = int(numbers[0])
        if hour > 23:
            return False
        return True

    @staticmethod
    def icalendar_start():
        print('''BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VTIMEZONE
TZID:Europe/Warsaw
X-LIC-LOCATION:Europe/Warsaw
END:VTIMEZONE''')

    def icalendar_event(self):
        for event in self.calendar:
            print('''BEGIN:VEVENT
DTSTART:{}{}{}T{}{}00
DTEND:{}{}{}T{}{}00
SUMMARY:{}
END:VEVENT'''.format(event['date'][6:10], event['date'][3:5], event['date'][0:2], event['time'][0:2],
                     event['time'][3:5], event['date'][6:10], event['date'][3:5], event['date'][0:2],
                     event['time'][0:2], event['time'][3:5], event['title']))

    @staticmethod
    def icalendar_end():
        print('''END:VCALENDAR''')

    def list_calendar(self):
        for event in self.calendar:
            print("Title: {}\nDate: {}, {}".format(event['title'], event['date'], event['time']))


class AddCommandAsANewEvent(MenuCommand):
    def __init__(self, calendar):
        self.calendar = calendar

    def description(self):
        return "New event"

    def execute(self):
        title = self.event_title()
        date = self.event_date()
        time = self.event_time()
        event = {
            'title': title,
            'date': date,
            'time': time,
        }
        self.calendar.append(event)


class PrintListFromCalendar(MenuCommand):
    def __init__(self, calendar):
        self.calendar = calendar

    def description(self):
        return "List calendar"

    def execute(self):
        self.list_calendar()


class AddCommandToiCalendar(MenuCommand):
    def __init__(self, calendar):
        self.calendar = calendar

    def description(self):
        return "Export calendar to iCalendar"

    def execute(self):
        self.icalendar_start()
        self.icalendar_event()
        self.icalendar_end()


class ExitCommand(MenuCommand):
    def __init__(self, menu):
        super().__init__()
        self._menu = menu

    def description(self):
        return "Exit"

    def execute(self):
        self._menu.stop()


class Menu:
    def __init__(self):
        self._commands = []
        self._should_running = True

    def add_command(self, cmd):
        self._commands.append(cmd)

    def run(self):
        while self._should_running:
            self._display_menu()
            self._execute_selected_command()

    def stop(self):
        self._should_running = False

    def _display_menu(self):
        for i, cmd in enumerate(self._commands):
            print("{}. {}".format(i + 1, cmd.description()))

    def _execute_selected_command(self):
        while True:
            try:
                cmd_num = int(input("Select menu item (1-{}): ".format(len(self._commands))))
                cmd = self._commands[cmd_num - 1]
                cmd.execute()
            except ValueError:
                print("Invalid input")
                continue
            else:
                break
