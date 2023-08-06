class Price:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    def __repr__(self):
        return '(First {}, Last {})'.format(self.first, self.last)

    def get_first(self):
        """Return first element"""
        return self.first

    def get_last(self):
        """Return last Element"""
        return self.last()


def sort_prices(n):
    """Sorted array of prices"""
    sorted_data = sorted(n)
    first_item = sorted_data[0]
    last_item = sorted_data[-1]
    price = Price(first=first_item, last=last_item)
    return sorted_data, price
