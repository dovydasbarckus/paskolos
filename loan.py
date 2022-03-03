

class Loan:
    def __init__(self, variable1, variable2, variable3):
        self.amount = variable1
        self.period = variable2
        self.interest = variable3
        self.total_interests = []
        self.columns = {
            "Month Nr.": [],
            "Amount to be refunded €": [],
            "Balance €": [],
            "Added Interests €": [],
            "Final sum to pay €": []
        }
        self.new_row = {}
        self.__my_loan__()

    def __my_loan__(self):
        amount_every_month_to_pay = self.amount / self.period
        left_to_pay = self.amount
        numbers_of_months = []
        balance = []
        for months in range(int(self.period)):
            self.total_interests.append(round(left_to_pay * (self.interest / 100) / 12, 2))
            left_to_pay -= round(amount_every_month_to_pay, 2)
            numbers_of_months.append(months + 1)
            balance.append(left_to_pay)

        self.columns["Month Nr."] = numbers_of_months
        self.columns["Amount to be refunded €"] = [round(amount_every_month_to_pay, 2) for x in numbers_of_months]
        balance_rounded = [round(num, 2) for num in balance]
        self.columns["Balance €"] = balance_rounded
        self.columns["Added Interests €"] = self.total_interests
        self.columns["Final sum to pay €"] = [round(x + amount_every_month_to_pay, 2) for x in self.total_interests]
        self.new_row = {'Month Nr.': ['Total'],
                   'Amount to be refunded €': [self.amount],
                   'Balance €': [""],
                   'Added Interests €': [sum(self.total_interests)],
                   "Final sum to pay €": [self.amount + sum(self.total_interests)]
                   }

