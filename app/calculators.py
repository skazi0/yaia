from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal(10) ** -2


def fixed_mul(x, y):
    return (Decimal(x) * Decimal(y)).quantize(TWOPLACES,
                                              rounding=ROUND_HALF_UP)


class LineCalculator(object):
    def calculate(self, line):
        if line.is_prepaid:
            line.net_value = line.unit_price
        else:
            line.net_value = fixed_mul(line.quantity, line.unit_price)
        return line


class TotalCalculator(object):
    def calculate(self, lines):
        subtotals = defaultdict(lambda: {'net': Decimal(0),
                                         'tax': Decimal(0),
                                         'gross': Decimal(0)})
        total = {'net': Decimal(0), 'tax': Decimal(0), 'gross': Decimal(0)}

        for l in lines:
            tax_rate = l['tax_rate']
            subtotals[tax_rate]['net'] += Decimal(l['net_value'])

        for r, s in subtotals.items():
            if r is not None:
                s['tax'] = fixed_mul(s['net'], Decimal(r)/Decimal(100.0))
            s['gross'] = s['net'] + s['tax']

            total['net'] += s['net']
            total['tax'] += s['tax']
            total['gross'] += s['gross']

        return (subtotals, total)
