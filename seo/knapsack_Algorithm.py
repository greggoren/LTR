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
            portion = min(self.MAXWT - wt, amount)
            wt  += portion
            addval  = portion * unit_value
            val    += addval
            bagged += [(name, portion, addval)]
            if wt >= self.MAXWT:
                break
        return bagged