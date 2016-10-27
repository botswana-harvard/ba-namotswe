

class Regimen:

    def __init__(self, value):
        self.value = value
        self.parsed_value = self.parse_regimen(value)

    def parse_regimen(self, value):
        value = value.split(',')
        return value
