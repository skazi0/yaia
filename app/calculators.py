class LineCalculator(object):
    def calculate(self, line):
        line.net_value = line.quantity * line.unit_price
        return line
