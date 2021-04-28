

class ListingStrategy:
    def begin(self):
        pass

    def event(self, title, date, time):
        pass

    def end(self):
        pass


def list_calendar(calendar, listing_strategy):
    listing_strategy.begin()

    for event in calendar:
        title = event['title']
        date = event['date']
        time = event['time']
        listing_strategy.event(title, date, time)

    listing_strategy.end()
