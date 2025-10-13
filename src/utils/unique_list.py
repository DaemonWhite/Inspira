class UniqueList(list):
    def append(self, item):
        if item.lower() not in self:
            super().append(item.lower())
        else:
            raise ValueError(f"'{item}' existe is present in list")

    def extend(self, iterable):
        for item in iterable:
            self.append(item)
