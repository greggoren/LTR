class knapsack:

    def __init__(self,items,MAXWT):
        self.items = items
        self.MAXWT = MAXWT

    def pack(self):
        sorted_items = sorted(((value/amount, amount, name)
                               for name, amount, value in self.items),
                              reverse = True)
        wt = val = 0
        bagged = []
        for unit_value, amount, name in sorted_items:

            portion = amount
            wt += portion
            if wt >= self.MAXWT:
                wt -= portion
                continue

            addval  = portion * unit_value
            val    += addval
            bagged += [(name, portion, addval)]

        return bagged