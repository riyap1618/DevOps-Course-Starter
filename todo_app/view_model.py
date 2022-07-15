class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    def get_items_by_status(self, status):
        result = []
        for item in self._items:
            if item.status == status:
                result.append(item)
        return result

    @property
    def doing_items(self):
        return self.get_items_by_status('Doing')

    @property
    def todo_items(self):
        return self.get_items_by_status('To Do')

    @property
    def done_items(self):
        return self.get_items_by_status('Done')
