class JSONElement:
    def __init__(self, item):
        self.item = item

    def pop(self, key: str):
        value = self.item[key]
        del self.item[key]
        return value

    def get_object(self, key: str):
        return JSONElement(self.item[key])

    def __getitem__(self, item):
        return self.item[item]

    def as_dict(self):
        return self.item
