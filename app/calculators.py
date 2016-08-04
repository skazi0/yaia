from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal(10) ** -2

def fixed_mul(x, y):
    return (Decimal(x) * Decimal(y)).quantize(TWOPLACES, rounding=ROUND_HALF_UP)

class LineCalculator(object):
    def calculate(self, line):
        line.net_value = fixed_mul(line.quantity, line.unit_price)
        return line
