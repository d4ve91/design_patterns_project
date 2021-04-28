from menu import Menu, MenuCommand, AddCommandAsANewEvent, PrintListFromCalendar, AddCommandToiCalendar, ExitCommand
import calendar

def main():

    calendar = []
    
    # event = {
    #    'title': 'Programowanie obiektowe w jezyku PYTHON - Cwiczenia',
    #    'date': '28.03.2020',
    #    'time': '12:45',
    # }
    #
    # calendar.append(event)

    menu = Menu()


    menu.add_command(AddCommandAsANewEvent(calendar))
    menu.add_command(PrintListFromCalendar(calendar))
    menu.add_command(AddCommandToiCalendar(calendar))
    menu.add_command(ExitCommand(menu))

    menu.run()


main()
